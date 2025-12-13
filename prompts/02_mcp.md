================================================================================
MODULE 15: MODEL CONTEXT PROTOCOL (MCP) INTEGRATION
================================================================================

⚠️ NOTE: This module is part of Global Guidelines (instruction manual).
Apply this guidance to THE USER'S PROJECT, not to Global Guidelines itself.
Global Guidelines is in: ~/global/ or similar
User's project is in: A separate directory (ask user for project path)



⚡ MANDATORY ACTIVATION:
================================================================================
AI MUST check and use MCP from the FIRST interaction!

When to activate:
-----------------
✅ At the very start of any task
✅ Before suggesting any solutions
✅ When user mentions any tool or integration
✅ Throughout the task to leverage available tools

How to activate:
----------------
1. Check available MCP servers immediately
2. List tools from each server
3. Use appropriate tools for the task
4. Don't reinvent what MCP already provides

⚠️ CRITICAL: If you're NOT checking MCP servers at the start, you're NOT
following Global Guidelines properly! MCP is NOT optional - it's MANDATORY!

Example First Interaction:
--------------------------
User: "Help me build a web app"

AI MUST do:
✅ "Let me check available MCP tools first..."
✅ Check: manus-mcp-cli tool list --server <each_server>
✅ "I found these tools: [list]"
✅ Use relevant tools throughout the task

AI MUST NOT:
❌ Start without checking MCP
❌ Ignore available MCP tools
❌ Manually do what MCP tools can do




OVERVIEW
--------
Model Context Protocol (MCP) is an open-source protocol that connects AI applications.
with external systems and tools. MCP provides a standardized way to extend the capabilities of LLMs through
الاتصال بالخوادم المتخصصة.

CORE CONCEPTS
-------------

1. MCP Architecture
   - Client: التطبيق الذي يستخدم MCP (VS Code, Claude, Cursor)
   - Server: الخادم الذي يوفر الأدوات والموارد
   - Transport: طريقة الاتصال (SSE, stdio, HTTP)
   - Protocol: البروتوكول الموحد للتواصل

2. MCP Components
   - Tools: وظائف قابلة للاستدعاء
   - Resources: بيانات ومحتوى
   - Prompts: قوالب للتفاعل
   - Sampling: طلبات LLM

3. MCP Benefits
   - توحيد التكامل مع الأدوات الخارجية
   - أمان محسّن مع صلاحيات محددة
   - قابلية التوسع والصيانة
   - دعم متعدد المنصات

================================================================================
SECTION 1: PLAYWRIGHT MCP SERVER
================================================================================

OVERVIEW
--------
Playwright MCP Server provides browser automation capabilities using Playwright.
يمكّن LLMs من التفاعل مع صفحات الويب من خلال snapshots منظمة.

Repository: https://github.com/microsoft/playwright-mcp
Package: @playwright/mcp

KEY FEATURES
------------

1. Fast and Lightweight
   - يستخدم accessibility tree بدلاً من الصور
   - لا يحتاج لنماذج vision
   - أداء سريع ومحدد

2. LLM-Friendly
   - بيانات منظمة structured data
   - لا يحتاج لمعالجة صور
   - نتائج محددة deterministic

3. Browser Automation
   - دعم Chrome, Firefox, WebKit
   - headless و headed modes
   - device emulation
   - network interception

INSTALLATION
------------

```bash
# تثبيت عبر npm
npx @playwright/mcp@latest

# تثبيت المتصفحات
npx playwright install chrome

# استخدام Docker
docker run -i --rm --init --pull=always mcr.microsoft.com/playwright/mcp
```

CONFIGURATION
-------------

### VS Code Configuration

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser", "chrome",
        "--headless"
      ]
    }
  }
}
```

### Docker Configuration

```json
{
  "mcpServers": {
    "playwright": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init",
        "--pull=always",
        "mcr.microsoft.com/playwright/mcp"
      ]
    }
  }
}
```

AVAILABLE TOOLS
---------------

### Navigation Tools

1. browser_navigate
   - التنقل إلى URL محدد
   - دعم timeout وwait conditions

```typescript
{
  "name": "browser_navigate",
  "arguments": {
    "url": "https://example.com",
    "waitUntil": "networkidle"
  }
}
```

2. browser_close
   - إغلاق الصفحة أو المتصفح
   - تنظيف الموارد

### Interaction Tools

3. browser_click
   - النقر على عنصر
   - دعم selectors متعددة

```typescript
{
  "name": "browser_click",
  "arguments": {
    "selector": "button[data-testid='submit']"
  }
}
```

4. browser_type
   - كتابة نص في حقل
   - دعم keyboard events

```typescript
{
  "name": "browser_type",
  "arguments": {
    "selector": "input[name='email']",
    "text": "user@example.com"
  }
}
```

5. browser_fill_form
   - ملء نموذج كامل
   - دعم حقول متعددة

```typescript
{
  "name": "browser_fill_form",
  "arguments": {
    "fields": [
      {"selector": "input[name='username']", "value": "admin"},
      {"selector": "input[name='password']", "value": "secret"}
    ]
  }
}
```

6. browser_select_option
   - اختيار من dropdown
   - دعم value, label, index

7. browser_hover
   - تحريك المؤشر فوق عنصر
   - تفعيل hover effects

8. browser_drag
   - سحب وإفلات بين عناصر
   - دعم drag and drop

### Data Extraction Tools

9. browser_snapshot
   - التقاط accessibility snapshot
   - بيانات منظمة للصفحة

```typescript
{
  "name": "browser_snapshot",
  "arguments": {
    "selector": "main" // optional
  }
}
```

10. browser_take_screenshot
    - التقاط صورة للصفحة
    - دعم full page و viewport

```typescript
{
  "name": "browser_take_screenshot",
  "arguments": {
    "fullPage": true,
    "path": "screenshot.png"
  }
}
```

11. browser_evaluate
    - تنفيذ JavaScript
    - إرجاع النتائج

```typescript
{
  "name": "browser_evaluate",
  "arguments": {
    "expression": "document.title"
  }
}
```

### Network Tools

12. browser_network_requests
    - قائمة طلبات الشبكة
    - تحليل API calls

13. browser_console_messages
    - رسائل console
    - أخطاء JavaScript

### File Operations

14. browser_file_upload
    - رفع ملفات
    - دعم multiple files

```typescript
{
  "name": "browser_file_upload",
  "arguments": {
    "selector": "input[type='file']",
    "files": ["/path/to/file.pdf"]
  }
}
```

### Wait Operations

15. browser_wait_for
    - انتظار شروط محددة
    - timeout configurable

```typescript
{
  "name": "browser_wait_for",
  "arguments": {
    "selector": ".loading",
    "state": "hidden",
    "timeout": 5000
  }
}
```

ADVANCED CONFIGURATION
----------------------

### Security Options

```bash
# حظر service workers
npx @playwright/mcp@latest --block-service-workers

