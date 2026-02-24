# Rule: Container Networking — Tailscale + Cloudflare

> **Applies To**: All GAARA-AI infrastructure

## Internal Communication (Tailscale)
1. All inter-service communication MUST use Tailscale IPs (100.x.x.x)
2. MagicDNS hostnames (gpu-pc, vps1, vps2, local-server) are preferred over raw IPs
3. Never hardcode Tailscale IPs — use environment variables
4. All ports are accessible within the mesh (no firewall config needed)

## External Access (Cloudflare)
1. NO ports shall be opened on any server firewall
2. ALL external access MUST go through Cloudflare Tunnel
3. Zero Trust authentication REQUIRED on all public hostnames
4. Cloudflare Access policy: email domain @gaara.com + One-time PIN

## ACL Rules (Tailscale Admin Console)
```
tag:ai-gpu    → can reach tag:ai-infra (all ports)
tag:ai-worker → can reach tag:ai-infra (all ports)
tag:ai-worker → can reach tag:ai-gpu (port 11434 only — Ollama)
tag:ai-gpu    → can reach tag:ai-worker (all ports)
tag:ai-infra  → can reach tag:ai-infra (all ports)
```

## Docker Networking
- Use `network_mode: service:tailscale-sidecar` for containers that need Tailscale access
- Use internal Docker bridge network for containers on the same host
- cloudflared container runs on Local Server only
