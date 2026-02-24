# GUIDE-tailscale-cloudflare-networking.md
# Governance: ML/AI Application Framework (Feb 2026)

## 1. Architecture: Dual-Layer Networking

GAARA-AI uses two complementary networking layers:
- **Tailscale** = Internal mesh VPN (server-to-server, encrypted P2P)
- **Cloudflare Tunnel** = External gateway (internet-facing services, DDoS/WAF)

### Why Not WireGuard Directly?
| Aspect | WireGuard (Manual) | Tailscale + Cloudflare |
|--------|-------------------|----------------------|
| Setup | Generate keys per node, edit configs | `tailscale up` (1 command) |
| NAT Traversal | Fails behind Double NAT | Automatic (>90% direct P2P) |
| DNS | Manual /etc/hosts | MagicDNS (gpu-pc, vps1...) |
| Add new node | Edit ALL existing configs | `tailscale up` on new node only |
| HTTPS exposure | Nginx + Let's Encrypt + certs | Cloudflare auto HTTPS + DDoS + WAF |
| Access control | iptables rules | JSON ACLs + Zero Trust policies |
| Cost | Free | Free (Personal: 100 devices) |

## 2. Tailscale Setup (Internal Mesh)

### 2.1 Install on Each Server
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

### 2.2 Authenticate Each Node
```bash
# GPU PC (has browser)
tailscale up --hostname=gpu-pc --advertise-tags=tag:ai-gpu

# VPS #1 (headless — use auth key)
tailscale up --hostname=vps1 --advertise-tags=tag:ai-worker \
  --authkey=tskey-auth-xxxxx

# VPS #2
tailscale up --hostname=vps2 --advertise-tags=tag:ai-worker \
  --authkey=tskey-auth-xxxxx

# Local Server (subnet router for LAN access)
tailscale up --hostname=local-server --advertise-tags=tag:ai-infra \
  --advertise-routes=192.168.1.0/24 --authkey=tskey-auth-xxxxx
```

### 2.3 Auth Keys
Generate at: **Tailscale Admin → Settings → Keys → Generate auth key**
- Check "Reusable" for automation
- Check "Ephemeral" for temporary/CI nodes
- Set expiry (90 days recommended, rotate via Celery scheduled task)

### 2.4 MagicDNS
After setup, nodes resolve by hostname automatically:
```bash
ping gpu-pc        # → 100.x.x.1
ping vps1          # → 100.x.x.2
ssh vps2           # → 100.x.x.3
curl http://local-server:8000/health  # Works!
```

### 2.5 ACLs (Access Control Lists)
Configure in **Tailscale Admin → Access Controls**:
```json
{
  "tagOwners": {
    "tag:ai-gpu": ["autogroup:admin"],
    "tag:ai-worker": ["autogroup:admin"],
    "tag:ai-infra": ["autogroup:admin"]
  },
  "acls": [
    {"action": "accept", "src": ["tag:ai-gpu", "tag:ai-worker"],
     "dst": ["tag:ai-infra:*"]},
    {"action": "accept", "src": ["tag:ai-gpu"],
     "dst": ["tag:ai-worker:*"]},
    {"action": "accept", "src": ["tag:ai-worker"],
     "dst": ["tag:ai-gpu:11434"]},
    {"action": "accept", "src": ["tag:ai-infra"],
     "dst": ["tag:ai-infra:*"]}
  ]
}
```

### 2.6 Tailscale in Docker (Sidecar Pattern)
```yaml
tailscale:
  image: tailscale/tailscale:stable
  container_name: gaara-tailscale
  hostname: local-server
  cap_add: [NET_ADMIN, SYS_MODULE]
  environment:
    - TS_AUTHKEY=${TAILSCALE_AUTHKEY}
    - TS_STATE_DIR=/var/lib/tailscale
    - TS_EXTRA_ARGS=--advertise-tags=tag:ai-infra
    - TS_USERSPACE=false
  volumes:
    - tailscale_data:/var/lib/tailscale
    - /dev/net/tun:/dev/net/tun
  restart: unless-stopped
```

### 2.7 Tailscale SSH (Optional — No SSH Keys)
```bash
# Enable on target server
tailscale up --ssh

# Connect from any Tailscale node
tailscale ssh gpu-pc  # Authenticated via Tailscale identity
```

## 3. Cloudflare Tunnel Setup (External Access)

### 3.1 Create Tunnel
1. Go to **dash.teams.cloudflare.com** → Access → Tunnels
2. Click **Create Tunnel** → name: `gaara-ai-tunnel`
3. Copy the **Token** (starts with `eyJh...`)

### 3.2 Docker Container
```yaml
cloudflared:
  image: cloudflare/cloudflared:latest
  container_name: gaara-cloudflared
  command: tunnel --no-autoupdate run
  environment:
    - TUNNEL_TOKEN=${CLOUDFLARE_TUNNEL_TOKEN}
  restart: unless-stopped
  networks:
    - gaara-net
```

### 3.3 Configure Public Hostnames (in Cloudflare Dashboard)
| Subdomain | Service | Port |
|-----------|---------|------|
| ai.gaara.com | http://api-gateway:8000 | API Gateway |
| erp.gaara.com | http://localhost:8080 | Django ERP |
| flower.gaara.com | http://flower:5555 | Celery Monitor |
| grafana.gaara.com | http://grafana:3000 | Dashboards |

### 3.4 Zero Trust Access Policies
In **Cloudflare Zero Trust → Applications → Add**:
- Application: `ai.gaara.com`
- Policy: Allow
- Authentication: Email domain `@gaara.com` OR One-time PIN
- Session duration: 24 hours

### 3.5 Benefits Over Nginx + Let's Encrypt
- **No open ports**: Tunnel is outbound-only (server → Cloudflare)
- **Auto HTTPS**: TLS certificates managed by Cloudflare
- **DDoS protection**: Cloudflare edge absorbs attacks
- **WAF firewall**: Blocks SQL injection, XSS, bot attacks
- **CDN caching**: Static assets cached at edge
- **Zero Trust**: Identity-based access, not IP-based

## 4. Service Communication Patterns

### 4.1 Internal (via Tailscale)
```python
# From worker on VPS → Ollama on GPU PC
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://gpu-pc:11434/api/generate",  # MagicDNS name
        json={"model": "qwen2.5:7b", "prompt": "..."}
    )
```

### 4.2 External (via Cloudflare Tunnel)
```javascript
// From browser/mobile → API Gateway
const response = await fetch("https://ai.gaara.com/api/v1/plant/diagnose", {
    method: "POST",
    headers: { "Authorization": "Bearer jwt_token" },
    body: formData  // image upload
});
```

## 5. Security Checklist

- [ ] Tailscale ACLs configured (least privilege)
- [ ] Auth keys rotated every 90 days
- [ ] Cloudflare Access policies set for all public hostnames
- [ ] Tunnel token stored in .env (not committed to git)
- [ ] MFA enabled on Tailscale admin account
- [ ] MFA enabled on Cloudflare account
- [ ] Firewall: only Tailscale (UDP) + Cloudflare Tunnel (outbound 443) allowed
- [ ] No services exposed on public IPs directly
