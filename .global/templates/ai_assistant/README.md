# AI Assistant Template

**Intelligent AI-powered assistant application**

---

## 📋 Overview

Complete AI assistant system with:
- **Natural Language Processing** - Understand user queries
- **Knowledge Base** - Store and retrieve information
- **Chat Interface** - Interactive conversations
- **Multi-model Support** - GPT, Claude, Gemini, etc.
- **Context Awareness** - Remember conversation history
- **Custom Training** - Train on your data

---

## 🏗️ Architecture

### Frontend
- **Framework:** React 18 + TypeScript
- **UI:** Tailwind CSS + Headless UI
- **Chat UI:** Custom chat components
- **State:** Zustand
- **Real-time:** WebSocket

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **AI Integration:** LangChain
- **Vector DB:** Pinecone / Chroma
- **LLM:** OpenAI GPT-4, Anthropic Claude
- **Embeddings:** OpenAI Ada-002
- **Cache:** Redis

### Database
- **Primary:** PostgreSQL (conversations, users)
- **Vector:** Pinecone / Chroma (knowledge base)
- **Cache:** Redis (sessions, responses)

---

## 🚀 Features

### Core Features

✅ **Chat Interface**
- Clean, modern UI
- Markdown support
- Code highlighting
- File attachments
- Voice input (optional)

✅ **AI Capabilities**
- Natural language understanding
- Context-aware responses
- Multi-turn conversations
- Function calling
- Streaming responses

✅ **Knowledge Base**
- Document upload (PDF, DOCX, TXT)
- Web scraping
- Vector search
- Semantic retrieval
- Source citations

✅ **User Management**
- Authentication (JWT)
- Conversation history
- User preferences
- Usage tracking

✅ **Admin Panel**
- User management
- Analytics dashboard
- Model configuration
- Knowledge base management

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- OpenAI API key (or other LLM provider)

### Installation

```bash
# 1. Generate from template
python3 ../../tools/template_generator.py \
  --template ai_assistant \
  --output ~/projects/my-ai-assistant

# 2. Navigate
cd ~/projects/my-ai-assistant

# 3. Configure environment
cp .env.example .env
# Add your API keys:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# 4. Start with Docker
docker-compose up -d

# 5. Run migrations
docker-compose exec backend alembic upgrade head

# 6. Create admin user
docker-compose exec backend python scripts/create_admin.py

# 7. Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Admin: http://localhost:3000/admin
```

---

## 📁 Structure

```
ai_assistant/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   │   ├── ChatInput.tsx
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   └── ChatHistory.tsx
│   │   │   ├── Knowledge/
│   │   │   └── Admin/
│   │   ├── pages/
│   │   │   ├── ChatPage.tsx
│   │   │   ├── KnowledgePage.tsx
│   │   │   └── AdminPage.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── websocket.ts
│   │   │   └── auth.ts
│   │   └── store/
│   │       ├── chatStore.ts
│   │       └── authStore.ts
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── llm.py          # LLM integration
│   │   │   ├── embeddings.py   # Embeddings
│   │   │   ├── chains.py       # LangChain chains
│   │   │   └── prompts.py      # Prompt templates
│   │   ├── chat/
│   │   │   ├── routes.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── knowledge/
│   │   │   ├── routes.py
│   │   │   ├── ingestion.py    # Document processing
│   │   │   ├── retrieval.py    # Vector search
│   │   │   └── storage.py      # Vector DB
│   │   ├── auth/
│   │   ├── admin/
│   │   └── config/
│   │       ├── settings.py
│   │       └── database.py
│   ├── models/              # Saved AI models
│   ├── requirements.txt
│   └── main.py
├── database/
│   └── migrations/
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── docker-compose.yml
├── tests/
│   ├── test_chat.py
│   ├── test_knowledge.py
│   └── test_ai.py
├── docs/
│   ├── setup.md
│   ├── api.md
│   ├── ai_models.md
│   └── deployment.md
├── .env.example
├── config.json
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

```env
# Project
PROJECT_NAME={{PROJECT_NAME}}

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Database
DATABASE_URL=postgresql://user:pass@db:5432/{{DATABASE_NAME}}
REDIS_URL=redis://redis:6379/0

# Vector Database
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
# OR
CHROMA_PERSIST_DIRECTORY=./chroma_db

# AI Configuration
DEFAULT_LLM=gpt-4
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=2000
EMBEDDING_MODEL=text-embedding-ada-002

# Features
ENABLE_VOICE_INPUT=false
ENABLE_FILE_UPLOAD=true
ENABLE_WEB_SCRAPING=true
MAX_CONVERSATION_LENGTH=50

