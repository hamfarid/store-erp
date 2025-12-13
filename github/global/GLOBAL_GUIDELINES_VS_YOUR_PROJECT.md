# ⚠️ IMPORTANT DISTINCTION: Global Guidelines vs. Your Project

This document clarifies the critical distinction between **Global Guidelines** (this repository) and **Your Project** (the codebase you are building).

---

## 🎯 What is Global Guidelines?

Global Guidelines is a **comprehensive AI development prompt system**. It is **NOT** your project. It is an instruction manual that tells the AI agent **HOW** to work.

**Think of it this way:**
- **Global Guidelines:** The cookbook with recipes and techniques.
- **Your Project:** The actual meal you are cooking.

---

## 📁 Folder Structure Explained

### Global Guidelines Repository (`github/global/`)

This is the instruction manual. It contains:

- `prompts/`: AI guidance modules (the "recipes"). **The AI reads these.**
- `examples/`: Reference examples for learning.
- `knowledge/`: A library of verified facts and solutions.
- `rules/`: Non-negotiable coding standards.
- `workflows/`: Pre-defined multi-step tasks.
- `.memory/`: The AI agent's working memory.
- `system_log.md`: The AI agent's action log.

### Your Project (e.g., `my-project/`)

This is the actual application you are building. It contains:

- `src/`: Your actual source code.
- `tests/`: Your actual tests.
- `docs/`: Your project's documentation.
- `package.json` or `requirements.txt`: Your project's dependencies.
- `.env`: Your project's environment variables.

---

## 🔒 CRITICAL: Environment Separation

**Global Guidelines and Your Project MUST have SEPARATE environments.** This is the most important rule to prevent conflicts and data corruption.

| Environment | Global Guidelines (`github/global/`) | Your Project (e.g., `my-project/`) |
|---|---|---|
| **Purpose** | The AI's instruction manual & tools | The user's actual application |
| **Database**| For the AI's tools only (e.g., `.memory/`) | The application's database (e.g., PostgreSQL) |
| **Docker** | For the AI's tools only | The application's containers |
| **Config** | For the AI's tools only | The application's configuration (`.env`) |

### What this means in practice:

- **DO NOT** use the `github/global/.memory/` directory to store user data for your project.
- **DO NOT** use the `github/global/system_log.md` to log application events. Create a separate logging system for your project.
- **DO NOT** use the `github/global/` Docker setup for your project. Create a `docker-compose.yml` inside your project directory.
- **DO NOT** store your project's API keys or database URLs in the `github/global/` environment.

**Always create a completely separate, self-contained environment for your project.**

### Example of Correct Separation:

**Global Guidelines (AI's Brain):**
- `~/github/global/.memory/`
- `~/github/global/system_log.md`

**Your Project (User's Application):**
- `~/my-project/src/`
- `~/my-project/db/app.db`
- `~/my-project/logs/app.log`
- `~/my-project/.env`

---

## 🚨 Common Mistakes to Avoid

1. ❌ **Confusing the two:** Thinking that `github/global/` is the project you are building.
   - ✅ **Correction:** `github/global/` is your instruction manual. Your project is in a separate directory.

2. ❌ **Modifying Global Guidelines:** Trying to "fix" or modify files in `github/global/`.
   - ✅ **Correction:** You should only read from `github/global/`. You write to your project directory.

3. ❌ **Mixing Environments:** Using the `github/global/` database or config for your project.
   - ✅ **Correction:** Always create a new, separate environment for your project.

4. ❌ **Including Global Guidelines in Analysis:** Running project analysis tools on the `github/global/` directory.
   - ✅ **Correction:** Only analyze your project's directory.

---

## 🎯 The Correct Workflow

1. **Receive a task** (e.g., `start-new-project`).
2. **Read the Core Prompt** (`GLOBAL_PROFESSIONAL_CORE_PROMPT.md`).
3. **Read the relevant prompts** from `github/global/prompts/`.
4. **Create a new directory** for the user's project (e.g., `mkdir my-project`).
5. **Work inside the new directory** (`cd my-project`).
6. **Apply the guidance** from Global Guidelines to the code you write in `my-project/`.
7. **Keep the two environments completely separate.**

---

By understanding and respecting this separation, you will avoid critical errors and build robust, reliable software correctly.

