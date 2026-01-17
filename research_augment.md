# Augment Rules Research - Official Documentation

## Source
- URL: https://docs.augmentcode.com/setup-augment/guidelines
- Date: November 4, 2025

## Key Findings

### What are Rules & Guidelines?

Agent and Chat rules and guidelines are **natural language instructions** that help Augment reply with more accurate and relevant responses.

### Types of Rules

Augment supports **3 types of rules**:

1. **Always**: Contents will be included in **every user prompt**
2. **Manual**: Needs to be tagged through **@ attaching** the Rules file manually
3. **Auto**: Agent will **automatically detect and attach** rules based on a **description field**

### File Location

Rules are files that live in the **`.augment/rules`** directory.

**Format:** Markdown files (`.md` or `.mdx`)

### How Augment Imports Rules

- Augment will **automatically import rules** if they are detected in the current workspace
- Augment looks for markdown files ending with `*.md` or `*.mdx`
- Can also manually import rules inside of Settings > Import rules

### User Guidelines vs Rules

**User Guidelines:**
- Stored **locally in your IDE**
- Will be applied to **all future chats** in that IDE
- Guidelines defined in VSCode will **not propagate** to JetBrains IDEs and vice versa
- Maximum: 24,576 characters

**Rules:**
- Stored within the **repository** under `.augment/rules`
- Allow you to split up guidelines into **multiple files**
- Maximum: 49,512 characters (combined with Workspace Guidelines)

### Workspace Guidelines (Legacy)

- File: `.augment-guidelines` in the **root of repository**
- Legacy system (being replaced by Rules)
- Augment will automatically import Workspace Guidelines as Rules

### Availability

- **VSCode:** Guidelines available in plugin version 0.492.0 and above
- **JetBrains IDEs:** Guidelines available in plugin version 0.197.0 and above
- **Rules:** Not yet available in JetBrains IDEs (VSCode only)

### How to Add User Guidelines

1. @ mention and select `User Guidelines`
2. Enter your guidelines
3. Press Escape to save or wait for autosave

OR

1. In the top right corner, select the hamburger menu (⋯)
2. Select Settings
3. From the left menu in Augment Settings, select User Guidelines and Rules

### Tips for Good Rules and Guidelines

- Provide guidelines as a **list**
- Use **simple, clear, and concise** language
- Asking for shorter or code-only answers may **hurt response quality**

### Examples

**User Guideline Examples:**
- Ask for additional explanation e.g. `For Typescript code, explain what the code is doing in more detail`
- Set a preferred language e.g. `Respond to questions in Spanish`

**Rule Examples:**
- Add links to Google Docs, Notion or Confluence files
- Point to specific documentation e.g. `Python 3.13.5`
- Outline templates or example code
- Establish consistent frameworks, coding styles, and architectural patterns
- Provide examples on codebase style

**Workspace Guideline Examples:**
- Identifying preferred libraries e.g. `pytest vs unittest`
- Identifying specific patterns e.g. `For NextJS, use the App Router and server components`
- Rejecting specific anti-patterns e.g. `a deprecated internal module`
- Defining naming conventions e.g. `functions start with verbs`

### Current Limitations

- User Guidelines: Maximum 24,576 characters
- Workspace Guidelines + Rules: Maximum 49,512 characters
- If limits exceeded, applied in order: (manual rules, always + auto rules, .augment-guidelines)
- Rules not yet available in JetBrains IDEs

### What Guidelines/Rules Do NOT Apply To

- Completions
- Instructions
- Next Edit

They **only apply to Agent and Chat**.

---

## CRITICAL FINDINGS

### ✅ CORRECT: Our Implementation

1. **File location:** `.augment/rules/` ✅
2. **File format:** Markdown (`.md`) ✅
3. **3 types:** Always, Auto, Manual ✅

### ❌ INCORRECT: Our Implementation

1. **Frontmatter format:** We used YAML-like frontmatter, but documentation doesn't specify this format
2. **Auto-detect field:** Documentation mentions "description field" for Auto rules, but doesn't show exact format
3. **File naming:** Documentation doesn't specify naming conventions

### 🔍 NEEDS VERIFICATION

1. **Exact frontmatter format** for rule types
2. **Auto-detect keywords** - how does Augment detect them?
3. **File naming conventions** - any specific requirements?

---

## Next Steps

1. Search for examples of Augment rules files
2. Find the exact frontmatter format
3. Verify auto-detect mechanism
4. Update our implementation if needed




---

## UPDATED FINDINGS - CLI Documentation

### Source
- URL: https://docs.augmentcode.com/cli/rules
- Date: November 4, 2025

### Frontmatter Configuration (OFFICIAL FORMAT)

**Rule Types:**

1. **`always_apply`**: Rule contents are automatically included in every user prompt
2. **`agent_requested`**: Rule is automatically detected and attached based on the description field when relevant
3. **`manual`**: Not yet supported in CLI (only works in IDE extensions with @ mentions)

### Frontmatter Format (YAML)

**Always Apply Example:**
```markdown
---
type: always_apply
---

# TypeScript Guidelines

- Use strict mode in all TypeScript files
- Define explicit return types for all functions
- Avoid using `any` type unless absolutely necessary
```

**Agent Requested (Auto) Example:**
```markdown
---
type: agent_requested
description: React component development patterns and best practices
---

# React Component Guidelines

- Use functional components with hooks
- Implement proper TypeScript interfaces for props
- Follow the established folder structure in src/components/
```

### Key Differences from Our Implementation

**Our Implementation:**
```markdown
**Type:** Always
**Purpose:** Define your core identity and principles
```

**Official Format:**
```yaml
---
type: always_apply
---
```

### ✅ CORRECT in Our Implementation
1. File location: `.augment/rules/` ✅
2. File format: Markdown (`.md`) ✅
3. Concept of 3 types ✅

### ❌ INCORRECT in Our Implementation
1. **Frontmatter format:** We used bold text instead of YAML frontmatter ❌
2. **Type names:** We used `Always`, `Auto`, `Manual` instead of `always_apply`, `agent_requested`, `manual` ❌
3. **Description field:** For `agent_requested`, we used `Auto-detect:` instead of `description:` in YAML ❌

### Supported Rules Files (Order of Precedence)

1. Custom rules file (via `--rules` flag)
2. `CLAUDE.md` (compatible with Claude Code)
3. `AGENTS.md` (compatible with Cursor)
4. `<workspace_root>/.augment/guidelines.md` (legacy)
5. `<workspace_root>/.augment/rules/` (recursively searches .md files)

### Best Practices

1. **Be Specific**: Provide clear, actionable guidelines
2. **Use Examples**: Include code examples
3. **Keep Updated**: Regularly review and update
4. **Be Concise**: Focus on most important guidelines
5. **Test Guidelines**: Verify that Auggie follows your rules

### Agent-Requested vs Always Apply

- Use `agent_requested` over `always_apply` to **optimize context usage**
- Agent will determine if rule is relevant to current task
- Ensures specialized guidelines are available when needed

---

## CONCLUSION

**We need to update our Augment rules files to use the correct YAML frontmatter format:**

1. Change from bold text format to YAML frontmatter
2. Change type names: `Always` → `always_apply`, `Auto` → `agent_requested`, `Manual` → `manual`
3. For agent_requested, use `description:` field in YAML
4. Remove `Auto-detect:` lines and replace with proper YAML `description:`