# تحديد origins مسموحة
npx @playwright/mcp@latest --allowed-origins "https://example.com;https://api.example.com"

# حظر origins معينة
npx @playwright/mcp@latest --blocked-origins "https://ads.example.com"

# منح صلاحيات
npx @playwright/mcp@latest --grant-permissions "geolocation,clipboard-read"
```

### Performance Options

```bash
# headless mode
npx @playwright/mcp@latest --headless

# device emulation
npx @playwright/mcp@latest --device "iPhone 15"

# viewport size
npx @playwright/mcp@latest --viewport-size "1920x1080"

# timeout settings
npx @playwright/mcp@latest --timeout-action 10000 --timeout-navigation 60000
```

### Recording Options

```bash
# حفظ trace
npx @playwright/mcp@latest --save-trace

# حفظ video
npx @playwright/mcp@latest --save-video "1280x720"

# حفظ session
npx @playwright/mcp@latest --save-session

# مجلد الإخراج
npx @playwright/mcp@latest --output-dir "./test-results"
```

TESTING USE CASES
-----------------

### 1. Frontend Testing Complete

```typescript
// اختبار صفحة تسجيل الدخول
{
  "workflow": [
    {
      "tool": "browser_navigate",
      "args": {"url": "https://app.example.com/login"}
    },
    {
      "tool": "browser_fill_form",
      "args": {
        "fields": [
          {"selector": "#email", "value": "test@example.com"},
          {"selector": "#password", "value": "testpass123"}
        ]
      }
    },
    {
      "tool": "browser_click",
      "args": {"selector": "button[type='submit']"}
    },
    {
      "tool": "browser_wait_for",
      "args": {"selector": ".dashboard", "state": "visible"}
    },
    {
      "tool": "browser_snapshot",
      "args": {}
    }
  ]
}
```

### 2. API Route Testing

```typescript
// اختبار API endpoints من الواجهة
{
  "workflow": [
    {
      "tool": "browser_navigate",
      "args": {"url": "https://app.example.com"}
    },
    {
      "tool": "browser_network_requests",
      "args": {"filter": "api/*"}
    },
    {
      "tool": "browser_evaluate",
      "args": {
        "expression": `
          fetch('/api/users')
            .then(r => r.json())
            .then(data => data)
        `
      }
    }
  ]
}
```

### 3. Security Testing

```typescript
// اختبار أمان الصفحة
{
  "workflow": [
    {
      "tool": "browser_navigate",
      "args": {"url": "https://app.example.com"}
    },
    {
      "tool": "browser_console_messages",
      "args": {"level": "error"}
    },
    {
      "tool": "browser_evaluate",
      "args": {
        "expression": `
          // فحص CSP headers
          document.querySelector('meta[http-equiv="Content-Security-Policy"]')?.content
        `
      }
    }
  ]
}
```

### 4. Performance Testing

```typescript
// قياس أداء الصفحة
{
  "workflow": [
    {
      "tool": "browser_navigate",
      "args": {"url": "https://app.example.com"}
    },
    {
      "tool": "browser_evaluate",
      "args": {
        "expression": `
          JSON.stringify(performance.getEntriesByType('navigation')[0])
        `
      }
    },
    {
      "tool": "browser_network_requests",
      "args": {"includeTimings": true}
    }
  ]
}
```

PROGRAMMATIC USAGE
------------------

```javascript
import http from 'http';
import { createConnection } from '@playwright/mcp';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';

http.createServer(async (req, res) => {
  // إنشاء اتصال Playwright MCP
  const connection = await createConnection({
    browser: {
      launchOptions: {
        headless: true,
        args: ['--no-sandbox']
      }
    }
  });

  // إنشاء SSE transport
  const transport = new SSEServerTransport('/messages', res);
  
  // ربط الاتصال
  await connection.connect(transport);
}).listen(3000);
```

================================================================================
SECTION 2: CONTEXT7 MCP SERVER
================================================================================

OVERVIEW
--------
Context7 MCP Server provides up-to-date documentation and live code examples directly from the source.
يضمن حصول LLMs على معلومات دقيقة ومحدثة للمكتبات والأطر.

Repository: https://github.com/upstash/context7
Website: https://context7.com

KEY FEATURES
------------

1. Up-to-Date Documentation
   - وثائق محدثة من المصدر
   - دعم إصدارات متعددة
   - أمثلة كود حقيقية

2. Library Support
   - دعم آلاف المكتبات
   - JavaScript, Python, Go, Rust
   - Frameworks شائعة

3. Version-Specific
   - وثائق خاصة بالإصدار
   - changelog وmigratio guides
   - breaking changes

INSTALLATION
------------

```bash
# تثبيت عبر npm
npx @upstash/context7-mcp@latest

# استخدام Docker
docker run -i --rm mcp/context7
```

CONFIGURATION
-------------

### VS Code Configuration

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["@upstash/context7-mcp@latest"]
    }
  }
}
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

AVAILABLE TOOLS
---------------

### 1. search_libraries

البحث عن مكتبات متاحة

```typescript
{
  "name": "search_libraries",
  "arguments": {
    "query": "react",
    "language": "javascript"
  }
}
```

### 2. resolve_library_id

الحصول على معرف مكتبة محدد

```typescript
{
  "name": "resolve_library_id",
  "arguments": {
    "name": "react",
    "version": "18.2.0"
  }
}
```

### 3. get_documentation

جلب وثائق مكتبة

```typescript
{
  "name": "get_documentation",
  "arguments": {
    "libraryId": "react@18.2.0",
    "topic": "hooks"
  }
}
```

### 4. get_code_examples

الحصول على أمثلة كود

```typescript
{
  "name": "get_code_examples",
  "arguments": {
    "libraryId": "react@18.2.0",
    "feature": "useState"
  }
}
```

USE CASES
---------

### 1. Framework Documentation

```typescript
// الحصول على وثائق Next.js
{
  "workflow": [
    {
      "tool": "search_libraries",
      "args": {"query": "next.js"}
    },
    {
      "tool": "resolve_library_id",
      "args": {"name": "next", "version": "14.0.0"}
    },
    {
      "tool": "get_documentation",
      "args": {
        "libraryId": "next@14.0.0",
        "topic": "app-router"
      }
    }
  ]
}
```

### 2. API Reference

```typescript
// الحصول على مرجع API
{
  "workflow": [
    {
      "tool": "resolve_library_id",
      "args": {"name": "express", "version": "latest"}
    },
    {
      "tool": "get_documentation",
      "args": {
        "libraryId": "express@latest",
        "topic": "middleware"
      }
    },
    {
      "tool": "get_code_examples",
      "args": {
        "libraryId": "express@latest",
        "feature": "error-handling"
      }
    }
  ]
}
```

### 3. Migration Guide

```typescript
// دليل الترقية
{
  "workflow": [
    {
      "tool": "get_documentation",
      "args": {
        "libraryId": "react@17.0.0",
        "topic": "migration"
      }
    },
    {
      "tool": "get_documentation",
      "args": {
        "libraryId": "react@18.0.0",
        "topic": "breaking-changes"
      }
    }
  ]
}
```

INTEGRATION WITH PLAYWRIGHT
----------------------------

```typescript
// دمج Context7 مع Playwright للاختبار المستنير
{
  "workflow": [
    // 1. الحصول على وثائق المكتبة
    {
      "tool": "context7.get_documentation",
      "args": {
        "libraryId": "react-testing-library@latest",
        "topic": "queries"
      }
    },
    // 2. استخدام Playwright للاختبار
    {
      "tool": "playwright.browser_navigate",
      "args": {"url": "https://app.example.com"}
    },
    {
      "tool": "playwright.browser_snapshot",
      "args": {}
    }
  ]
}
```

================================================================================
SECTION 3: GITHUB MCP SERVER
================================================================================

OVERVIEW
--------
GitHub MCP Server directly connects AI tools to the GitHub platform.
يوفر قدرات شاملة لإدارة المستودعات، Issues، PRs، والمزيد.

Repository: https://github.com/github/github-mcp-server
Remote Server: https://api.githubcopilot.com/mcp/

KEY FEATURES
------------

1. Repository Management
   - تصفح الكود والملفات
   - البحث في المستودعات
   - تحليل commits
   - فهم بنية المشروع

2. Issue & PR Automation
   - إنشاء وتحديث Issues
   - إدارة Pull Requests
   - code review
   - project boards

3. CI/CD Intelligence
   - مراقبة GitHub Actions
   - تحليل build failures
   - إدارة releases
   - workflow insights

4. Code Analysis
   - security findings
   - Dependabot alerts
   - code patterns
   - codebase insights

5. Team Collaboration
   - discussions
   - notifications
   - team activity
   - process automation

INSTALLATION
------------

### Remote Server (Recommended)

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

### Local Server with Docker

```bash
# إنشاء GitHub Personal Access Token
# https://github.com/settings/tokens

