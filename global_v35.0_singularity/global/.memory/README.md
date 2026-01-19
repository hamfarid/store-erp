# AI Memory System - Local Storage

This directory contains the AI memory system's local storage. **Do not commit this to Git.**

## Directory Structure

```
.memory/
├── conversations/     # Conversation history (JSON files)
├── knowledge/         # Semantic knowledge base (JSON files)
├── preferences/       # User preferences and settings
├── state/             # Current state and context
├── checkpoints/       # State checkpoints for recovery
└── vectors/           # Vector database for semantic search
```

## Usage

### Conversations
Stores conversation history with timestamps and metadata.

**Format:**
```json
{
  "timestamp": "2025-11-03T10:30:00Z",
  "user_id": "user123",
  "conversation_id": "conv_001",
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "context": {
    "project": "ecommerce",
    "task": "authentication"
  }
}
```

### Knowledge
Stores semantic knowledge and facts.

**Format:**
```json
{
  "id": "know_001",
  "type": "semantic",
  "content": "User prefers PostgreSQL for this project",
  "importance": 8,
  "metadata": {
    "category": "preference",
    "project": "ecommerce"
  },
  "created_at": "2025-11-03T10:30:00Z"
}
```

### Preferences
Stores user preferences and settings.

**Format:**
```json
{
  "user_id": "user123",
  "preferences": {
    "language": "python",
    "style": "functional",
    "database": "postgresql",
    "testing": "pytest"
  },
  "updated_at": "2025-11-03T10:30:00Z"
}
```

### State
Stores current context and state.

**Format:**
```json
{
  "user_id": "user123",
  "current_project": "ecommerce",
  "current_task": "authentication",
  "context": {
    "stack": ["Python", "React", "PostgreSQL"],
    "phase": "implementation"
  },
  "updated_at": "2025-11-03T10:30:00Z"
}
```

### Checkpoints
Stores state checkpoints for recovery.

**Format:**
```json
{
  "checkpoint_id": "cp_001",
  "name": "after_auth_implementation",
  "timestamp": "2025-11-03T10:30:00Z",
  "state": {
    "project": "ecommerce",
    "progress": 0.75,
    "completed_tasks": [...]
  }
}
```

### Vectors
Contains ChromaDB vector database files for semantic search.

## Security

- ⚠️ **Never commit this directory to Git**
- ✅ Already added to `.gitignore`
- ✅ Contains user-specific data only
- ✅ No sensitive credentials (use `.env` for that)

## Maintenance

### Cleanup Old Data

```bash
# Remove conversations older than 90 days
find .memory/conversations/ -name "*.json" -mtime +90 -delete

# Remove old checkpoints (keep last 10)
ls -t .memory/checkpoints/*.json | tail -n +11 | xargs rm -f
```

### Backup

```bash
# Create backup
tar -czf memory_backup_$(date +%Y%m%d).tar.gz .memory/

# Restore from backup
tar -xzf memory_backup_YYYYMMDD.tar.gz
```

## Database Setup

### PostgreSQL

```sql
-- Create database
CREATE DATABASE ai_memory;

-- Connect to database
\c ai_memory

-- Create tables (see Module 60 for schema)
```

### Redis

```bash
# Start Redis
redis-server --daemonize yes

# Connect
redis-cli
```

### ChromaDB

```python
from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=".memory/vectors"
))
```

## See Also

- **Module 60:** Memory Management & Context Retention
- **Documentation:** prompts/60_memory_management.txt
- **Examples:** See Module 60, Section 6

