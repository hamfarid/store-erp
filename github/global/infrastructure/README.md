# Infrastructure — Global System v26.0.2 Diamond 32

> Docker, Kubernetes, Terraform, Ansible, and CI/CD configurations.

## Structure
| Directory | Contents |
|-----------|----------|
| `containers/` | Docker containers (GAARA-AI, learning, search) |
| `docker/` | Dockerfiles and compose files for ML pipeline |
| `k8s/` | Kubernetes manifests |
| `iac/` | Terraform & Trivy configs |
| `ansible/` | Ansible playbooks |
| `monitoring/` | Grafana/Prometheus configs |

## Key Files
- `Dockerfile.backend` — Backend service image
- `Dockerfile.frontend` — Frontend service image
- `docker-compose.shared.yml` — Shared services
- See `DOCKER_GUIDE.md` at project root for usage guide
