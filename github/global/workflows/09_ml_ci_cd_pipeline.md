# ML CI/CD Pipeline Workflow (v18.0)
# Scope: Automated Testing, Building, and Deployment
# Tools: GitHub Actions, Jenkins, ArgoCD

## 1. Pipeline Stages

### 1.1 Continuous Integration (CI)
*   **Trigger**: Push to `main` or Pull Request.
*   **Steps**:
    1.  **Linting**: Run `ruff check .` and `biome check .`.
    2.  **Unit Tests**: Run `pytest tests/unit`.
    3.  **Security Scan**: Run `trivy fs .` (Code Scan).
    4.  **Build**: Build Docker image `gaara/ml-serving:${SHA}`.

### 1.2 Continuous Delivery (CD) - Staging
*   **Trigger**: Merge to `main`.
*   **Steps**:
    1.  **Push Image**: Push to ECR/DockerHub.
    2.  **Deploy Staging**: Update K8s manifest in `gitops-repo/staging`.
    3.  **Integration Tests**: Run `pytest tests/integration` against Staging URL.
    4.  **Performance Tests**: Run `k6 run load_test.js`.

### 1.3 Continuous Deployment (CD) - Production
*   **Trigger**: Manual Approval (or Auto-Promote if Gates Pass).
*   **Steps**:
    1.  **Promote Image**: Tag image as `v1.2.3`.
    2.  **Deploy Production**: Update K8s manifest in `gitops-repo/production`.
    3.  **Canary Rollout**: Argo Rollouts manages traffic shift (1% -> 100%).
    4.  **Verify**: Check Health/Metrics (Prometheus).

## 2. GitHub Actions Example

```yaml
name: ML CI/CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest ruff
    - name: Lint
      run: ruff check .
    - name: Test
      run: pytest tests/unit

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker Image
      run: docker build -t gaara/ml-serving:${{ github.sha }} -f infrastructure/docker/Dockerfile.ml-serving .
    - name: Scan Image
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'gaara/ml-serving:${{ github.sha }}'
        format: 'table'
        exit-code: '1'
        ignore-unfixed: true
        vuln-type: 'os,library'
        severity: 'CRITICAL,HIGH'
```

## 3. ArgoCD Application Example

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ml-serving-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/gaara/gitops-repo.git
    targetRevision: HEAD
    path: production/ml-serving
  destination:
    server: https://kubernetes.default.svc
    namespace: ml-production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```
