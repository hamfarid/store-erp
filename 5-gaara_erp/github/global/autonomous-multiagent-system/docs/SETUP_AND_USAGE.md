# 🚀 Setup and Usage Guide

Complete guide for setting up and using the Autonomous Multi-Agent System.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Basic Usage](#basic-usage)
5. [Advanced Usage](#advanced-usage)
6. [Workflow Details](#workflow-details)
7. [Memory Management](#memory-management)
8. [Error Tracking](#error-tracking)
9. [Helper System](#helper-system)
10. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Required

- **Python 3.11+**
- **pip** (Python package manager)
- **Git**

### API Keys Required

You need API keys for all three AI services:

1. **Google Gemini** (Primary - Unlimited)
   - Sign up: https://ai.google.dev/
   - Get API key from Google AI Studio
   - Free tier available

2. **Anthropic Claude** (Secondary - Limited)
   - Sign up: https://www.anthropic.com/
   - Get API key from Console
   - Pay-as-you-go pricing

3. **OpenAI ChatGPT** (Consultant - Very Limited)
   - Sign up: https://platform.openai.com/
   - Get API key from API Keys page
   - Pay-as-you-go pricing

### Recommended

- **VS Code** (for development)
- **pytest** (for testing)
- **Global Guidelines v10.3.0** (for best practices)

---

## 2. Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/hamfarid/autonomous-multiagent-system.git
cd autonomous-multiagent-system
```

### Step 2: Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import google.genai; import anthropic; import openai; print('✅ All packages installed!')"
```

---

## 3. Configuration

### Step 1: Create Environment File

```bash
cp .env.example .env
```

### Step 2: Add API Keys

Edit `.env`:

```env
# Google Gemini API Key
GEMINI_API_KEY=AIza...your_key_here

# Anthropic Claude API Key
ANTHROPIC_API_KEY=sk-ant-...your_key_here

# OpenAI ChatGPT API Key
OPENAI_API_KEY=sk-...your_key_here
OPENAI_API_BASE=https://api.openai.com/v1
```

### Step 3: Test Configuration

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("Gemini:", "✅" if os.getenv('GEMINI_API_KEY') else "❌")
print("Claude:", "✅" if os.getenv('ANTHROPIC_API_KEY') else "❌")
print("ChatGPT:", "✅" if os.getenv('OPENAI_API_KEY') else "❌")
```

### Step 4: Initialize Global Directories

```bash
# Create global directories
mkdir -p ~/.global/memory
mkdir -p ~/.global/mcp
mkdir -p ~/.global/errors/do_not_make_this_error_again
mkdir -p ~/.global/helpers/{definitions,errors,imports,classes,modules}

echo "✅ Global directories created"
```

---

## 4. Basic Usage

### Example 1: Simple Function

```python
from src.orchestrator import AutonomousOrchestrator

# Create orchestrator
orchestrator = AutonomousOrchestrator("email-validator")

# Define requirement
requirement = "Build a function to validate email addresses with tests"

# Run (no consultation for simple projects)
result = orchestrator.run(requirement, consult_on_architecture=False)

# Check result
if result["success"]:
    print("✅ Success!")
    print(f"Code: {result['result']['code']}")
    print(f"Tests: {result['result']['tests']}")
else:
    print(f"❌ Failed: {result['error']}")
```

### Example 2: REST API

```python
from src.orchestrator import AutonomousOrchestrator

# Create orchestrator
orchestrator = AutonomousOrchestrator("todo-api")

# Define requirement
requirement = """
Build a REST API for a todo list application:
- Create, read, update, delete todos
- SQLite database
- Flask framework
- 95%+ test coverage
"""

# Run (no consultation for standard projects)
result = orchestrator.run(requirement, consult_on_architecture=False)
```

---

## 5. Advanced Usage

### Example 3: Complex System (with Consultation)

```python
from src.orchestrator import AutonomousOrchestrator

# Create orchestrator
orchestrator = AutonomousOrchestrator("distributed-system")

# Define complex requirement
requirement = """
Build a distributed microservices system for e-commerce:

1. User Service (authentication, profiles)
2. Product Service (catalog, inventory)
3. Order Service (cart, checkout, orders)
4. Payment Service (Stripe integration)

Requirements:
- Microservices architecture
- REST APIs with OpenAPI
- PostgreSQL databases
- Redis caching
- RabbitMQ message queue
- Docker containers
- Kubernetes deployment
- 95%+ test coverage
- Complete documentation

Technology Stack:
- Python (Flask)
- PostgreSQL
- Redis
- RabbitMQ
- Docker
- Kubernetes
"""

# Run with consultation (complex project)
result = orchestrator.run(
    requirement=requirement,
    consult_on_architecture=True  # ChatGPT will review architecture
)

# Save results
if result["success"]:
    # Save files
    import os
    os.makedirs("output", exist_ok=True)
    
    with open("output/code.py", "w") as f:
        f.write(result["result"]["code"])
    
    with open("output/tests.py", "w") as f:
        f.write(result["result"]["tests"])
    
    with open("output/README.md", "w") as f:
        f.write(result["result"]["documentation"])
    
    print("✅ Files saved to output/")
```

### Accessing Memory

```python
from src.memory_manager import MemoryManager

# Load project memory
memory = MemoryManager("distributed-system")

# Get all context
context = memory.get_all_context()
print(context.keys())

# Get specific memory
architecture = memory.load("architecture")
decisions = memory.load("decisions")
progress = memory.load("progress")

print(f"Architecture:\n{architecture}")
print(f"Decisions:\n{decisions}")
print(f"Progress:\n{progress}")
```

### Checking Past Errors

```python
from src.error_tracker import ErrorTracker

# Load error tracker
tracker = ErrorTracker()

# Get past errors for project
errors = tracker.get_past_errors("distributed-system")

for error in errors:
    print(f"Error #{error['id']}: {error['name']}")
    print(f"  Description: {error['description']}")
    print(f"  Solution: {error['solution']}")
    print()

# Get statistics
stats = tracker.get_stats()
print(f"Total errors: {stats['total_errors']}")
print(f"By project: {stats['errors_by_project']}")
```

---

## 6. Workflow Details

### Phase 0: Initialize

**What happens:**
- Memory is initialized for the project
- Past errors are loaded
- Helper files are loaded
- MCP is configured

**Output:**
- `~/.global/memory/[project]/context.md`
- `~/.global/memory/[project]/past_errors.md`
- `~/.global/memory/[project]/helpers_available.md`

### Phase 1: Understand

**Agent:** Lead (Gemini)

**What happens:**
- Analyzes the requirement
- Identifies scope and features
- Lists technical considerations
- Asks clarification questions (if needed)

**Output:**
- `~/.global/memory/[project]/requirement.md`
- `~/.global/memory/[project]/understanding.md`

### Phase 2: Plan

**Agents:** Lead (Gemini) + Consultant (ChatGPT, if complex)

**What happens:**
- Designs system architecture
- Chooses technology stack
- Defines key components
- Makes architectural decisions
- Gets strategic review (if complex)

**Output:**
- `~/.global/memory/[project]/architecture.md`
- `~/.global/memory/[project]/decisions.md`

### Phase 3: Code

**Agent:** Lead (Gemini)

**What happens:**
- Writes production-ready code
- Follows best practices
- Uses helper files
- Adds proper documentation
- Implements error handling

**Output:**
- `~/.global/memory/[project]/code.md`

### Phase 4: Review

**Agents:** Reviewer (Claude) + Lead (Gemini, if fixes needed)

**What happens:**
- Reviews code quality
- Identifies bugs and issues
- Suggests improvements
- Lead fixes issues if needed
- Re-reviews until approved

**Output:**
- `~/.global/memory/[project]/reviews.md`
- Updated code (if fixed)

### Phase 5: Test

**Agents:** Reviewer (Claude) + Lead (Gemini, if fixes needed)

**What happens:**
- Writes comprehensive tests
- Runs tests automatically
- Lead fixes failures
- Re-runs until all pass
- Verifies 95%+ coverage

**Output:**
- `~/.global/memory/[project]/tests.md`
- `~/.global/memory/[project]/test_output.md`

### Phase 6: Finalize

**Agent:** Lead (Gemini)

**What happens:**
- Writes complete documentation
- Updates Memory with final status
- Returns complete result

**Output:**
- `~/.global/memory/[project]/documentation.md`
- `~/.global/memory/[project]/status.md` (Complete)

---

## 7. Memory Management

### Memory Structure

```
~/.global/memory/[project-name]/
├── context.md              # Project overview
├── requirement.md          # Original requirement
├── understanding.md        # Requirement analysis
├── architecture.md         # System design
├── decisions.md            # Architectural decisions
├── preferences.md          # Development preferences
├── code.md                 # Generated code
├── reviews.md              # Code reviews
├── tests.md                # Test code
├── test_output.md          # Test results
├── documentation.md        # Documentation
├── progress.md             # Project progress
├── agents_log.md           # Agent interactions
└── status.md               # Current status
```

### Manual Memory Operations

```python
from src.memory_manager import MemoryManager

memory = MemoryManager("my-project")

# Save
memory.save("custom_key", "custom content")

# Load
content = memory.load("custom_key")

# Append
memory.append("progress", "New milestone reached")

# Save JSON
memory.save_json("config", {"setting": "value"})

# Load JSON
config = memory.load_json("config")

# Get all
all_context = memory.get_all_context()
```

---

## 8. Error Tracking

### Error Structure

```
~/.global/errors/
├── do_not_make_this_error_again/
│   ├── 001_jwt_token_expiry.md
│   ├── 002_database_connection_pool.md
│   └── ...
├── error_log.json
└── error_stats.json
```

### Logging Errors

```python
from src.error_tracker import ErrorTracker

tracker = ErrorTracker()

# Log an error
tracker.log_error({
    "name": "sql_injection_vulnerability",
    "project": "my-api",
    "agent": "lead",
    "description": "SQL query used string concatenation",
    "solution": "Used parameterized queries instead",
    "severity": "high",
    "code_snippet": "query = f'SELECT * FROM users WHERE id={user_id}'",
    "fix_snippet": "query = 'SELECT * FROM users WHERE id=?'\ncursor.execute(query, (user_id,))",
    "how_to_avoid": "Always use parameterized queries for SQL",
    "tags": ["security", "sql", "injection"]
})
```

### Viewing Errors

```python
# Get past errors
errors = tracker.get_past_errors("my-api")

# Get summary
summary = tracker.get_error_summary("my-api")
print(summary)

# Get statistics
stats = tracker.get_stats()
print(f"Total: {stats['total_errors']}")
print(f"By project: {stats['errors_by_project']}")
print(f"By agent: {stats['errors_by_agent']}")
```

---

## 9. Helper System

### Helper Structure

```
~/.global/helpers/
├── definitions/            # Type definitions, enums
├── errors/                 # Custom error classes
├── imports/                # Common imports
├── classes/                # Base classes
└── modules/                # Utility functions
```

### Using Helpers

```python
from src.helper_manager import HelperManager

helper = HelperManager()

# Get all helpers
helpers = helper.get_all_helpers()

# Get specific type
definitions = helper.get_definitions()
error_classes = helper.get_error_classes()
imports = helper.get_imports()
base_classes = helper.get_base_classes()
modules = helper.get_utility_modules()

# Add new helper
helper.add_definition("email_regex", """
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
""")

# Get summary
print(helper.get_helper_summary())
```

---

## 10. Troubleshooting

### Problem: "API key not found"

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"

# Reload environment
source venv/bin/activate
```

### Problem: "Agent failed to execute"

**Solution:**
```python
# Check API quotas
# Gemini: https://console.cloud.google.com/
# Claude: https://console.anthropic.com/
# ChatGPT: https://platform.openai.com/usage

# Test API directly
from google import genai
client = genai.Client(api_key="your_key")
response = client.models.generate_content(model="gemini-2.0-flash-exp", contents="test")
print(response.text)
```

### Problem: "Tests failed"

**Solution:**
The system automatically fixes test failures. If it fails repeatedly:

```python
# Check test output
memory = MemoryManager("project-name")
test_output = memory.load("test_output")
print(test_output)

# Check error logs
tracker = ErrorTracker()
errors = tracker.get_past_errors("project-name")
for error in errors[-5:]:
    print(error)
```

### Problem: "Memory not found"

**Solution:**
```bash
# Check global directories exist
ls -la ~/.global/memory/

# Reinitialize
mkdir -p ~/.global/memory/[project-name]

# Or recreate
from src.memory_manager import MemoryManager
memory = MemoryManager("project-name")
```

### Problem: "Import errors"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.11+

# Check imports
python -c "from src.orchestrator import AutonomousOrchestrator; print('✅')"
```

---

## 📚 Additional Resources

- **README.md** - Overview and quick start
- **Architecture Design** - `docs/ARCHITECTURE.md`
- **API Reference** - `docs/API_REFERENCE.md`
- **Examples** - `examples/` directory

---

**Version:** 1.0.0  
**Date:** November 5, 2025  
**Status:** Production Ready

🚀 **Happy Autonomous Coding!** 🚀