# تشغيل عبر Docker
docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token \
  ghcr.io/github/github-mcp-server
```

CONFIGURATION
-------------

### VS Code Configuration (OAuth)

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

### VS Code Configuration (PAT)

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${input:github_mcp_pat}"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "github_mcp_pat",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ]
}
```

### Local Server Configuration

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

### GitHub Enterprise Configuration

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "-e", "GITHUB_HOST",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token",
        "GITHUB_HOST": "https://github.enterprise.com"
      }
    }
  }
}
```

AVAILABLE TOOLS
---------------

### Repository Operations

1. list_repositories
   - قائمة المستودعات
   - فلترة وترتيب

2. get_repository
   - معلومات مستودع
   - إحصائيات

3. search_repositories
   - البحث في المستودعات
   - advanced queries

4. get_file_contents
   - قراءة محتوى ملف
   - دعم branches

5. search_code
   - البحث في الكود
   - regex support

### Issue Management

6. list_issues
   - قائمة Issues
   - فلترة بالحالة

7. create_issue
   - إنشاء issue جديد
   - labels وassignees

8. update_issue
   - تحديث issue
   - إغلاق أو إعادة فتح

9. add_issue_comment
   - إضافة تعليق
   - markdown support

### Pull Request Operations

10. list_pull_requests
    - قائمة PRs
    - فلترة بالحالة

11. create_pull_request
    - إنشاء PR جديد
    - من branch إلى branch

12. update_pull_request
    - تحديث PR
    - merge أو close

13. get_pull_request_diff
    - الحصول على diff
    - تحليل التغييرات

14. request_review
    - طلب مراجعة
    - assign reviewers

### Workflow Operations

15. list_workflows
    - قائمة workflows
    - GitHub Actions

16. get_workflow_run
    - معلومات workflow run
    - logs وstatus

17. trigger_workflow
    - تشغيل workflow
    - مع parameters

### Release Management

18. list_releases
    - قائمة releases
    - latest وpre-releases

19. create_release
    - إنشاء release جديد
    - مع assets

20. get_latest_release
    - أحدث release
    - download URLs

USE CASES
---------

### 1. Issue Tracking and Search

```typescript
// البحث عن issues والمشاكل
{
  "workflow": [
    {
      "tool": "search_repositories",
      "args": {
        "query": "language:javascript stars:>1000"
      }
    },
    {
      "tool": "list_issues",
      "args": {
        "owner": "facebook",
        "repo": "react",
        "state": "open",
        "labels": "bug"
      }
    },
    {
      "tool": "create_issue",
      "args": {
        "owner": "myorg",
        "repo": "myproject",
        "title": "Found security vulnerability",
        "body": "Details...",
        "labels": ["security", "high-priority"]
      }
    }
  ]
}
```

### 2. Latest Release Check

```typescript
// فحص أحدث الإصدارات
{
  "workflow": [
    {
      "tool": "get_latest_release",
      "args": {
        "owner": "nodejs",
        "repo": "node"
      }
    },
    {
      "tool": "list_releases",
      "args": {
        "owner": "nodejs",
        "repo": "node",
        "per_page": 5
      }
    }
  ]
}
```

### 3. Code Review Automation

```typescript
// مراجعة كود تلقائية
{
  "workflow": [
    {
      "tool": "list_pull_requests",
      "args": {
        "owner": "myorg",
        "repo": "myproject",
        "state": "open"
      }
    },
    {
      "tool": "get_pull_request_diff",
      "args": {
        "owner": "myorg",
        "repo": "myproject",
        "pull_number": 123
      }
    },
    {
      "tool": "add_issue_comment",
      "args": {
        "owner": "myorg",
        "repo": "myproject",
        "issue_number": 123,
        "body": "LGTM! ✅"
      }
    }
  ]
}
```

### 4. CI/CD Monitoring

```typescript
// مراقبة workflows
{
  "workflow": [
    {
      "tool": "list_workflows",
      "args": {
        "owner": "myorg",
        "repo": "myproject"
      }
    },
    {
      "tool": "get_workflow_run",
      "args": {
        "owner": "myorg",
        "repo": "myproject",
        "run_id": 123456
      }
    }
  ]
}
```

SECURITY BEST PRACTICES
------------------------

### Token Management

```bash
# تخزين آمن للـ token
export GITHUB_PAT=ghp_xxxxxxxxxxxx

# استخدام .env file
echo "GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxx" > .env
echo ".env" >> .gitignore

# صلاحيات محدودة
# منح فقط الصلاحيات المطلوبة:
# - repo: للوصول للمستودعات
# - read:packages: لصور Docker
# - read:org: لفرق المنظمة
```

### Token Rotation

```bash
# تدوير دوري للـ tokens
# إنشاء token جديد كل 90 يوم
# حذف tokens القديمة

