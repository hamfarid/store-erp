=================================================================================
PROJECT TEMPLATES - ERP, Web, AI, ML
=================================================================================

Version: 5.0.0
Type: Templates

Comprehensive project templates for rapid development.

=================================================================================
AVAILABLE TEMPLATES
=================================================================================

1. **ERP System** - Enterprise Resource Planning
2. **Web Page** - Simple static website
3. **Web Page with Login** - Web application with authentication
4. **ML Template** - Machine Learning project
5. **Test Template** - Testing framework setup
6. **Email Template** - Email templates and sending
7. **AI Assistant** - AI-powered chatbot/assistant
8. **Charity Management** - Donation and beneficiary management
9. **AI Prediction** - Forecasting and prediction system

=================================================================================
USING TEMPLATES
=================================================================================

## Command Line

```bash
# List all templates
python3 tools/template_generator.py --list

# Interactive mode
python3 tools/template_generator.py --interactive

# Generate specific template
python3 tools/template_generator.py --template erp_system --output my-erp
```

## Programmatic Usage

```python
from tools.template_generator import TemplateGenerator

generator = TemplateGenerator()

# List templates
templates = generator.list_templates()

# Generate template
generator.generate_template(
    template_name="erp_system",
    output_dir="my-erp",
    variables={
        "project_name": "My ERP",
        "database_name": "my_erp_db",
        "frontend_port": 3000,
        "backend_port": 8000
    }
)
```

=================================================================================
TEMPLATE CUSTOMIZATION
=================================================================================

Each template supports these variables:

- `{PROJECT_NAME}` - Project display name
- `{project_name}` - Project slug (lowercase, underscores)
- `{DATABASE_NAME}` - Database name
- `{FRONTEND_PORT}` - Frontend port number
- `{BACKEND_PORT}` - Backend API port number
- `{DB_PORT}` - Database port number
- `{HOST}` - Host/domain name

=================================================================================
TEMPLATE DETAILS
=================================================================================

## 1. ERP System

**Features:**
- Inventory management
- Sales & purchases
- Accounting
- HR management
- Reporting

**Tech Stack:**
- Backend: Django/FastAPI
- Frontend: React
- Database: PostgreSQL
- Cache: Redis

## 2. AI Assistant

**Features:**
- Natural language understanding
- Context-aware responses
- Knowledge base (RAG)
- Multi-turn conversations

**Tech Stack:**
- LangChain
- OpenAI/Claude API
- Vector database (Pinecone/Chroma)
- FastAPI backend

## 3. Charity Management

**Features:**
- Donation processing
- Beneficiary management
- Campaign management
- Volunteer coordination

**Tech Stack:**
- Backend: Django
- Payment: Stripe/PayPal
- Frontend: React
- Database: PostgreSQL

=================================================================================
END OF TEMPLATES PROMPT
=================================================================================
