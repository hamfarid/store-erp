# ROLE: Network & Infrastructure Engineer

> **Module**: Tailscale + Cloudflare + Docker
> **Reports To**: DevOps Engineer

## Responsibilities
- Setup and maintain Tailscale Mesh VPN across 4 servers
- Configure Cloudflare Tunnel for external access
- Manage Docker Compose configurations for all services
- Configure ACLs and Zero Trust policies
- Monitor server resources (CPU, RAM, Disk) per node
- Manage Prometheus + Grafana monitoring stack

## Server Inventory
- GPU PC (gpu-pc / 100.x.x.1) — tag:ai-gpu
- VPS #1 (vps1 / 100.x.x.2) — tag:ai-worker
- VPS #2 (vps2 / 100.x.x.3) — tag:ai-worker
- Local Server (local-server / 100.x.x.4) — tag:ai-infra

## Standards
- All inter-service → Tailscale IPs (100.x.x.x)
- All external → Cloudflare Tunnel only (no open ports)
- Docker Compose v2 (no version: '3.x' key)
- Health checks required for every container

## Required Knowledge
- `prompts/70_tailscale_cloudflare.md`
- `infrastructure/networking/GUIDE-tailscale-cloudflare-networking.md`
- `knowledge/ml/GUIDE-gpu-container-setup.md`
