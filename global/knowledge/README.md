# Global Knowledge Base

> **Purpose:** Store project-wide knowledge, best practices, and guidelines.

**Version:** 1.0
**Last Updated:** 2025-01-16

---

## Directory Structure

```
knowledge/
├── README.md                       # This file
├── 01_osf_framework.md             # OSF decision framework
├── 02_zero_tolerance_rules.md      # Non-negotiable rules
├── 03_frontend_architecture.md     # Frontend guidelines
├── 04_backend_architecture.md      # Backend guidelines
├── 05_testing_strategy.md          # Testing approach
├── 06_security_best_practices.md   # Security guidelines
├── 07_git_workflow.md              # Git workflow
├── 08_deployment_checklist.md      # Deployment checklist
├── core/                           # Core knowledge
│   ├── environment.md              # Environment setup
│   ├── mcp.md                      # MCP tools usage
│   └── memory.md                   # Memory management
└── lessons_learned/                # Archived lessons
```

---

## Quick Reference

### OSF Framework Weights
| Factor | Weight |
|--------|--------|
| Security | 35% |
| Correctness | 20% |
| Reliability | 15% |
| Performance | 10% |
| Maintainability | 10% |
| Scalability | 10% |

### Zero Tolerance Rules
1. ❌ No hardcoded secrets
2. ❌ No SQL injection
3. ❌ No XSS vulnerabilities
4. ❌ No unhandled errors
5. ❌ No missing tests (80%+ coverage)

---

## Usage

1. **Before implementing** - Check relevant knowledge files
2. **During development** - Follow best practices
3. **After issues** - Update lessons learned

---

## Related Files

- `global/errors/` - Error tracking
- `docs/` - Project documentation
- `.memory/` - AI memory system
