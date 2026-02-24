# Onboarding Workflow (Global System v26 Diamond 32 Synchronized Intelligence Edition)

This workflow helps new developers (and AI agents) get up to speed with the project using the **Agentic Engine**.

## Steps

1. **Initialize the Agentic Engine**
   - **Command:** `python3 global/tools/lifecycle.py <project_name> "Initialize Global System v26 Diamond 32"`
   - This sets up the memory structure and logs the start.

2. **Read Core Documentation**
   - Read: `README.md`
   - Read: `global/prompts/GLOBAL_PROFESSIONAL_CORE_PROMPT_Global System v26 Diamond 32.md`
   - Read: `global/BOOTSTRAP.md`

3. **Set Up Development Environment**
   - Install dependencies: `pip install -r requirements.txt`
   - Set up environment variables (copy `.env.example` to `.env`)

4. **Run Speckit Analysis**
   - **Command:** `python3 global/tools/speckit.py analyze`
   - This maps the codebase and creates `project_memory.md`.

5. **Run Verification**
   - **Command:** `python3 global/tools/speckit.py verify`
   - Ensure the codebase is clean (Sentinel Check).

6. **Complete a Starter Task**
   - Pick a task from `todo.md`.
   - Use `speckit.py implement` to execute it.

7. **Review Team Workflows**
   - Understand the **Zero-Error Policy**.
   - Learn the **Sequential Thinking** process.