# استخدام tokens منفصلة للبيئات المختلفة
GITHUB_PAT_DEV=...
GITHUB_PAT_PROD=...
```

================================================================================
SECTION 4: COMPREHENSIVE TESTING WORKFLOW
================================================================================

COMPLETE FRONTEND TESTING
--------------------------

### Test Plan Structure

```typescript
{
  "testPlan": {
    "name": "Complete Frontend Test Suite",
    "phases": [
      "1. Setup and Navigation",
      "2. API Route Testing",
      "3. Security Testing",
      "4. Performance Testing",
      "5. Issue Reporting"
    ]
  }
}
```

### Phase 1: Setup and Navigation

```typescript
{
  "phase": "Setup",
  "tools": ["playwright"],
  "steps": [
    {
      "tool": "browser_navigate",
      "args": {
        "url": "https://app.example.com",
        "waitUntil": "networkidle"
      }
    },
    {
      "tool": "browser_snapshot",
      "args": {},
      "validate": "page loaded successfully"
    }
  ]
}
```

### Phase 2: API Route Testing

```typescript
{
  "phase": "API Testing",
  "tools": ["playwright"],
  "steps": [
    // اختبار GET endpoints
    {
      "tool": "browser_evaluate",
      "args": {
        "expression": `
          fetch('/api/users')
            .then(r => ({status: r.status, data: r.json()}))
        `
      },
      "validate": "status === 200"
    },
    // اختبار POST endpoints
    {
      "tool": "browser_evaluate",
      "args": {
        "expression": `
          fetch('/api/users', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name: 'Test User'})
          }).then(r => r.json())
        `
      }
    },
    // مراقبة network requests
    {
      "tool": "browser_network_requests",
      "args": {
        "filter": "api/*",
        "includeTimings": true
      }
    }
  ]
}
```

### Phase 3: Security Testing

```typescript
{
  "phase": "Security",
  "tools": ["playwright", "context7"],
  "steps": [
    // الحصول على best practices
    {
      "tool": "context7.get_documentation",
      "args": {
        "libraryId": "owasp-top-10@latest",
        "topic": "web-security"
      }
    },
    // فحص CSP headers
    {
      "tool": "browser_evaluate",
      "args": {
        "expression": `
          ({
            csp: document.querySelector('meta[http-equiv="Content-Security-Policy"]')?.content,
            xframe: document.querySelector('meta[http-equiv="X-Frame-Options"]')?.content
          })
        `
      }
    },
    // فحص console errors
    {
      "tool": "browser_console_messages",
      "args": {"level": "error"}
    },
    // اختبار authentication
    {
      "tool": "browser_fill_form",
      "args": {
        "fields": [
          {"selector": "#username", "value": "admin"},
          {"selector": "#password", "value": "wrongpass"}
        ]
      }
    },
    {
      "tool": "browser_click",
      "args": {"selector": "button[type='submit']"}
    },
    {
      "tool": "browser_wait_for",
      "args": {
        "selector": ".error-message",
        "state": "visible"
      }
    }
  ]
}
```

### Phase 4: Performance Testing

```typescript
{
  "phase": "Performance",
  "tools": ["playwright"],
  "steps": [
    // قياس page load
    {
      "tool": "browser_evaluate",
      "args": {
        "expression": `
          JSON.stringify({
            navigation: performance.getEntriesByType('navigation')[0],
            resources: performance.getEntriesByType('resource').length,
            paint: performance.getEntriesByType('paint')
          })
        `
      }
    },
    // قياس network performance
    {
      "tool": "browser_network_requests",
      "args": {
        "includeTimings": true,
        "includeSizes": true
      }
    },
    // التقاط screenshots
    {
      "tool": "browser_take_screenshot",
      "args": {
        "fullPage": true,
        "path": "performance-test.png"
      }
    }
  ]
}
```

### Phase 5: Issue Reporting

```typescript
{
  "phase": "Reporting",
  "tools": ["github"],
  "steps": [
    // البحث عن issues مشابهة
    {
      "tool": "github.list_issues",
      "args": {
        "owner": "myorg",
        "repo": "myproject",
        "state": "open",
        "labels": "bug"
      }
    },
    // إنشاء issue جديد
    {
      "tool": "github.create_issue",
      "args": {
        "owner": "myorg",
        "repo": "myproject",
        "title": "Security: Missing CSP header",
        "body": `
## Issue Description
Missing Content-Security-Policy header detected.

## Steps to Reproduce
1. Navigate to https://app.example.com
2. Inspect response headers
3. CSP header is missing

## Expected Behavior
CSP header should be present with strict policy

## Test Results
- Browser: Chrome
- Date: 2025-01-02
- Tester: MCP Automation

## Screenshots
See attached screenshot.
        `,
        "labels": ["security", "high-priority"]
      }
    }
  ]
}
```

AUTOMATED TESTING WORKFLOW
---------------------------

```typescript
{
  "automatedWorkflow": {
    "trigger": "on_push",
    "steps": [
      // 1. الحصول على أحدث الوثائق
      {
        "mcp": "context7",
        "action": "get_documentation",
        "library": "testing-library"
      },
      // 2. تشغيل اختبارات Playwright
      {
        "mcp": "playwright",
        "action": "run_test_suite",
        "config": "playwright.config.ts"
      },
      // 3. تحليل النتائج
      {
        "mcp": "playwright",
        "action": "analyze_results",
        "generateReport": true
      },
      // 4. رفع issues للفشل
      {
        "mcp": "github",
        "action": "create_issue_if_failed",
        "assignees": ["@qa-team"]
      },
      // 5. تحديث PR
      {
        "mcp": "github",
        "action": "add_pr_comment",
        "summary": "test_results"
      }
    ]
  }
}
```

================================================================================
SECTION 5: BEST PRACTICES
================================================================================

MCP INTEGRATION BEST PRACTICES
-------------------------------

### 1. Server Selection

```typescript
// اختر الخوادم المناسبة لاحتياجك
{
  "development": ["playwright", "context7"],
  "testing": ["playwright", "github"],
  "production": ["github"],
  "documentation": ["context7"]
}
```

### 2. Configuration Management

```bash
# استخدم ملفات تكوين منفصلة
.mcp/
├── development.json
├── testing.json
└── production.json

