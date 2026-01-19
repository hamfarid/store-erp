# MCP Configuration for Cursor, VS Code & Antigravity

Complete MCP server configuration for GAARA development environment.

**Version:** 2.0.0  
**Last Updated:** 2026-01-12  
**Author:** GAARA Technical Team

---

## 📁 File Structure

```
mcp-full-config/
├── .cursor/
│   └── mcp.json              ← Cursor configuration
├── .vscode/
│   └── mcp-settings.jsonc    ← VS Code configuration
├── antigravity/
│   └── mcp-config.json       ← Google Antigravity configuration
├── .env.template             ← Environment variables template
└── README.md                 ← This file
```

---

## 🔧 Configured MCP Servers (17 Total)

| Server | Purpose | API Key | Category |
|--------|---------|---------|----------|
| **Sequential Thinking** | Problem-solving, reasoning | ❌ None | Reasoning |
| **Exa** | Code search, web research | ✅ Required | Research |
| **Speckit** | API specifications | ❌ None | API |
| **Ref** | Documentation verification | ✅ Required | Documentation |
| **Supabase** | Database queries | ✅ Required | Database |
| **Sentry** | Error tracking | ✅ Required | Monitoring |
| **GitHub** | Code management | ✅ Required | VCS |
| **Firecrawl** | Web scraping | ✅ Required | Scraping |
| **Pinecone** | Vector search | ✅ Required | Vector DB |
| **Vectara** | RAG engine | ✅ Required | RAG |
| **Playwright** | Browser automation | ❌ None | Testing |
| **Magic UI** | Animations, marketing UI | ❌ None | UI |
| **Shadcn** | Professional UI components | ❌ None | UI |
| **Datadog** | Observability | ✅ Required | Monitoring |
| **Snyk** | Security scanning | ✅ Required | Security |
| **Railway** | Django/Python deployment | ✅ Required | Deployment |
| **Vercel** | Frontend deployment | ✅ Required | Deployment |

---

## 🚀 Installation

### Step 1: Set Environment Variables

```bash
# Copy the template
cp .env.template ~/.env.mcp

# Edit with your API keys
nano ~/.env.mcp

# Add to your shell profile (~/.bashrc or ~/.zshrc)
echo "source ~/.env.mcp" >> ~/.zshrc
source ~/.zshrc
```

### Step 2: Install for Your IDE

---

## 📌 CURSOR INSTALLATION

### Option A: Global Configuration (All Projects)

```bash
# Create global config directory
mkdir -p ~/.cursor

# Copy configuration
cp .cursor/mcp.json ~/.cursor/mcp.json
```

### Option B: Project-Specific Configuration

```bash
# In your project root
mkdir -p .cursor
cp /path/to/mcp-full-config/.cursor/mcp.json .cursor/mcp.json
```

### Verify Installation

1. Open Cursor
2. Press `Cmd/Ctrl + Shift + P`
3. Search: "Cursor Settings"
4. Navigate to MCP tab
5. Verify servers are listed

---

## 📌 VS CODE INSTALLATION

### Option A: User Settings (Global)

```bash
# Linux/macOS
cp .vscode/mcp-settings.jsonc ~/.config/Code/User/settings.json

# Windows
cp .vscode/mcp-settings.jsonc %APPDATA%\Code\User\settings.json
```

### Option B: Workspace Settings (Project-Specific)

```bash
# In your project root
mkdir -p .vscode
cp /path/to/mcp-full-config/.vscode/mcp-settings.jsonc .vscode/settings.json
```

### Required Extension

Install the MCP extension for VS Code:
```bash
code --install-extension anthropic.vscode-mcp
```

---

## 📌 GOOGLE ANTIGRAVITY INSTALLATION

### Configuration File Location

```bash
# Linux/macOS
mkdir -p ~/.config/antigravity
cp antigravity/mcp-config.json ~/.config/antigravity/mcp-config.json

# Or project-specific
cp antigravity/mcp-config.json /your/project/.antigravity/mcp-config.json
```

