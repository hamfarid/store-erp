# MCP Usage Rules (v26.0)
# Status: MANDATORY
# Enforcement: Automated by Speckit
# Scope: All Agents using Model Context Protocol tools

---

## 1. Philosophy
MCP (Model Context Protocol) is not an option — it is the primary mechanism for AI agents to interact with external systems. Every agent must use MCP tools when available instead of attempting manual workarounds or hallucinating results.

## 2. Mandatory Tool Usage

### 2.1 Research & Information Retrieval
When researching external information, agents MUST use available search MCP tools (e.g., `brave-search`, `context7`, `web_search`). Hallucinating URLs, API responses, or documentation content is strictly forbidden and constitutes Error #C003.

### 2.2 Database Operations
All database schema changes, queries, and data operations MUST use the appropriate database MCP tools (e.g., `supabase`, `postgres`). Direct SQL execution outside of MCP tools is only permitted when the MCP tool is unavailable AND the Architect approves.

### 2.3 UI & Browser Testing
Automated testing MUST use `playwright` MCP tools when available. Manual verification is a fallback, not the primary method. All Playwright test results must be logged.

### 2.4 File System Operations
File operations MUST use structured MCP tools when available. Agents should not construct file paths from memory — always verify paths exist before reading or writing.

## 3. Error Handling for MCP Calls

### 3.1 Retry Policy
If an MCP tool call fails, retry exactly ONCE with adjusted parameters (e.g., simplified query, different search terms). If the retry also fails, escalate to the user with the exact error message. Never pretend a failed MCP call succeeded.

### 3.2 Timeout Handling
Default timeout for MCP calls: 30 seconds. For long-running operations (database migrations, large file processing): 120 seconds. If timeout occurs, log the timeout and retry once before escalating.

### 3.3 Fallback Chain
When primary MCP tool is unavailable: (1) try alternative MCP tool for the same operation, (2) if no alternative exists, inform the user and request manual intervention, (3) never hallucinate results as a "fallback."

## 4. Logging & Traceability
Every MCP tool call MUST be logged in `memory-bank/activeContext.md` with: tool name, input parameters (summarized), output summary, and timestamp. This enables debugging of agent actions and creates an audit trail.

## 5. Security Constraints
MCP tools must NEVER be used to: store or transmit credentials in plain text, access systems outside the project scope, bypass authentication or authorization controls, or execute arbitrary code on production systems without explicit approval.

## 6. Cross-References
*   **Iron Rules**: `rules/00-iron-rules.md` — MCP usage is subject to all iron rules.
*   **Error Catalog**: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` — Error #C003 (hallucinated imports/APIs).
*   **Context Engineering**: `rules/RULES-context-engineering.md` — MCP supports the Context First protocol.