# لا ترفع secrets إلى Git
echo ".mcp/*.json" >> .gitignore
echo ".env" >> .gitignore
```

### 3. Error Handling

```typescript
{
  "errorHandling": {
    "retry": {
      "maxAttempts": 3,
      "backoff": "exponential"
    },
    "fallback": {
      "onTimeout": "skip_and_continue",
      "onError": "log_and_report"
    },
    "logging": {
      "level": "info",
      "destination": "logs/mcp.log"
    }
  }
}
```

### 4. Performance Optimization

```typescript
{
  "optimization": {
    "caching": {
      "enabled": true,
      "ttl": 3600,
      "storage": "memory"
    },
    "parallelization": {
      "maxConcurrent": 5,
      "queueSize": 100
    },
    "timeout": {
      "default": 30000,
      "navigation": 60000,
      "action": 5000
    }
  }
}
```

### 5. Security Guidelines

```typescript
{
  "security": {
    "tokens": {
      "storage": "environment_variables",
      "rotation": "90_days",
      "scope": "minimum_required"
    },
    "permissions": {
      "principle": "least_privilege",
      "review": "quarterly"
    },
    "audit": {
      "enabled": true,
      "logActions": true,
      "alertOnSuspicious": true
    }
  }
}
```

TESTING BEST PRACTICES
-----------------------

### 1. Test Organization

```typescript
{
  "testStructure": {
    "unit": "playwright/unit/",
    "integration": "playwright/integration/",
    "e2e": "playwright/e2e/",
    "security": "playwright/security/",
    "performance": "playwright/performance/"
  }
}
```

### 2. Test Data Management

```typescript
{
  "testData": {
    "fixtures": "fixtures/",
    "mocks": "mocks/",
    "seeds": "seeds/",
    "cleanup": "after_each_test"
  }
}
```

### 3. Reporting

```typescript
{
  "reporting": {
    "formats": ["html", "json", "junit"],
    "screenshots": "on_failure",
    "videos": "on_failure",
    "traces": "on_failure",
    "artifacts": "test-results/"
  }
}
```

### 4. CI/CD Integration

```yaml
# .github/workflows/mcp-tests.yml
name: MCP Testing
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install Playwright
        run: |
          npm install -D @playwright/test
          npx playwright install --with-deps
      
      - name: Run MCP Tests
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: npx playwright test
      
      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results/
      
      - name: Report to GitHub
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'MCP Test Failure',
              body: 'Automated tests failed. See artifacts.'
            })
```

TROUBLESHOOTING
---------------

### Common Issues

1. **Connection Timeout**
   ```bash
   # زيادة timeout
   npx @playwright/mcp@latest --timeout-navigation 120000
   ```

2. **Authentication Errors**
   ```bash
   # التحقق من token
   echo $GITHUB_PERSONAL_ACCESS_TOKEN
   
   # إعادة إنشاء token
   # https://github.com/settings/tokens
   ```

3. **Browser Launch Failures**
   ```bash
   # تثبيت dependencies
   npx playwright install-deps
   
   # استخدام no-sandbox
   npx @playwright/mcp@latest --no-sandbox
   ```

4. **Network Issues**
   ```bash
   # استخدام proxy
   npx @playwright/mcp@latest --proxy-server http://proxy:3128
   
   # تجاوز domains معينة
   npx @playwright/mcp@latest --proxy-bypass ".com,.org"
   ```

RESOURCES
---------

### Official Documentation
- Playwright MCP: https://github.com/microsoft/playwright-mcp
- Context7: https://github.com/upstash/context7
- GitHub MCP: https://github.com/github/github-mcp-server
- MCP Protocol: https://modelcontextprotocol.io

### Community Resources
- MCP Registry: https://github.com/mcp
- MCP Servers: https://github.com/modelcontextprotocol/servers
- Examples: https://modelcontextprotocol.io/examples

### Tools and Extensions
- VS Code MCP: https://code.visualstudio.com/docs/copilot/customization/mcp-servers
- Claude Desktop: https://claude.ai/download
- Cursor: https://cursor.sh

================================================================================
END OF MODULE 15: MCP INTEGRATION
================================================================================




================================================================================
SECTION 6: CODE ANALYSIS MCP SERVERS
================================================================================

OVERVIEW
--------
Code analysis tools help maintain code quality, detect errors, and improve.
الأداء. هذه الأدوات ضرورية لأي مشروع احترافي.

### 6.1 RUFF MCP SERVER

OVERVIEW
--------
Ruff is a very fast Python linter and code formatter written in the Rust language.
يوفر MCP server للتكامل مع أدوات AI.

Repository: https://github.com/Anselmoo/mcp-server-analyzer
Package: ruff-mcp-server

KEY FEATURES
------------

1. **Ultra-Fast Performance**
   - 10-100x أسرع من Flake8
   - مكتوب بلغة Rust
   - معالجة متوازية

2. **Comprehensive Linting**
   - 800+ قاعدة linting
   - دعم Flake8, pylint, pycodestyle
   - اكتشاف dead code مع VULTURE
   - type checking hints

3. **Auto-Fixing**
   - إصلاح تلقائي للمشاكل
   - safe و unsafe fixes
   - bulk fixing

4. **Code Formatting**
   - متوافق مع Black
   - configurable style
   - fast formatting

INSTALLATION
------------

```bash
# تثبيت Ruff
pip install ruff

# تثبيت MCP server
npm install -g ruff-mcp-server

# أو استخدام npx
npx ruff-mcp-server
```

CONFIGURATION
-------------

### VS Code Configuration

```json
{
  "mcpServers": {
    "ruff": {
      "command": "npx",
      "args": ["ruff-mcp-server"],
      "env": {
        "RUFF_CONFIG": ".ruff.toml"
      }
    }
  }
}
```

### Ruff Configuration (.ruff.toml)

```toml
[tool.ruff]
# Python version
target-version = "py311"

# Line length
line-length = 88

# Enable rules
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

# Ignore specific rules
ignore = [
    "E501",  # line too long
    "B008",  # function calls in argument defaults
]

# Exclude directories
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # unused imports in __init__.py
"tests/**/*.py" = ["S101"]  # assert usage in tests
```

AVAILABLE TOOLS
---------------

### 1. lint_code

فحص الكود وإرجاع المشاكل

```python
{
  "tool": "ruff.lint_code",
  "arguments": {
    "file_path": "src/main.py",
    "fix": false
  }
}
```

### 2. format_code

تنسيق الكود

```python
{
  "tool": "ruff.format_code",
  "arguments": {
    "file_path": "src/main.py",
    "check": false
  }
}
```

### 3. check_project

فحص المشروع كاملاً

```python
{
  "tool": "ruff.check_project",
  "arguments": {
    "directory": "src/",
    "fix": true,
    "show_fixes": true
  }
}
```

### 4. find_dead_code

اكتشاف الكود غير المستخدم

```python
{
  "tool": "ruff.find_dead_code",
  "arguments": {
    "directory": "src/",
    "min_confidence": 80
  }
}
```

USE CASES
---------

### 1. Pre-Commit Linting

```bash
# إضافة إلى .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: 
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
```

### 2. CI/CD Integration

```yaml
# .github/workflows/lint.yml
name: Lint
on: [push, pull_request]

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: chartboost/ruff-action@v1
        with:
          args: check --output-format=github
