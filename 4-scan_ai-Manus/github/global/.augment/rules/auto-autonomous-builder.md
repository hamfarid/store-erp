---
type: agent_requested
description: Autonomous multi-agent builder integration
keywords: autonomous, auto-build, multi-agent, @autonomous
priority: high
---

# Autonomous Multi-Agent Builder Integration

## Purpose

This rule enables Augment to use the autonomous multi-agent system for building complete projects automatically. When the user requests autonomous building, Augment will invoke the orchestrator which coordinates multiple AI agents (Gemini, Claude, ChatGPT) to design, code, review, test, and document the project.

## Activation

This rule activates when the user:
- Uses the keyword `@autonomous` in their message
- Explicitly requests "auto-build" or "multi-agent build"
- Asks to "build autonomously"

## How It Works

### Architecture

```
User → Augment → Orchestrator → Agents (Gemini, Claude, ChatGPT)
                                   ↓
                            Code + Tests + Docs
```

### Workflow

1. **Extract requirement** from user message
2. **Determine project name** (or generate one)
3. **Check if complex** (needs architectural consultation)
4. **Run orchestrator** via Python script
5. **Parse results** (code, tests, documentation)
6. **Present to user** in a clear format

## Instructions for Augment

When this rule activates, you MUST follow these steps:

### Step 1: Extract Information

From the user's message, extract:
- **Requirement**: What to build (e.g., "REST API for user authentication")
- **Project name**: Explicit name or generate from requirement (e.g., "user-auth-api")
- **Complexity**: Is this a complex project? (microservices, distributed systems, etc.)

### Step 2: Run the Orchestrator

Execute this command:

```bash
cd ~/.global/autonomous-multiagent-system && \
python augment_interface.py "[REQUIREMENT]" "[PROJECT_NAME]" [--consult]
```

**Parameters:**
- `[REQUIREMENT]`: The extracted requirement (in quotes)
- `[PROJECT_NAME]`: The project name (lowercase, hyphens, no spaces)
- `--consult`: Add this flag ONLY for complex projects

**Example (Simple):**
```bash
cd ~/.global/autonomous-multiagent-system && \
python augment_interface.py "Build a REST API for user authentication with JWT" "user-auth-api"
```

**Example (Complex):**
```bash
cd ~/.global/autonomous-multiagent-system && \
python augment_interface.py "Build a microservices system with user, product, and order services" "ecommerce-system" --consult
```

### Step 3: Parse the Output

The script outputs:
1. **Human-readable format** (with banners and sections)
2. **JSON format** (at the end, for programmatic access)

Parse the JSON output to extract:
- `success`: boolean
- `result.code`: Generated code
- `result.tests`: Generated tests
- `result.documentation`: Generated documentation
- `result.architecture`: Architecture design (if consulted)

### Step 4: Present Results

Present the results to the user in this format:

```markdown
## ✅ Project Built Successfully!

### 📋 Project Information
- **Name**: [project-name]
- **Requirement**: [requirement]
- **Agents Used**: Lead (Gemini), Reviewer (Claude)[, Consultant (ChatGPT)]

### 🏗️ Architecture
[Show architecture if available]

### 📝 Generated Code
[Show code with syntax highlighting]

### 🧪 Generated Tests
[Show tests with syntax highlighting]

### 📖 Documentation
[Show documentation]

### 💾 Files Location
The project files are saved in:
- Memory: `~/.global/memory/[project-name]/`
- Code: `~/.global/memory/[project-name]/code.md`
- Tests: `~/.global/memory/[project-name]/tests.md`
- Docs: `~/.global/memory/[project-name]/documentation.md`

### 🚀 Next Steps
[Suggest next steps based on the project]
```

### Step 5: Handle Errors

If the script fails:
1. Show the error message
2. Check common issues:
   - API keys not configured
   - Invalid requirement
   - Network issues
3. Suggest solutions
4. Offer to retry

## Examples

### Example 1: Simple Project

**User:**
```
@autonomous Build a REST API for todo list with Flask and SQLite
```

**Augment Action:**
```bash
cd ~/.global/autonomous-multiagent-system && \
python augment_interface.py "Build a REST API for todo list with Flask and SQLite" "todo-api"
```