### Verify in Antigravity

1. Open Antigravity
2. Go to Settings → MCP Servers
3. Import configuration or verify auto-detection

---

## 🔑 Getting API Keys

### Required Keys

| Service | Get Key From |
|---------|--------------|
| **Exa** | https://exa.ai/api-keys |
| **Ref** | https://ref.dev/settings/api |
| **Supabase** | https://app.supabase.com/project/_/settings/api |
| **Sentry** | https://sentry.io/settings/account/api/auth-tokens/ |
| **GitHub** | https://github.com/settings/tokens |
| **Firecrawl** | https://firecrawl.dev/app/api-keys |
| **Pinecone** | https://app.pinecone.io/organizations/-/keys |
| **Vectara** | https://console.vectara.com/console/apiAccess |
| **Datadog** | https://app.datadoghq.com/organization-settings/api-keys |
| **Snyk** | https://app.snyk.io/account |
| **Railway** | https://railway.app/account/tokens |
| **Vercel** | https://vercel.com/account/tokens |

### No API Key Required
- Speckit
- Playwright
- Magic UI
- Shadcn UI
- Sequential Thinking

---

## 📋 Server Categories & Usage

### 🧠 Reasoning
```
sequential-thinking → Use for complex problem-solving
```

### 🔍 Research (Priority Order)
```
1. exa → get_code_context_exa (FIRST)
2. exa → web_search_exa (FALLBACK)
3. speckit → API specifications
4. ref → Documentation (LAST RESORT)
```

### 💾 Database
```
supabase → Direct Postgres queries, schema exploration
```

### 🔒 Security & Monitoring
```
sentry → Error tracking, stack traces
datadog → Metrics, logs, traces, APM
snyk → Vulnerability scanning
```

### 🌐 Web & Scraping
```
firecrawl → Web scraping, data extraction
playwright → Browser automation, testing
```

### 🎨 UI & Components
```
shadcn → Professional, accessible React components
magic-ui → Animations, marketing sections
```

### 🔎 Vector & RAG
```
pinecone → Vector search, embeddings
vectara → RAG, document retrieval
```

### 📂 Code Management
```
github → PRs, issues, repositories
```

### 🚀 Deployment
```
railway → Django/Python backend hosting
vercel → Frontend deployment, preview URLs
```

---

## 🛠️ Troubleshooting

### MCP Servers Not Loading

```bash
# Check if Node.js is installed
node --version

# Clear npx cache
npx clear-npx-cache

# Verify environment variables
echo $EXA_API_KEY
```

### Connection Issues

```bash
# Test individual server
npx -y @anthropic/mcp-exa --help

# Check logs
# Cursor: Cmd/Ctrl + Shift + P → "Developer: Show Logs"
# VS Code: View → Output → Select "MCP"
```

### Authentication Errors

1. Verify API key is correct
2. Check key permissions/scopes
3. Ensure environment variable is exported
4. Restart IDE after changes

---

## 📊 Quick Reference

### Cursor Commands
```
Cmd/Ctrl + Shift + P → "Cursor Settings" → MCP
```

### VS Code Commands
```
Cmd/Ctrl + Shift + P → "MCP: List Servers"
Cmd/Ctrl + Shift + P → "MCP: Restart Server"
```

### Environment Check
```bash
# Print all MCP-related env vars
env | grep -E "(EXA|REF|SUPABASE|SENTRY|GITHUB|FIRECRAWL|PINECONE|VECTARA|DD_|SNYK)"
```

---

## 🔗 Resources

- [MCP Official Docs](https://modelcontextprotocol.io)
- [Cursor MCP Guide](https://docs.cursor.com/context/model-context-protocol)
- [MCP Server Directory](https://cursor.directory/mcp)
- [GitHub MCP Servers](https://github.com/modelcontextprotocol/servers)

---

## 📄 License

Internal use - GAARA Technical Team