```

### 3. Automated Code Review

```typescript
{
  "workflow": [
    {
      "tool": "github.list_pull_requests",
      "args": {"state": "open"}
    },
    {
      "tool": "github.get_pull_request_diff",
      "args": {"pull_number": 123}
    },
    {
      "tool": "ruff.lint_code",
      "args": {"file_path": "changed_file.py", "fix": true}
    },
    {
      "tool": "github.add_issue_comment",
      "args": {
        "issue_number": 123,
        "body": "Ruff found and fixed issues"
      }
    }
  ]
}
```

---

### 6.2 ESLINT MCP SERVER

OVERVIEW
--------
ESLint هو linter قابل للتخصيص لـ JavaScript و TypeScript.
يساعد في اكتشاف المشاكل وفرض معايير البرمجة.

Repository: https://github.com/eslint/eslint
MCP Documentation: https://eslint.org/docs/latest/use/mcp

KEY FEATURES
------------

1. **Pluggable Architecture**
   - 300+ قواعد مدمجة
   - آلاف الـ plugins
   - قواعد مخصصة

2. **Auto-Fixing**
   - إصلاح تلقائي للمشاكل
   - safe fixes فقط
   - configurable

3. **TypeScript Support**
   - دعم كامل لـ TypeScript
   - type-aware rules
   - @typescript-eslint plugin

4. **Framework Integration**
   - React, Vue, Angular
   - Next.js, Nuxt
   - custom frameworks

INSTALLATION
------------

```bash
# تثبيت ESLint
npm install -D eslint

# تثبيت MCP server
npm install -g @eslint/mcp-server

# Initialize config
npx eslint --init
```

CONFIGURATION
-------------

### VS Code Configuration

```json
{
  "mcpServers": {
    "eslint": {
      "command": "npx",
      "args": ["@eslint/mcp-server"]
    }
  }
}
```

### ESLint Configuration (eslint.config.js)

```javascript
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';
import react from 'eslint-plugin-react';

export default [
  js.configs.recommended,
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    plugins: {
      '@typescript-eslint': typescript,
      'react': react
    },
    rules: {
      'no-unused-vars': 'error',
      'no-console': 'warn',
      '@typescript-eslint/no-explicit-any': 'error',
      'react/prop-types': 'off'
    },
    settings: {
      react: {
        version: 'detect'
      }
    }
  }
];
```

AVAILABLE TOOLS
---------------

### 1. lint_file

فحص ملف واحد

```javascript
{
  "tool": "eslint.lint_file",
  "arguments": {
    "file_path": "src/App.tsx",
    "fix": false
  }
}
```

### 2. lint_directory

فحص مجلد

```javascript
{
  "tool": "eslint.lint_directory",
  "arguments": {
    "directory": "src/",
    "extensions": [".js", ".jsx", ".ts", ".tsx"],
    "fix": true
  }
}
```

### 3. get_config

الحصول على التكوين

```javascript
{
  "tool": "eslint.get_config",
  "arguments": {
    "file_path": "src/App.tsx"
  }
}
```

USE CASES
---------

### 1. Pre-Commit Hook

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "git add"
    ]
  }
}
```

### 2. CI/CD Integration

```yaml
# .github/workflows/lint.yml
name: ESLint
on: [push, pull_request]

jobs:
  eslint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx eslint . --ext .js,.jsx,.ts,.tsx
```

---

### 6.3 CODE ANALYSIS MCP SERVER

OVERVIEW
--------
خادم شامل لتحليل الكود يدعم لغات متعددة ويوفر رؤى عميقة.

Repository: https://github.com/saiprashanths/code-analysis-mcp
Features: Multi-language, Deep analysis, Security scanning

KEY FEATURES
------------

1. **Multi-Language Support**
   - Python, JavaScript, TypeScript
   - Go, Rust, Java
   - C/C++, C#

2. **Deep Analysis**
   - Complexity metrics
   - Code smells
   - Design patterns
   - Architecture analysis

3. **Security Scanning**
   - Vulnerability detection
   - Dependency scanning
   - OWASP Top 10
   - CWE database

4. **Performance Analysis**
   - Bottleneck detection
   - Memory leaks
   - CPU profiling
   - Optimization suggestions

INSTALLATION
------------

```bash
# تثبيت via npm
npm install -g code-analysis-mcp

# أو Docker
docker run -i --rm code-analysis-mcp
```

CONFIGURATION
-------------

```json
{
  "mcpServers": {
    "code-analysis": {
      "command": "npx",
      "args": ["code-analysis-mcp"],
      "env": {
        "ANALYSIS_DEPTH": "deep",
        "SECURITY_SCAN": "true"
      }
    }
  }
}
```

AVAILABLE TOOLS
---------------

### 1. analyze_codebase

تحليل شامل للمشروع

```javascript
{
  "tool": "code-analysis.analyze_codebase",
  "arguments": {
    "directory": "src/",
    "depth": "deep",
    "include_security": true,
    "include_performance": true
  }
}
```

### 2. find_code_smells

اكتشاف code smells

```javascript
{
  "tool": "code-analysis.find_code_smells",
  "arguments": {
    "file_path": "src/legacy.py",
    "severity": "medium"
  }
}
```

### 3. security_scan

فحص أمني

```javascript
{
  "tool": "code-analysis.security_scan",
  "arguments": {
    "directory": "src/",
    "check_dependencies": true,
    "owasp_check": true
  }
}
```

### 4. complexity_metrics

قياس التعقيد

```javascript
{
  "tool": "code-analysis.complexity_metrics",
  "arguments": {
    "file_path": "src/complex.py",
    "metrics": ["cyclomatic", "cognitive", "halstead"]
  }
}
```

USE CASES
---------

### Complete Code Review Workflow

```typescript
{
  "workflow": [
    // 1. تحليل الكود
    {
      "tool": "code-analysis.analyze_codebase",
      "args": {"directory": "src/", "depth": "deep"}
    },
    // 2. فحص أمني
    {
      "tool": "code-analysis.security_scan",
      "args": {"directory": "src/", "owasp_check": true}
    },
    // 3. Lint Python
    {
      "tool": "ruff.check_project",
      "args": {"directory": "src/", "fix": true}
    },
    // 4. Lint JavaScript
    {
      "tool": "eslint.lint_directory",
      "args": {"directory": "src/", "fix": true}
    },
    // 5. إنشاء تقرير
    {
      "tool": "github.create_issue",
      "args": {
        "title": "Code Analysis Report",
        "body": "Analysis results...",
        "labels": ["code-quality"]
      }
    }
  ]
}
```

================================================================================
SECTION 7: TASK MANAGEMENT MCP SERVERS
================================================================================

OVERVIEW
--------
Task management tools assist in organizing work, tracking progress, and automating workflows.

### 7.1 TASK QUEUE MCP SERVER

OVERVIEW
--------
Advanced task management system for AI assistants with support for priorities and scheduling.

Repository: https://github.com/chriscarrollsmith/taskqueue-mcp
Package: taskqueue-mcp

