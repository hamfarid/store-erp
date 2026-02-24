# Prompt 70: Network Infrastructure — Tailscale + Cloudflare

> **Scope**: Internal VPN mesh and external access for GAARA-AI
> **When to Load**: Network architecture, server connectivity, external access

## Two-Layer Architecture

### Layer 1: Tailscale Mesh VPN (Internal)
- **Purpose**: Connect all 4 servers into private 100.x.x.x network
- **Protocol**: WireGuard-based, P2P (>90% direct connections)
- **DNS**: MagicDNS — auto hostname resolution (gpu-pc, vps1, vps2, local-server)
- **Cost**: Free (Personal plan: 100 devices)

### Layer 2: Cloudflare Tunnel (External)
- **Purpose**: Expose services to internet without opening ports
- **Features**: Auto HTTPS, DDoS protection, WAF, Zero Trust auth
- **Container**: cloudflared runs on Local Server

## Server Tags & ACLs
```
tag:ai-gpu    → GPU PC (LLM, training)
tag:ai-worker → VPS #1, VPS #2 (scraping, processing)
tag:ai-infra  → Local Server (databases, gateway)
```

### Access Rules
- AI services (gpu, worker) → can reach infrastructure (infra)
- GPU → can reach workers
- Workers → can reach GPU on port 11434 only (Ollama)
- Infrastructure → can reach infrastructure

## Public Hostnames (Cloudflare)
```
ai.gaara.com      → http://api-gateway:8000  (API Gateway)
erp.gaara.com     → http://localhost:8080    (Django ERP)
flower.gaara.com  → http://flower:5555       (Celery Monitor)
grafana.gaara.com → http://grafana:3000      (Monitoring)
```

## Why Tailscale + Cloudflare (Not WireGuard)
| Feature | WireGuard (manual) | Tailscale + Cloudflare |
|:--------|:-------------------|:-----------------------|
| Setup | Complex (keys, configs per node) | 1 minute per node |
| NAT Traversal | Fails behind Double NAT | Auto P2P (>90%) |
| DNS | Manual | MagicDNS auto |
| Adding nodes | Update all configs manually | Just `tailscale up` |
| HTTPS | Manual Nginx + Let's Encrypt | Auto Cloudflare |
| Security | Good | Zero Trust + ACLs + Audit Log |
| Cost | Free | Free (Personal plan) |
| Monitoring | None | Tailscale Admin + Cloudflare Dashboard |

## Rules
- All inter-service communication uses Tailscale IPs (100.x.x.x)
- External access ONLY through Cloudflare Tunnel (no open ports)
- Zero Trust authentication required for all external hostnames
- ACLs enforced per server tag — least privilege principle
