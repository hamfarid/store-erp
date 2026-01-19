# Nginx Reverse Proxy Configuration

This configuration sets up an Nginx reverse proxy for all projects with port forwarding.

## Port Mapping Table

| Project # | Project Name | Backend | Frontend | Database | ML | AI |
|-----------|--------------|---------|----------|----------|----|----|
| 1 | test_projects | 1001 | 1501 | 2502 | 1101 | 1601 |
| 2 | gold-price-predictor | 2001 | 2501 | 4502 | 2101 | 2601 |
| 3 | Zakat | 3001 | 3501 | 6502 | 3101 | 3601 |
| 4 | scan_ai-Manus | 4001 | 4501 | 8502 | 4101 | 4601 |
| 5 | gaara_erp | 5001 | 5501 | 10502 | 5101 | 5601 |
| 6 | store | 6001 | 6501 | 12502 | 6101 | 6601 |

## Setup Instructions

### 1. Start Nginx Proxy
```bash
docker-compose -f docker-compose.nginx.yml up -d
```

### 2. View Logs
```bash
docker logs nginx-proxy -f
```

### 3. Stop Nginx Proxy
```bash
docker-compose -f docker-compose.nginx.yml down
```

### 4. Reload Configuration (without downtime)
```bash
docker exec nginx-proxy nginx -s reload
```

## Network Requirements

Each project must be in its own Docker network:
- `test_projects_network`
- `gold_predictor_network`
- `zakat_network`
- `scan_ai_network`
- `gaara_erp_network`
- `store_network`

### Create Networks
```bash
docker network create test_projects_network
docker network create gold_predictor_network
docker network create zakat_network
docker network create scan_ai_network
docker network create gaara_erp_network
docker network create store_network
```

## Container Naming Convention

Containers must follow this naming pattern:
- `{project-name}-backend`
- `{project-name}-frontend`
- `{project-name}-database`
- `{project-name}-ml`
- `{project-name}-ai`

## Configuration Files

- `nginx/nginx.conf` - Main Nginx configuration
- `nginx/conf.d/*.conf` - Individual project configurations
- `docker-compose.nginx.yml` - Docker Compose for Nginx

## SSL Configuration (Optional)

To add SSL certificates, place them in `nginx/ssl/` and update the server blocks in the configuration files.

## Troubleshooting

### Check Nginx Configuration
```bash
docker exec nginx-proxy nginx -t
```

### View Error Logs
```bash
docker exec nginx-proxy cat /var/log/nginx/error.log
```

### View Access Logs
```bash
docker exec nginx-proxy cat /var/log/nginx/access.log
```