KEY FEATURES
------------

1. **Priority Queue**
   - مهام ذات أولويات
   - FIFO, LIFO, Priority-based
   - Dynamic re-prioritization

2. **Task Scheduling**
   - جدولة المهام
   - Recurring tasks
   - Deadline management

3. **Task Dependencies**
   - تبعيات بين المهام
   - Parallel execution
   - Sequential workflows

4. **Progress Tracking**
   - تتبع التقدم
   - Status updates
   - Completion notifications

INSTALLATION
------------

```bash
# تثبيت via npm
npm install -g taskqueue-mcp

# تشغيل الخادم
npx taskqueue-mcp
```

CONFIGURATION
-------------

```json
{
  "mcpServers": {
    "taskqueue": {
      "command": "npx",
      "args": ["taskqueue-mcp"],
      "env": {
        "QUEUE_TYPE": "priority",
        "MAX_CONCURRENT": "5"
      }
    }
  }
}
```

AVAILABLE TOOLS
---------------

### 1. add_task

إضافة مهمة جديدة

```javascript
{
  "tool": "taskqueue.add_task",
  "arguments": {
    "title": "Fix login bug",
    "description": "User reported login issue",
    "priority": "high",
    "deadline": "2025-01-10",
    "tags": ["bug", "urgent"]
  }
}
```

### 2. list_tasks

قائمة المهام

```javascript
{
  "tool": "taskqueue.list_tasks",
  "arguments": {
    "status": "pending",
    "priority": "high",
    "sort_by": "deadline"
  }
}
```

### 3. update_task

تحديث مهمة

```javascript
{
  "tool": "taskqueue.update_task",
  "arguments": {
    "task_id": "123",
    "status": "in_progress",
    "progress": 50
  }
}
```

### 4. complete_task

إكمال مهمة

```javascript
{
  "tool": "taskqueue.complete_task",
  "arguments": {
    "task_id": "123",
    "notes": "Fixed and tested"
  }
}
```

### 5. schedule_task

جدولة مهمة

```javascript
{
  "tool": "taskqueue.schedule_task",
  "arguments": {
    "task_id": "123",
    "schedule": "daily",
    "time": "09:00",
    "timezone": "UTC"
  }
}
```

USE CASES
---------

### 1. Bug Tracking Workflow

```typescript
{
  "workflow": [
    // 1. إنشاء مهمة من GitHub issue
    {
      "tool": "github.list_issues",
      "args": {"state": "open", "labels": "bug"}
    },
    {
      "tool": "taskqueue.add_task",
      "args": {
        "title": "Fix bug #123",
        "priority": "high",
        "source": "github"
      }
    },
    // 2. تعيين للمطور
    {
      "tool": "taskqueue.assign_task",
      "args": {"task_id": "123", "assignee": "developer@example.com"}
    },
    // 3. تتبع التقدم
    {
      "tool": "taskqueue.update_task",
      "args": {"task_id": "123", "status": "in_progress"}
    }
  ]
}
```

### 2. Daily Standup Automation

```typescript
{
  "workflow": [
    // قائمة المهام المكتملة أمس
    {
      "tool": "taskqueue.list_tasks",
      "args": {
        "status": "completed",
        "completed_after": "yesterday"
      }
    },
    // قائمة المهام لليوم
    {
      "tool": "taskqueue.list_tasks",
      "args": {
        "status": "pending",
        "priority": "high"
      }
    },
    // إرسال تقرير
    {
      "tool": "slack.send_message",
      "args": {
        "channel": "#standup",
        "text": "Daily standup report"
      }
    }
  ]
}
```

---

### 7.2 PRODUCTIVITY MCP SERVERS

OVERVIEW
--------
مجموعة من الأدوات لزيادة الإنتاجية وأتمتة المهام اليومية.

#### Amazing Marvin MCP

```json
{
  "server": "amazing-marvin",
  "features": [
    "Task management",
    "Time tracking",
    "Habit tracking",
    "Goal setting"
  ]
}
```

#### Todoist MCP

```json
{
  "server": "todoist",
  "features": [
    "Task lists",
    "Projects",
    "Labels and filters",
    "Reminders"
  ]
}
```

#### Notion MCP

```json
{
  "server": "notion",
  "features": [
    "Database management",
    "Page creation",
    "Content search",
    "Team collaboration"
  ]
}
```

INTEGRATION EXAMPLE
-------------------

```typescript
{
  "daily_workflow": [
    // 1. جمع المهام من مصادر متعددة
    {
      "tool": "github.list_issues",
      "args": {"assignee": "me", "state": "open"}
    },
    {
      "tool": "notion.query_database",
      "args": {"database_id": "tasks"}
    },
    // 2. دمج في task queue
    {
      "tool": "taskqueue.bulk_add_tasks",
      "args": {"tasks": "collected_tasks"}
    },
    // 3. ترتيب حسب الأولوية
    {
      "tool": "taskqueue.prioritize_tasks",
      "args": {"algorithm": "eisenhower_matrix"}
    },
    // 4. إنشاء خطة اليوم
    {
      "tool": "taskqueue.create_daily_plan",
      "args": {"max_tasks": 5}
    }
  ]
}
```

================================================================================
SECTION 8: MONITORING & ERROR TRACKING
================================================================================

### 8.1 SENTRY MCP SERVER

OVERVIEW
--------
Sentry MCP provides complete integration with the Sentry platform for error and performance tracking.

Repository: MCP Registry (configured in user environment)
Features: Error tracking, Performance monitoring, Issue management

KEY FEATURES
------------

1. **Error Monitoring**
   - Real-time error tracking
   - Stack traces
   - User context
   - Breadcrumbs

2. **Performance Monitoring**
   - Transaction tracking
   - Slow queries
   - API monitoring
   - Frontend performance

3. **Issue Management**
   - Automatic grouping
   - Assignment
   - Resolution tracking
   - Release tracking

4. **Alerts & Notifications**
   - Custom alerts
   - Slack/Email integration
   - Threshold-based
   - Anomaly detection

AVAILABLE TOOLS
---------------

### 1. list_issues

قائمة المشاكل

```javascript
{
  "tool": "sentry.list_issues",
  "arguments": {
    "project": "my-app",
    "status": "unresolved",
    "level": "error"
  }
}
```

### 2. get_issue_details

تفاصيل مشكلة

```javascript
{
  "tool": "sentry.get_issue_details",
  "arguments": {
    "issue_id": "123456"
  }
}
```

### 3. resolve_issue

حل مشكلة

```javascript
{
  "tool": "sentry.resolve_issue",
  "arguments": {
    "issue_id": "123456",
    "resolution": "fixed",
    "release": ""
  }
}
```

### 4. get_performance_metrics

مقاييس الأداء

```javascript
{
  "tool": "sentry.get_performance_metrics",
  "arguments": {
    "project": "my-app",
    "timeframe": "24h",
    "metrics": ["apdex", "throughput", "p95"]
  }
}
```

