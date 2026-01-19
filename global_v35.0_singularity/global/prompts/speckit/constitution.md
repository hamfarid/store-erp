# /speckit.constitution

**Goal:** Create or update the project's governing principles, development guidelines, and architectural vision.

**Input:**
*   Project Mission/Description (from User)
*   Existing README.md (if Adoption Mode)
*   Global System Rules (`global/rules/*.md`)
*   Global System Roles (`global/roles/*.md`)

**Output:** `CONSTITUTION.md`

**Instructions:**
1.  **Adopt the Persona:** You are **The Architect** and **The Lawmaker**.
2.  **Analyze Context:** Read the input materials. Understand the "Spirit" of the project.
3.  **Define Principles:**
    *   What are the non-negotiable rules? (e.g., "Security First", "Mobile Responsive").
    *   What is the architectural style? (e.g., "Microservices", "Monolith", "Event-Driven").
4.  **Integrate Global Rules:** Explicitly reference `global/rules/` (e.g., "Must adhere to 103_librarian_protocol.md").
5.  **Define Roles:** List the key roles (Builder, QA, Shadow) and their responsibilities in this specific project.
6.  **Write the Constitution:** Create a document that serves as the "Supreme Law" for all subsequent development.

**Template:**
```markdown
# Project Constitution: [Project Name]

## 1. Vision & Mission
[Clear statement of purpose]

## 2. Core Principles (The Non-Negotiables)
*   [Principle 1]
*   [Principle 2]
*   ...

## 3. Architectural Guidelines
*   **Tech Stack:** [Stack]
*   **Pattern:** [Pattern]

## 4. System Integration
*   This project operates under the **Global System v34.0**.
*   All code must pass the **Librarian Protocol**.
*   All specs must follow **SDD (Spec-Driven Development)**.

## 5. Roles & Responsibilities
*   **Architect:** [Name/AI]
*   **Builder:** [Name/AI]
*   ...
```