**Augment Response:**
```markdown
## ✅ Project Built Successfully!

### 📋 Project Information
- **Name**: todo-api
- **Requirement**: Build a REST API for todo list with Flask and SQLite
- **Agents Used**: Lead (Gemini), Reviewer (Claude)

### 📝 Generated Code
[Shows Flask API code with routes, models, database setup]

### 🧪 Generated Tests
[Shows pytest tests with 95%+ coverage]

### 📖 Documentation
[Shows API documentation with endpoints, examples, setup instructions]
```

### Example 2: Complex Project

**User:**
```
@autonomous Build a microservices system with user authentication, product catalog, and order processing. Use PostgreSQL, Redis, and RabbitMQ.
```

**Augment Action:**
```bash
cd ~/.global/autonomous-multiagent-system && \
python augment_interface.py "Build a microservices system with user authentication, product catalog, and order processing. Use PostgreSQL, Redis, and RabbitMQ." "ecommerce-microservices" --consult
```

**Augment Response:**
```markdown
## ✅ Project Built Successfully!

### 📋 Project Information
- **Name**: ecommerce-microservices
- **Requirement**: Build a microservices system...
- **Agents Used**: Lead (Gemini), Reviewer (Claude), Consultant (ChatGPT)

### 🏗️ Architecture
[Shows detailed microservices architecture reviewed by ChatGPT]

### 📝 Generated Code
[Shows code for all microservices]

### 🧪 Generated Tests
[Shows comprehensive tests]

### 📖 Documentation
[Shows complete system documentation]
```

### Example 3: Without @autonomous Keyword

**User:**
```
Can you build me a REST API for user authentication?
```

**Augment Action:**
Ask the user:
```
Would you like me to build this autonomously using the multi-agent system? 
This will use Gemini, Claude, and (optionally) ChatGPT to design, code, review, 
test, and document the entire project automatically.

Reply with "@autonomous yes" to proceed.
```

## Important Notes

### API Usage

The system uses three APIs with different usage limits:
- **Gemini (Lead Agent)**: Unlimited ✅ - Used for most tasks
- **Claude (Reviewer Agent)**: Limited ⚠️ - Used only for review and testing
- **ChatGPT (Consultant Agent)**: Very Limited ⚠️⚠️ - Used only for complex projects with `--consult` flag

**Always prefer NOT using `--consult` unless the project is genuinely complex** (microservices, distributed systems, complex architecture).

### Project Complexity Guidelines

**Simple Projects** (no `--consult`):
- Single service/application
- Standard CRUD operations
- Common patterns (REST API, web app, CLI tool)
- Well-defined requirements

**Complex Projects** (use `--consult`):
- Multiple services (microservices)
- Distributed systems
- Complex architecture decisions
- Novel/unusual requirements
- High scalability needs

### Error Handling

Common errors and solutions:

1. **"GEMINI_API_KEY not found"**
   - Solution: Configure API keys in `~/.global/autonomous-multiagent-system/.env`

2. **"Failed to initialize orchestrator"**
   - Solution: Check if all dependencies are installed (`pip install -r requirements.txt`)

3. **"Agent failed"**
   - Solution: Check API quotas and network connection

4. **"Tests failed"**
   - The orchestrator will automatically retry and fix issues
   - If it still fails, show the error and suggest manual review

### Memory and Context

Each project has its own memory:
- Location: `~/.global/memory/[project-name]/`
- Contents: context, decisions, architecture, code, tests, documentation
- Persistent across sessions
- Can be referenced in future builds

### Best Practices

1. **Clear requirements**: The clearer the requirement, the better the result
2. **Appropriate complexity**: Don't use `--consult` for simple projects
3. **Review results**: Always review the generated code before using in production
4. **Iterate**: If the result isn't perfect, you can ask for modifications
5. **Save important projects**: The memory system saves everything, but you can also copy files to your workspace

## Integration with Other Tools

This autonomous builder can be combined with:
- **Augment's code editing**: For manual refinements
- **GitHub Copilot**: For inline suggestions
- **Manual review**: Always recommended for production code
- **Your expertise**: The system is a tool, not a replacement for your judgment

## Summary

When user says `@autonomous [requirement]`:
1. Extract requirement and project name
2. Determine if complex (needs `--consult`)
3. Run: `cd ~/.global/autonomous-multiagent-system && python augment_interface.py "[requirement]" "[project-name]" [--consult]`
4. Parse JSON output
5. Present results beautifully
6. Handle errors gracefully

**The system is fully autonomous - it will handle everything from understanding to documentation without any manual intervention!**

