# MCP Research Quick Reference Cheatsheet

## 🚨 FIRST STEP (ALWAYS)
```bash
date +"%Y-%m-%d"
```
**Verify date before ANY query!**

---

## Priority Order

```
1️⃣  EXA  ──────────────────────────▶  PRIMARY
    └─ get_code_context_exa (FIRST)
    └─ web_search_exa (FALLBACK)

2️⃣  SPECKIT  ──────────────────────▶  APIs ONLY
    └─ speckit_search
    └─ speckit_get_spec
    └─ speckit_validate

3️⃣  REF  ──────────────────────────▶  LAST RESORT
    └─ ref_search_documentation ✅
    └─ ref_read_url ✅
    └─ search_docs ❌ NEVER
    └─ my_docs ❌ NEVER
```

---

## Ref Triggers (need 1+)

| Trigger | Description |
|---------|-------------|
| 👤 | User explicitly requests docs |
| ⚔️ | Exa results contradict |
| 2️⃣ | 2+ failed fix attempts |
| 📅 | Doc drift suspected |

---

## Query Templates

### Exa Code
```
[lib] [ver] [feature] [lang] implementation [year]
```

### Exa Web
```
[topic] [aspect] [ver] [year] best practices
```

### Speckit
```
[service] [API type] [ver]
```

### Ref
```
[lib] [ver] [topic] official documentation
```

---

## Code Comment Format

```python
# Source: [URL]
# Version: [lib ver]
# Accessed: [YYYY-MM-DD]
# Drift: [potential changes]
```

---

## Quick Decision

```
Code question? → Exa get_code_context
API work?      → Speckit search
Docs needed?   → Check triggers → Ref
No results?    → Refine query → Retry Exa
```

---

## ❌ DON'T

- Skip date verification
- Use Ref before Exa
- Use search_docs
- Use my_docs
- Broad unfocused queries
- Omit version numbers

## ✅ DO

- Verify date FIRST
- Start with Exa
- Include versions
- Specific queries
- Document sources
- Multiple small queries
