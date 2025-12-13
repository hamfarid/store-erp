# 🤖 Autonomous Multi-Agent System

**Fully autonomous AI development system** where multiple AI agents work together without human intervention to design, code, review, test, and document software projects.

## 🎯 Overview

This system coordinates three AI agents to work together autonomously:

1. **Lead Agent (Google Gemini)** - Designs architecture and writes code
2. **Reviewer Agent (Anthropic Claude)** - Reviews code and writes tests
3. **Consultant Agent (OpenAI ChatGPT)** - Provides strategic advice

The system integrates with:
- **Memory Manager** - Project-specific memory storage
- **MCP Manager** - Model Context Protocol tools
- **Error Tracker** - Prevents repeating mistakes
- **Helper Manager** - Reusable code components

## ✨ Features

- ✅ **Fully Autonomous** - No human intervention required
- ✅ **Multi-Agent Collaboration** - Agents work together seamlessly
- ✅ **Memory Integration** - Persistent project context
- ✅ **Error Tracking** - Learn from mistakes
- ✅ **Helper System** - Reusable components
- ✅ **MCP Integration** - Extended capabilities
- ✅ **Quality Focus** - Code review + testing (95%+ coverage)
- ✅ **Strategic Consultation** - For complex projects

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/hamfarid/autonomous-multiagent-system.git
cd autonomous-multiagent-system

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Configure API Keys

You need API keys for:
- **Google Gemini** - https://ai.google.dev/
- **Anthropic Claude** - https://www.anthropic.com/
- **OpenAI ChatGPT** - https://platform.openai.com/

Add them to `.env`:

```env
GEMINI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
```

### 3. Run Simple Example

```python
from orchestrator import AutonomousOrchestrator

# Create orchestrator
orchestrator = AutonomousOrchestrator("my-project")

# Define requirement
requirement = "Build a function to validate email addresses"

# Run autonomous workflow
result = orchestrator.run(requirement)

# Get result
if result["success"]:
    print(result["result"]["code"])
    print(result["result"]["tests"])
```

## 📖 Usage

### Simple Project

```python
from orchestrator import AutonomousOrchestrator

orchestrator = AutonomousOrchestrator("email-validator")

requirement = """
Build a Python function to validate email addresses.
Include tests and documentation.
"""

result = orchestrator.run(
    requirement=requirement,
    consult_on_architecture=False  # Simple, no consultation needed
)
```

### Complex Project

```python
from orchestrator import AutonomousOrchestrator

orchestrator = AutonomousOrchestrator("user-auth-api")

requirement = """
Build a RESTful API for user authentication with:
- User registration and login
- JWT tokens
- Password reset
- PostgreSQL database
- 95%+ test coverage
"""

result = orchestrator.run(
    requirement=requirement,
    consult_on_architecture=True  # Complex, consult ChatGPT
)
```

## 🔄 Workflow

The system follows a 7-phase autonomous workflow:

### Phase 0: Initialize
- Initialize Memory and MCP
- Load past errors
- Load helper files

### Phase 1: Understand
- **Lead Agent** analyzes requirement
- Saves understanding to Memory

### Phase 2: Plan
- **Lead Agent** designs architecture
- **Consultant Agent** reviews (if complex)
- Saves plan to Memory

### Phase 3: Code
- **Lead Agent** writes code
- Uses helpers and follows best practices
- Saves code to Memory

### Phase 4: Review
- **Reviewer Agent** reviews code
- **Lead Agent** fixes issues if needed
- Saves review to Memory

### Phase 5: Test
- **Reviewer Agent** writes tests
- System runs tests automatically
- **Lead Agent** fixes failures
- Saves tests to Memory

### Phase 6: Finalize
- **Lead Agent** writes documentation
- Updates Memory with final status
- Returns complete result

## 📁 Project Structure

