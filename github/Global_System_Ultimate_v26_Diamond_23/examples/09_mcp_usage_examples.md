# 🔌 MCP Usage Examples (Global System Ultimate 2026)

**Status:** MANDATORY REFERENCE
**Enforcement:** Automated by Speckit (Analyze Phase)
**Version:** Global System Ultimate v8 - 2026 Edition

## 1. The Philosophy
The AI is a node in a vast network. MCP (Model Context Protocol) is the universal bus connecting agents, tools, and data.

## 2. Research Protocol (2026: Deep Research)
You MUST use MCP for multi-step deep research before answering complex questions.

```bash
# Correct Usage (Deep Research)
manus-mcp-cli tool call deep_research --server research_agent --input '{
  "topic": "Quantum-Resistant Cryptography in 2026",
  "depth": 3,
  "sources": ["arxiv", "ieee"]
}'
```

## 3. Thinking Protocol (2026: Neural-Symbolic)
You MUST use MCP for complex reasoning that requires symbolic logic verification.

```bash
# Correct Usage (Symbolic Verification)
manus-mcp-cli tool call verify_logic --server symbolic_reasoner --input '{
  "premise": "All microservices must be stateless",
  "conclusion": "Session data must be stored in Redis",
  "rules": ["12-Factor App"]
}'
```

## 4. Coding Protocol (2026: Semantic Edit)
You MUST use MCP for semantic code editing that understands project context.

```bash
# Correct Usage (Semantic Refactor)
manus-mcp-cli tool call refactor --server code_agent --input '{
  "target": "src/auth/login.ts",
  "instruction": "Migrate from JWT to Passkeys",
  "context": ["src/auth/types.ts"]
}'
```

## 5. The Logging Mandate (2026)
Every MCP call MUST be logged in `memory-bank/systemContext.md` with structured metadata.
`[MCP][2026-02-15] Called 'deep_research' | Topic: Quantum Crypto | Result: 15 papers analyzed.`
