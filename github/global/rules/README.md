# Rules — Global System v26.0.2 Diamond 32

> Mandatory rules enforced across all agents and workflows.

## Iron Rules (Priority 0)
- `00-iron-rules.md` — Non-negotiable system rules
- `01-coding-standards.md` — Code quality standards
- `99-anti-hallucination.md` — Anti-hallucination protocol

## Security
- `security.md` — Core security rules
- `security-policy.md` — Security policies
- `security_protocols.md` — Security protocols
- `mcp-security.md` — MCP security
- `data-privacy-gdpr.md` — GDPR compliance

## Development
- `RULES-mcp-usage.md` — MCP tool usage
- `RULES-context-engineering.md` — Context engineering
- `coding.md` — Coding practices
- `testing.md` — Testing requirements
- `dependency-management.md` — Dependency rules
- `safe-updates.md` — Safe update policy

## Operations
- `memory.md` — Memory management
- `error-handling.md` — Error handling
- `performance.md` — Performance rules
- `rate-limiting.md` — Rate limiting

## ML Rules (in `ml/`)
$(ls rules/ml/*.md 2>/dev/null | while read f; do echo "- \`ml/$(basename $f)\`"; done)
