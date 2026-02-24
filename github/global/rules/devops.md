# DevOps & Infrastructure Rules

## 1. Infrastructure as Code (IaC)
- All infrastructure changes must be defined in code (Terraform, Dockerfile, Kubernetes manifests).
- Manual changes to production servers are strictly forbidden.

## 2. CI/CD Pipeline
- Every commit to `main` must pass all tests.
- Deployment to production requires a successful build and passing e2e tests.
- Rollback mechanisms must be automated and tested.

## 3. Containerization
- Use multi-stage Docker builds to minimize image size.
- Do not run containers as root.
- Scan images for vulnerabilities before deployment.

## 4. Monitoring & Logging
- All services must emit structured JSON logs.
- Critical metrics (latency, error rate, saturation) must have alerts.
- Logs must not contain PII or secrets.

## 5. Security
- Secrets must be injected via environment variables or secret managers, never committed to code.
- Least privilege principle applies to all service accounts and roles.
