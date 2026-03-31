# MCP (Model Context Protocol) Usage Examples

## Overview
This document provides **practical, real-world examples** of how to use MCP (Model Context Protocol) in your development workflow. MCP is **MANDATORY** for all external interactions.

---

## 🔍 Example 1: Using MCP for Research & Information Gathering

### Scenario
You need to implement JWT authentication but are unsure about the best practices.

### How to Use MCP

#### Step 1: Search for Information
```bash
# Use MCP to search for JWT best practices
manus-mcp-cli tool call search --server brave_search --input '{
  "query": "JWT authentication best practices 2024",
  "count": 5
}'
```

#### Step 2: Analyze Results
MCP will return search results. Read through them and identify authoritative sources (e.g., OWASP, official JWT documentation).

#### Step 3: Save to Knowledge Base
```bash
# Save the verified information
cat > knowledge/jwt_best_practices.md << 'EOF'
# JWT Best Practices

## Key Points (verified from OWASP)
1. Use short expiration times (15 minutes for access tokens)
2. Implement refresh token rotation
3. Store tokens in httpOnly cookies (not localStorage)
4. Always validate the signature
5. Use strong signing algorithms (RS256, not HS256 for public APIs)

Source: https://owasp.org/...
EOF
```

#### Step 4: Log the Action
```bash
# Log to system_log.md
echo "[$(date)] RESEARCH: Used MCP to research JWT best practices. Saved to knowledge/jwt_best_practices.md" >> system_log.md
```

---

## 🧠 Example 2: Using MCP for Thinking & Planning

### Scenario
You need to decide between PostgreSQL and MongoDB for a new project.

### How to Use MCP

#### Step 1: Use MCP for Structured Thinking
```bash
# Use MCP to evaluate options
manus-mcp-cli tool call think --server thinking --input '{
  "problem": "Choose database: PostgreSQL vs MongoDB for e-commerce platform",
  "constraints": [
    "Need ACID transactions",
    "Complex relationships between users, orders, products",
    "Expected 100k+ users"
  ],
  "options": ["PostgreSQL", "MongoDB"]
}'
```

#### Step 2: MCP Returns Analysis
MCP will provide a structured analysis based on:
- OSF Framework (Security 35%, Correctness 20%, etc.)
- Your constraints
- Industry best practices

#### Step 3: Document the Decision
```bash
# Save to .memory/decisions/
cat > .memory/decisions/database_choice_20251107.md << 'EOF'
# Database Choice Decision

## Date: 2025-11-07
## Decision: PostgreSQL

## Rationale (OSF Framework):
- **Security (35%):** PostgreSQL has better ACID compliance and row-level security
- **Correctness (20%):** Strong typing and foreign key constraints prevent data corruption
- **Reliability (15%):** Mature, battle-tested in e-commerce
- **Performance (10%):** Sufficient for 100k users with proper indexing
- **Maintainability (10%):** SQL is well-known, easier to hire developers
- **Scalability (10%):** Can scale vertically and horizontally (with Citus)

## Alternatives Considered:
- MongoDB: Better for unstructured data, but lacks ACID guarantees

## Source: MCP thinking tool analysis
EOF
```

#### Step 4: Log the Decision
```bash
echo "[$(date)] DECISION: Chose PostgreSQL over MongoDB. Rationale saved to .memory/decisions/" >> system_log.md
```

---

## 🎭 Example 3: Using MCP Playwright for Frontend Testing

### Scenario
You need to test the login flow of a React application.

### How to Use MCP Playwright

#### Step 1: Install Browser (One-Time)
```bash
# Use MCP to install the browser
manus-mcp-cli tool call browser_install --server playwright --input '{
  "browser": "chromium"
}'
```

#### Step 2: Navigate to Login Page
```bash
# Navigate to the login page
manus-mcp-cli tool call browser_navigate --server playwright --input '{
  "url": "http://localhost:3000/login"
}'
```

#### Step 3: Fill Login Form
```bash
# Fill the login form
manus-mcp-cli tool call browser_fill --server playwright --input '{
  "selector": "#email",
  "value": "test@example.com"
}'

manus-mcp-cli tool call browser_fill --server playwright --input '{
  "selector": "#password",
  "value": "Test123456!"
}'
```

#### Step 4: Click Submit Button
```bash
# Click the login button
manus-mcp-cli tool call browser_click --server playwright --input '{
  "selector": "button[type=submit]"
}'
```

#### Step 5: Take Screenshot
```bash
# Take a screenshot to verify
manus-mcp-cli tool call browser_screenshot --server playwright --input '{
  "path": "tests/screenshots/login_success.png"
}'
```

#### Step 6: Verify Success
```bash
# Check if redirected to dashboard
manus-mcp-cli tool call browser_get_url --server playwright --input '{}'
# Expected: http://localhost:3000/dashboard
```

#### Step 7: Log the Test
```bash
echo "[$(date)] FRONTEND_TEST: Login flow tested with MCP Playwright. Screenshot saved." >> system_log.md
```

---

## 🔗 Example 4: Using MCP for API Integration

### Scenario
You need to integrate with a third-party weather API.

### How to Use MCP

#### Step 1: Search for API Documentation
```bash
# Use MCP to find the API
manus-mcp-cli tool call search --server brave_search --input '{
  "query": "OpenWeatherMap API documentation",
  "count": 3
}'
```

#### Step 2: Test the API
```bash
# Use MCP to make a test request (if available)
# Or use curl and log the result
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY" \
  | tee .memory/api_responses/weather_api_test.json
```

#### Step 3: Save API Example
```bash
cat > examples/11_weather_api_integration.md << 'EOF'
# Weather API Integration Example

## Endpoint
`GET https://api.openweathermap.org/data/2.5/weather`

## Parameters
- `q`: City name
- `appid`: API key (from environment variable)

## Example Response
```json
{
  "main": {
    "temp": 280.32,
    "humidity": 81
  },
  "weather": [
    {
      "description": "light rain"
    }
  ]
}
```

## Implementation
```javascript
const getWeather = async (city) => {
  const response = await fetch(
    `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${process.env.WEATHER_API_KEY}`
  );
  return response.json();
};
```
EOF
```

---

## 📋 MCP Usage Checklist

Before starting any task, ask yourself:

- [ ] **Do I need to research something?** → Use MCP search
- [ ] **Do I need to make a complex decision?** → Use MCP thinking
- [ ] **Do I need to test a frontend?** → Use MCP Playwright
- [ ] **Do I need to verify an API?** → Use MCP to test it
- [ ] **Did I log the MCP usage?** → Always log to `system_log.md`

---

## 🚨 Common Mistakes to Avoid

1. ❌ **Not using MCP for research** - Don't rely on outdated knowledge
2. ❌ **Not logging MCP usage** - Always log what you searched for and what you found
3. ❌ **Not saving results** - Save verified information to `knowledge/` or `examples/`
4. ❌ **Using MCP for simple tasks** - Use MCP for external interactions, not for basic file operations

---

## 📚 Related Files

- `prompts/02_mcp.md` - MCP prompt
- `prompts/03_thinking.md` - Thinking prompt
- `knowledge/` - Save verified information here
- `.memory/decisions/` - Save decisions here
- `system_log.md` - Log all MCP usage here

---

**Remember: MCP is MANDATORY for external interactions. Always use it, always log it.**

