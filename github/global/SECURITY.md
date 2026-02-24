# Security Policy — Global System v26.0.2 Diamond 32

## Supported Versions

| Version | Supported |
|---------|-----------|
| v26.0.2 (Diamond 32) | ✅ Active |
| v26.0.1 (Diamond 31) | ⚠️ Critical fixes only |
| < v26.0.1 | ❌ End of life |

## Reporting a Vulnerability

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. Email: security@gaara-group.com
3. Include: description, reproduction steps, affected files, severity estimate
4. Expected response time: 48 hours

## Security Standards

This system enforces:
- Input validation on all external data (see `rules/security.md`)
- No secrets in source code (enforced by `.gitignore` and `tools/security_scan.py`)
- OWASP LLM Top 10 compliance (see `knowledge/technical/owasp_llm_2025.md`)
- Dependency audit before each release
- Container image scanning via Trivy (see `infrastructure/iac/trivy.yaml`)

## Security-Related Files
- `rules/security.md` — Core security rules
- `rules/security-policy.md` — Detailed security policies
- `rules/security_protocols.md` — Security protocols
- `rules/data-privacy-gdpr.md` — GDPR compliance
- `rules/mcp-security.md` — MCP security rules
- `docs/SECURITY_GUIDELINES.md` — Security guidelines
- `tools/security_scan.py` — Automated security scanner
- `knowledge/technical/owasp_llm_2025.md` — OWASP LLM reference
