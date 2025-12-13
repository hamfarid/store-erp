# MCP Sequential Thinking Integration (Reference)

This folder contains ready-to-use example configurations to connect the official MCP "sequentialthinking" server to an MCP client (e.g., Claude Desktop). These files are for reference only; you typically paste their contents into your MCP client's config file.

## Option A — NPX (no Docker required)

Paste this into your MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    }
  }
}
```

Prerequisites:
- Node.js installed and available on PATH

## Option B — Docker

Paste this into your MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sequentialthinking": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "mcp/sequentialthinking"
      ]
    }
  }
}
```

Prerequisites:
- Docker installed and available on PATH

### Build the Docker image locally (optional)

From the root of the MCP repository:

```bash
docker build -t mcp/sequentialthinking -f src/sequentialthinking/Dockerfile .
```

## Verification tips
- After updating your MCP client config, restart the client and check its server list/inspector.
- Ensure Node (for NPX) or Docker (for Docker path) is installed and accessible.
- If behind a proxy, confirm `npx` and Docker pulls are allowed by your network policy.

