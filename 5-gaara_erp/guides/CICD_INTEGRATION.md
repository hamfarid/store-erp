# CI/CD Integration Guide

دليل شامل لإعداد التكامل والنشر المستمر (CI/CD) مع أفضل الممارسات.

---

## 📋 المحتويات

1. [GitHub Actions](#github-actions)
2. [GitLab CI](#gitlab-ci)
3. [Security Scanning](#security-scanning)
4. [Quality Gates](#quality-gates)
5. [Deployment Strategies](#deployment-strategies)

---

## GitHub Actions

### Complete CI/CD Workflow

```yaml
# FILE: .github/workflows/ci-cd.yml | PURPOSE: Complete CI/CD pipeline | OWNER: DevOps | LAST-AUDITED: 2025-10-28

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.11'

jobs:
  # ========================================
  # Stage 1: Code Quality & Security
  # ========================================
  code-quality:
    name: Code Quality & Linting
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      
      - name: Install dependencies
        run: |
          corepack enable
          pnpm install --frozen-lockfile
      
      - name: ESLint
        run: pnpm lint
      
      - name: Prettier Check
        run: pnpm format:check
      
      - name: TypeScript Check
        run: pnpm type-check
      
      - name: Python Linting
        run: |
          pip install flake8 black mypy
          flake8 backend/
          black --check backend/
          mypy backend/

  security-scan:
    name: Security Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Secret Scanning
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
      
      - name: Dependency Scanning
        run: |
          npm audit --production
          pip-audit
      
      - name: SAST with Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
      
      - name: Container Scanning
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  # ========================================
  # Stage 2: Testing
  # ========================================
  test-frontend:
    name: Frontend Tests
    runs-on: ubuntu-latest
    needs: [code-quality]
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      
      - name: Install dependencies
        run: |
          corepack enable
          pnpm install --frozen-lockfile
      
      - name: Unit Tests
        run: pnpm test:unit --coverage
      
      - name: Integration Tests
        run: pnpm test:integration
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: frontend

  test-backend:
    name: Backend Tests
    runs-on: ubuntu-latest
    needs: [code-quality]
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Unit Tests
        run: pytest tests/unit --cov=backend --cov-report=xml
      
      - name: Integration Tests
        run: pytest tests/integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379/0
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: backend

  e2e-tests:
    name: E2E Tests
    runs-on: ubuntu-latest
    needs: [test-frontend, test-backend]
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      
      - name: Install Playwright
        run: |
          corepack enable
          pnpm install --frozen-lockfile
          pnpm exec playwright install --with-deps
      
      - name: Run E2E Tests
        run: pnpm test:e2e
      
      - name: Upload Playwright Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/

  # ========================================
  # Stage 3: Build
  # ========================================
  build:
    name: Build & Package
    runs-on: ubuntu-latest
    needs: [security-scan, test-frontend, test-backend, e2e-tests]
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ secrets.REGISTRY_URL }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}
      
      - name: Build Frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          file: ./frontend/Dockerfile
          push: true
          tags: |
            ${{ secrets.REGISTRY_URL }}/frontend:${{ github.sha }}
            ${{ secrets.REGISTRY_URL }}/frontend:latest
          cache-from: type=registry,ref=${{ secrets.REGISTRY_URL }}/frontend:buildcache
          cache-to: type=registry,ref=${{ secrets.REGISTRY_URL }}/frontend:buildcache,mode=max
      
      - name: Build Backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile
          push: true
          tags: |
            ${{ secrets.REGISTRY_URL }}/backend:${{ github.sha }}
            ${{ secrets.REGISTRY_URL }}/backend:latest
      
      - name: Generate SBOM
        run: |
          docker sbom ${{ secrets.REGISTRY_URL }}/frontend:${{ github.sha }} > frontend-sbom.json
          docker sbom ${{ secrets.REGISTRY_URL }}/backend:${{ github.sha }} > backend-sbom.json
      
      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: |
            frontend-sbom.json
            backend-sbom.json

  # ========================================
  # Stage 4: Deploy
  # ========================================
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build]
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/frontend frontend=${{ secrets.REGISTRY_URL }}/frontend:${{ github.sha }} -n staging
          kubectl set image deployment/backend backend=${{ secrets.REGISTRY_URL }}/backend:${{ github.sha }} -n staging
          kubectl rollout status deployment/frontend -n staging
          kubectl rollout status deployment/backend -n staging

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v4
      
      - name: Canary Deployment
        run: |
          # Deploy canary (10% traffic)
          kubectl set image deployment/frontend-canary frontend=${{ secrets.REGISTRY_URL }}/frontend:${{ github.sha }} -n production
          kubectl rollout status deployment/frontend-canary -n production
          
          # Wait and monitor
          sleep 300
          
          # Check metrics
          if ./scripts/check-canary-health.sh; then
            # Promote to full deployment
            kubectl set image deployment/frontend frontend=${{ secrets.REGISTRY_URL }}/frontend:${{ github.sha }} -n production
            kubectl set image deployment/backend backend=${{ secrets.REGISTRY_URL }}/backend:${{ github.sha }} -n production
          else
            # Rollback canary
            kubectl rollout undo deployment/frontend-canary -n production
            exit 1
          fi
      
      - name: Smoke Tests
        run: |
          curl -f https://example.com/api/health || exit 1
          curl -f https://example.com/ || exit 1
      
      - name: Notify Success
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "✅ Deployment to production successful!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Deployment Successful* :white_check_mark:\n*Environment:* Production\n*Commit:* ${{ github.sha }}\n*Author:* ${{ github.actor }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## GitLab CI

### .gitlab-ci.yml

```yaml
# FILE: .gitlab-ci.yml | PURPOSE: GitLab CI/CD pipeline | OWNER: DevOps | LAST-AUDITED: 2025-10-28

stages:
  - lint
  - test
  - security
  - build
  - deploy

variables:
  NODE_VERSION: "20"
  PYTHON_VERSION: "3.11"
  DOCKER_DRIVER: overlay2

# ========================================
# Lint Stage
# ========================================
lint:frontend:
  stage: lint
  image: node:20
  script:
    - corepack enable
    - pnpm install --frozen-lockfile
    - pnpm lint
    - pnpm format:check
    - pnpm type-check
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

lint:backend:
  stage: lint
  image: python:3.11
  script:
    - pip install flake8 black mypy
    - flake8 backend/
    - black --check backend/
    - mypy backend/

# ========================================
# Test Stage
# ========================================
test:frontend:
  stage: test
  image: node:20
  script:
    - corepack enable
    - pnpm install --frozen-lockfile
    - pnpm test:unit --coverage
    - pnpm test:integration
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:backend:
  stage: test
  image: python:3.11
  services:
    - postgres:15
    - redis:7
  variables:
    POSTGRES_DB: test
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/test
    REDIS_URL: redis://redis:6379/0
  script:
    - pip install -r requirements.txt pytest pytest-cov
    - pytest tests/ --cov=backend --cov-report=xml --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

# ========================================
# Security Stage
# ========================================
security:sast:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config=auto --sarif > semgrep-results.sarif
  artifacts:
    reports:
      sast: semgrep-results.sarif

security:dependency:
  stage: security
  image: node:20
  script:
    - npm audit --production --audit-level=moderate
    - pip-audit

security:secrets:
  stage: security
  image: trufflesecurity/trufflehog:latest
  script:
    - trufflehog filesystem . --json > secrets-scan.json
  artifacts:
    paths:
      - secrets-scan.json

# ========================================
# Build Stage
# ========================================
build:docker:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA -f frontend/Dockerfile frontend/
    - docker build -t $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA -f backend/Dockerfile backend/
    - docker push $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA

# ========================================
# Deploy Stage
# ========================================
deploy:staging:
  stage: deploy
  image: bitnami/kubectl:latest
  only:
    - develop
  script:
    - kubectl set image deployment/frontend frontend=$CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA -n staging
    - kubectl set image deployment/backend backend=$CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA -n staging
    - kubectl rollout status deployment/frontend -n staging
    - kubectl rollout status deployment/backend -n staging
  environment:
    name: staging
    url: https://staging.example.com

deploy:production:
  stage: deploy
  image: bitnami/kubectl:latest
  only:
    - main
  when: manual
  script:
    - kubectl set image deployment/frontend frontend=$CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA -n production
    - kubectl set image deployment/backend backend=$CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA -n production
    - kubectl rollout status deployment/frontend -n production
    - kubectl rollout status deployment/backend -n production
  environment:
    name: production
    url: https://example.com
```

---

## Security Scanning

### Comprehensive Security Pipeline

```yaml
# FILE: .github/workflows/security.yml | PURPOSE: Security scanning | OWNER: Security | LAST-AUDITED: 2025-10-28

name: Security Scanning

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  push:
    branches: [main, develop]

jobs:
  secret-scan:
    name: Secret Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: TruffleHog
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  dependency-scan:
    name: Dependency Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: npm audit
        run: npm audit --production --audit-level=moderate
      
      - name: Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

  sast:
    name: SAST
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
            p/cwe-top-25

  container-scan:
    name: Container Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build image
        run: docker build -t myapp:test .
      
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:test'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
      
      - name: Upload to Security tab
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

---

## Quality Gates

### SonarQube Integration

```yaml
# FILE: .github/workflows/quality-gate.yml | PURPOSE: Quality gates | OWNER: QA | LAST-AUDITED: 2025-10-28

name: Quality Gate

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sonarqube:
    name: SonarQube Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: SonarQube Scan
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
      
      - name: Quality Gate
        uses: sonarsource/sonarqube-quality-gate-action@master
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        with:
          scanMetadataReportFile: .scannerwork/report-task.txt

  lighthouse:
    name: Lighthouse CI
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            https://staging.example.com
            https://staging.example.com/dashboard
          uploadArtifacts: true
          temporaryPublicStorage: true
          budgetPath: ./lighthouse-budget.json
```

---

## Deployment Strategies

### Blue-Green Deployment

```bash
#!/bin/bash
# FILE: scripts/blue-green-deploy.sh | PURPOSE: Blue-green deployment | OWNER: DevOps | LAST-AUDITED: 2025-10-28

set -e

IMAGE_TAG=$1
NAMESPACE="production"

# Determine current active deployment
ACTIVE=$(kubectl get service app -n $NAMESPACE -o jsonpath='{.spec.selector.version}')

if [ "$ACTIVE" == "blue" ]; then
    NEW="green"
else
    NEW="blue"
fi

echo "Current active: $ACTIVE"
echo "Deploying to: $NEW"

# Deploy new version
kubectl set image deployment/app-$NEW app=$IMAGE_TAG -n $NAMESPACE
kubectl rollout status deployment/app-$NEW -n $NAMESPACE

# Run smoke tests
./scripts/smoke-tests.sh https://app-$NEW.internal

# Switch traffic
kubectl patch service app -n $NAMESPACE -p "{\"spec\":{\"selector\":{\"version\":\"$NEW\"}}}"

echo "Traffic switched to $NEW"
echo "Old version ($ACTIVE) still running for rollback"
```

### Canary Deployment

```bash
#!/bin/bash
# FILE: scripts/canary-deploy.sh | PURPOSE: Canary deployment | OWNER: DevOps | LAST-AUDITED: 2025-10-28

set -e

IMAGE_TAG=$1
CANARY_WEIGHT=10  # 10% traffic

# Deploy canary
kubectl set image deployment/app-canary app=$IMAGE_TAG -n production
kubectl rollout status deployment/app-canary -n production

# Update traffic split
kubectl patch virtualservice app -n production --type=json -p="[
  {\"op\": \"replace\", \"path\": \"/spec/http/0/route/0/weight\", \"value\": $((100-CANARY_WEIGHT))},
  {\"op\": \"replace\", \"path\": \"/spec/http/0/route/1/weight\", \"value\": $CANARY_WEIGHT}
]"

echo "Canary deployed with $CANARY_WEIGHT% traffic"
echo "Monitoring for 5 minutes..."

sleep 300

# Check metrics
if ./scripts/check-canary-metrics.sh; then
    echo "Canary healthy, promoting to stable"
    kubectl set image deployment/app app=$IMAGE_TAG -n production
    kubectl rollout status deployment/app -n production
    
    # Reset traffic to 100% stable
    kubectl patch virtualservice app -n production --type=json -p="[
      {\"op\": \"replace\", \"path\": \"/spec/http/0/route/0/weight\", \"value\": 100},
      {\"op\": \"replace\", \"path\": \"/spec/http/0/route/1/weight\", \"value\": 0}
    ]"
else
    echo "Canary unhealthy, rolling back"
    kubectl rollout undo deployment/app-canary -n production
    exit 1
fi
```

---

**آخر تحديث:** 2025-10-28  
**الإصدار:** 1.0.0