```
autonomous-multiagent-system/
├── src/
│   ├── orchestrator.py          # Main orchestrator
│   ├── base_agent.py             # Base agent class
│   ├── lead_agent.py             # Lead agent (Gemini)
│   ├── reviewer_agent.py         # Reviewer agent (Claude)
│   ├── consultant_agent.py       # Consultant agent (ChatGPT)
│   ├── memory_manager.py         # Memory management
│   ├── mcp_manager.py            # MCP management
│   ├── error_tracker.py          # Error tracking
│   └── helper_manager.py         # Helper management
├── examples/
│   ├── simple_usage.py           # Simple example
│   └── complex_usage.py          # Complex example
├── tests/
│   └── (test files)
├── docs/
│   └── (documentation)
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

## 🗂️ Memory Structure

Each project has its own memory:

```
~/.global/memory/[project-name]/
├── context.md                    # Project context
├── decisions.md                  # Architectural decisions
├── architecture.md               # System architecture
├── preferences.md                # Development preferences
├── progress.md                   # Project progress
├── code.md                       # Generated code
├── tests.md                      # Test code
├── documentation.md              # Documentation
└── agents_log.md                 # Agent interactions
```

## 🚫 Error Tracking

The system tracks errors to prevent repetition:

```
~/.global/errors/
├── do_not_make_this_error_again/
│   ├── 001_jwt_token_expiry.md
│   ├── 002_database_connection.md
│   └── ...
├── error_log.json
└── error_stats.json
```

## 🛠️ Helper System

Reusable components:

```
~/.global/helpers/
├── definitions/                  # Type definitions
├── errors/                       # Custom errors
├── imports/                      # Common imports
├── classes/                      # Base classes
└── modules/                      # Utility modules
```

## ⚙️ Configuration

### API Usage

- **Gemini (Lead)**: Unlimited (your subscription)
- **Claude (Reviewer)**: Limited (use wisely)
- **ChatGPT (Consultant)**: Limited (only for complex projects)

### Consultation Threshold

The system automatically consults ChatGPT for complex projects containing keywords like:
- microservice
- distributed
- scalability
- high availability
- real-time
- machine learning
- blockchain
- security

## 📊 Examples

See `examples/` directory:
- `simple_usage.py` - Simple project example
- `complex_usage.py` - Complex project with consultation

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## 📚 Documentation

See `docs/` directory for detailed documentation:
- Architecture design
- API reference
- Best practices
- Troubleshooting

## 🤝 Integration with Global Guidelines

This system is designed to work with **Global Guidelines v10.3.0**:

- Follows "BEST solution, not easiest" principle
- Maintains environment separation
- Uses Memory and MCP correctly
- Tracks and prevents errors
- Uses helper files
- Aims for 95%+ test coverage

## ⚠️ Important Notes

### Environment Separation

```
YOUR tools (AI's helper tools):
~/.global/memory/[project-name]/
~/.global/mcp/[project-name]/
~/.global/errors/
~/.global/helpers/

USER's project (generated code):
~/user-project/
```

**NEVER mix them!**

### API Key Security

- Never commit `.env` file
- Use environment variables
- Rotate keys regularly

### Cost Management

- Gemini: Unlimited (use freely)
- Claude: Limited (review + test only)
- ChatGPT: Very limited (complex projects only)

## 🔧 Troubleshooting

### "API key not found"
- Check `.env` file exists
- Verify API keys are correct
- Ensure environment variables are loaded

### "Agent failed to execute"
- Check API quotas
- Verify internet connection
- Check API key permissions

### "Tests failed"
- Review test output in Memory
- Check error logs
- System will auto-fix and retry

## 📝 License

MIT License - See LICENSE file

## 🙏 Credits

Built with:
- Google Gemini API
- Anthropic Claude API
- OpenAI ChatGPT API
- Global Guidelines v10.3.0

## 📧 Support

For issues or questions:
- GitHub Issues: https://github.com/hamfarid/autonomous-multiagent-system/issues
- Global Guidelines: https://github.com/hamfarid/global

---

**Version:** 1.0.0  
**Status:** Production Ready  
**Date:** November 5, 2025

🤖 **Autonomous, Collaborative, Intelligent** 🤖