USE CASES
---------

### Automated Error Response

```typescript
{
  "workflow": [
    // 1. مراقبة الأخطاء الجديدة
    {
      "tool": "sentry.list_issues",
      "args": {"status": "unresolved", "age": "1h"}
    },
    // 2. تحليل الخطأ
    {
      "tool": "sentry.get_issue_details",
      "args": {"issue_id": "123"}
    },
    // 3. البحث عن حلول مشابهة
    {
      "tool": "github.search_code",
      "args": {"query": "error_message"}
    },
    // 4. إنشاء issue في GitHub
    {
      "tool": "github.create_issue",
      "args": {
        "title": "Sentry Error: ...",
        "body": "Stack trace...",
        "labels": ["bug", "sentry"]
      }
    },
    // 5. إضافة مهمة
    {
      "tool": "taskqueue.add_task",
      "args": {
        "title": "Fix Sentry error",
        "priority": "high"
      }
    }
  ]
}
```

================================================================================
SECTION 9: INFRASTRUCTURE & CLOUD
================================================================================

### 9.1 CLOUDFLARE MCP SERVER

OVERVIEW
--------
Integration with Cloudflare Workers Bindings for accessing Cloudflare services.

Repository: MCP Registry (configured in user environment)
Features: D1, R2, KV, Workers, Pages

KEY FEATURES
------------

1. **D1 Database**
   - SQL database
   - Serverless
   - Global replication

2. **R2 Storage**
   - Object storage
   - S3-compatible
   - No egress fees

3. **KV Store**
   - Key-value storage
   - Edge caching
   - Global distribution

4. **Workers**
   - Serverless functions
   - Edge computing
   - Low latency

AVAILABLE TOOLS
---------------

### 1. d1_query

استعلام D1

```javascript
{
  "tool": "cloudflare.d1_query",
  "arguments": {
    "database": "my-db",
    "query": "SELECT * FROM users WHERE active = 1"
  }
}
```

### 2. r2_upload

رفع إلى R2

```javascript
{
  "tool": "cloudflare.r2_upload",
  "arguments": {
    "bucket": "my-bucket",
    "key": "file.pdf",
    "content": "base64_content"
  }
}
```

### 3. kv_get

قراءة من KV

```javascript
{
  "tool": "cloudflare.kv_get",
  "arguments": {
    "namespace": "my-kv",
    "key": "config"
  }
}
```

### 4. deploy_worker

نشر Worker

```javascript
{
  "tool": "cloudflare.deploy_worker",
  "arguments": {
    "name": "my-worker",
    "script": "worker_code.js"
  }
}
```

================================================================================
SECTION 10: ADVANCED MCP PATTERNS
================================================================================

SEQUENTIAL THINKING MCP
-----------------------

يساعد في تقسيم المشاكل المعقدة إلى خطوات قابلة للإدارة.

```typescript
{
  "pattern": "sequential_thinking",
  "steps": [
    {
      "step": 1,
      "action": "understand_problem",
      "tool": "context7.get_documentation"
    },
    {
      "step": 2,
      "action": "analyze_code",
      "tool": "code-analysis.analyze_codebase"
    },
    {
      "step": 3,
      "action": "identify_issues",
      "tool": "ruff.lint_code"
    },
    {
      "step": 4,
      "action": "create_tasks",
      "tool": "taskqueue.add_task"
    },
    {
      "step": 5,
      "action": "execute_fixes",
      "tool": "playwright.browser_navigate"
    },
    {
      "step": 6,
      "action": "verify_solution",
      "tool": "playwright.browser_snapshot"
    }
  ]
}
```

COMPLETE PROJECT WORKFLOW
--------------------------

```typescript
{
  "project_workflow": {
    "name": "Complete Development Cycle",
    "phases": [
      {
        "phase": "Planning",
        "tools": [
          "taskqueue.create_project",
          "notion.create_database",
          "github.create_repository"
        ]
      },
      {
        "phase": "Development",
        "tools": [
          "context7.get_documentation",
          "code-analysis.analyze_codebase",
          "ruff.lint_code",
          "eslint.lint_directory"
        ]
      },
      {
        "phase": "Testing",
        "tools": [
          "playwright.browser_navigate",
          "playwright.browser_snapshot",
          "playwright.browser_network_requests"
        ]
      },
      {
        "phase": "Deployment",
        "tools": [
          "cloudflare.deploy_worker",
          "github.create_release"
        ]
      },
      {
        "phase": "Monitoring",
        "tools": [
          "sentry.list_issues",
          "sentry.get_performance_metrics"
        ]
      }
    ]
  }
}
```

BEST PRACTICES
--------------

### 1. Tool Selection

```typescript
{
  "guidelines": {
    "code_quality": ["ruff", "eslint", "code-analysis"],
    "task_management": ["taskqueue", "notion", "github"],
    "testing": ["playwright", "context7"],
    "monitoring": ["sentry", "cloudflare"],
    "documentation": ["context7", "github"]
  }
}
```

### 2. Error Handling

```typescript
{
  "error_handling": {
    "retry": {
      "max_attempts": 3,
      "backoff": "exponential"
    },
    "fallback": {
      "primary": "ruff",
      "secondary": "pylint",
      "tertiary": "flake8"
    },
    "logging": {
      "tool": "sentry",
      "level": "error"
    }
  }
}
```

### 3. Performance Optimization

```typescript
{
  "optimization": {
    "parallel_execution": [
      "ruff.lint_code",
      "eslint.lint_directory",
      "code-analysis.security_scan"
    ],
    "caching": {
      "tool": "cloudflare.kv",
      "ttl": 3600
    },
    "batch_operations": {
      "tool": "taskqueue.bulk_add_tasks",
      "batch_size": 100
    }
  }
}
```

================================================================================
RESOURCES
================================================================================

### Official MCP Resources
- MCP Protocol: https://modelcontextprotocol.io
- MCP Registry: https://github.com/punkpeye/awesome-mcp-servers
- MCP Servers: https://github.com/modelcontextprotocol/servers

### Code Analysis Tools
- Ruff: https://github.com/astral-sh/ruff
- ESLint: https://eslint.org
- Code Analysis MCP: https://github.com/saiprashanths/code-analysis-mcp

### Task Management
- Task Queue MCP: https://github.com/chriscarrollsmith/taskqueue-mcp
- Notion API: https://developers.notion.com
- Todoist API: https://developer.todoist.com

### Monitoring & Infrastructure
- Sentry: https://sentry.io
- Cloudflare: https://developers.cloudflare.com

### Community
- Reddit r/mcp: https://reddit.com/r/mcp
- Discord: https://discord.gg/mcp
- Glama.ai: https://glama.ai/mcp/servers

================================================================================
END OF MODULE 15: MCP INTEGRATION (EXTENDED)
================================================================================

