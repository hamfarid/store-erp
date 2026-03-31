# RULE 104: THE ANTI-HALLUCINATION OATH (v32.0)

## 🚫 The Problem
AI models often "guess" imports or function names (e.g., `from utils import helper` when `helper` doesn't exist).

## 1. The Oath
**Mandate:** Before writing code that imports a module or calls a function, you must verify its existence.
**Output:** You must include this line in your thinking block:
> `[Verification Oath] I have read 'path/to/file.py' and confirmed that class 'MyClass' exists.`

## 2. The "No Guessing" Law
*   **Forbidden:** `import pandas as pd` (unless you checked `requirements.txt`).
*   **Forbidden:** `user.get_full_name()` (unless you checked the `User` model definition).

## 3. The Penalty
If you hallucinate a function name, you must:
1.  **Stop** immediately.
2.  **Log** the error in `global/errors/hallucinations.md`.
3.  **Create** a meta-rule to prevent this specific hallucination again.