# Ports
FRONTEND_PORT={{FRONTEND_PORT}}
BACKEND_PORT={{BACKEND_PORT}}
```

### config.json

```json
{
  "template_name": "ai_assistant",
  "version": "1.0.0",
  "ai_models": {
    "llm": {
      "provider": "openai",
      "model": "gpt-4",
      "temperature": 0.7,
      "max_tokens": 2000
    },
    "embeddings": {
      "provider": "openai",
      "model": "text-embedding-ada-002"
    },
    "vector_db": {
      "provider": "pinecone",
      "index_name": "ai-assistant"
    }
  },
  "features": {
    "chat": true,
    "knowledge_base": true,
    "voice_input": false,
    "file_upload": true,
    "web_scraping": true,
    "function_calling": true,
    "streaming": true
  }
}
```

---

## 💬 Chat Features

### Message Types

- **Text messages** - Standard chat
- **Code blocks** - Syntax highlighted
- **Tables** - Formatted tables
- **Lists** - Bullet/numbered lists
- **Links** - Clickable links
- **Images** - Inline images
- **Files** - File attachments

### AI Capabilities

- **Question answering** - Get answers
- **Code generation** - Generate code
- **Summarization** - Summarize text
- **Translation** - Translate languages
- **Analysis** - Analyze data
- **Creative writing** - Write content

---

## 📚 Knowledge Base

### Document Types

- PDF documents
- Word documents (DOCX)
- Text files (TXT, MD)
- Web pages (URL)
- CSV/Excel data

### Processing Pipeline

1. **Upload** - User uploads document
2. **Extract** - Extract text content
3. **Chunk** - Split into chunks
4. **Embed** - Generate embeddings
5. **Store** - Save to vector DB
6. **Index** - Create search index

### Retrieval

```python
# Semantic search
results = knowledge_base.search(
    query="How to deploy?",
    top_k=5,
    threshold=0.7
)

# With metadata filtering
results = knowledge_base.search(
    query="pricing",
    filters={"category": "documentation"},
    top_k=3
)
```

---

## 🤖 AI Models

### Supported LLMs

- **OpenAI:** GPT-4, GPT-3.5-turbo
- **Anthropic:** Claude 3 Opus/Sonnet/Haiku
- **Google:** Gemini Pro
- **Open Source:** Llama 2, Mistral

### Switching Models

```python
# In backend/app/ai/llm.py
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key=settings.OPENAI_API_KEY
)
```

---

## 📊 API Endpoints

### Chat

- `POST /api/chat/message` - Send message
- `GET /api/chat/history` - Get history
- `DELETE /api/chat/clear` - Clear history
- `WS /api/chat/stream` - WebSocket streaming

### Knowledge Base

- `POST /api/knowledge/upload` - Upload document
- `GET /api/knowledge/documents` - List documents
- `DELETE /api/knowledge/{id}` - Delete document
- `POST /api/knowledge/search` - Search knowledge

### Admin

- `GET /api/admin/users` - List users
- `GET /api/admin/analytics` - Analytics
- `PUT /api/admin/config` - Update config

---

## 🧪 Testing

```bash
# Backend tests
docker-compose exec backend pytest

# With coverage
docker-compose exec backend pytest --cov=app

# Frontend tests
cd frontend
npm test
```

---

## 📈 Deployment

### Production Checklist

- [ ] Set production API keys
- [ ] Configure vector database
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Enable HTTPS
- [ ] Set up backups
- [ ] Configure logging
- [ ] Test all features

---

## 🎨 Customization

### Custom Prompts

Edit `backend/app/ai/prompts.py`:

```python
SYSTEM_PROMPT = """
You are {{PROJECT_NAME}}, an AI assistant specialized in...

Your capabilities:
- Answer questions
- Provide code examples
- Analyze data

Always be helpful and accurate.
"""
```

### Custom UI

Edit `frontend/src/components/Chat/`:

- Change colors in Tailwind config
- Modify chat bubble styles
- Add custom components

---

## ✅ Summary

**Complete AI Assistant** with:

✅ **Modern chat UI** - Clean and responsive  
✅ **Multiple LLMs** - GPT-4, Claude, Gemini  
✅ **Knowledge base** - RAG with vector search  
✅ **Real-time** - WebSocket streaming  
✅ **Admin panel** - Full management  
✅ **Production ready** - Docker, tests, docs

**Build your AI assistant now!** 🤖

---

**Template Version:** 1.0.0  
**Last Updated:** 2025-11-02  
**Status:** ✅ Production Ready

