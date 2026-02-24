# Examples — Global System v26.0.2 Diamond 32

> Working examples demonstrating system patterns and implementations.

## General Examples
$(for f in $(find examples -maxdepth 1 -name "*.md" -type f ! -name "README.md" | sort); do
    title=$(head -1 "$f" | sed 's/^# //')
    echo "- \`$(basename $f)\` — $title"
done)

## Domain Examples
| Directory | Contents |
|-----------|----------|
| `backend/` | Backend service examples |
| `database/` | Database patterns |
| `frontend/` | Frontend component examples |
| `rag/` | RAG pipeline examples |
| `security/` | Security implementation examples |
| `testing/` | Test suite examples |

## ML Examples (in `ml/`)
$(for f in $(find examples/ml -name "*.md" -type f | sort); do
    echo "- \`ml/$(basename $f)\`"
done)
