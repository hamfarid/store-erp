# 🔌 API Development Workflow (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System v26 Diamond 32 (Agentic)
**Status:** MANDATORY

## 📋 Workflow Overview

```
Analyze (Speckit) → Plan (Speckit) → Implement (Speckit) → Verify (Sentinel)
```

## 🎯 Phase 1: Analyze & Design (Speckit)

### **Actions:**
1.  **Run Analysis:**
    ```bash
    python3 global/tools/speckit.py analyze
    ```
2.  **Define Spec:**
    *   Create `specs/api_feature.spec.md`.
    *   Define Endpoints, Methods, Request/Response schemas.
    *   Define Security Requirements (Auth, Rate Limiting).

## 🔧 Phase 2: Plan (Speckit)

### **Actions:**
1.  **Generate Plan:**
    ```bash
    python3 global/tools/speckit.py plan
    ```
2.  **Risk Assessment:**
    *   Identify potential security holes (SQLi, XSS).
    *   Define mitigation strategies in the plan.

## 💻 Phase 3: Implement (Speckit)

### **Actions:**
1.  **Generate Tasks:**
    ```bash
    python3 global/tools/speckit.py tasks
    ```
2.  **Execute Implementation:**
    ```bash
    python3 global/tools/speckit.py implement
    ```
    *   **Constraint:** TDD is mandatory. Write tests first.
    *   **Constraint:** Docstrings are mandatory.

## 🔒 Phase 4: Verify & Secure (Sentinel)

### **Actions:**
1.  **Run Verification:**
    ```bash
    python3 global/tools/speckit.py verify
    ```
    *   **Sentinel:** Checks for secrets and TODOs.
    *   **CodeRabbit:** Checks for code quality and security vulnerabilities.
    *   **Tests:** Runs `pytest` or `npm test`.

2.  **Documentation:**
    *   Auto-generate Swagger/OpenAPI docs.
    *   Update `global/system_log.md`.

## Remember
**An API is a contract. Do not break it.**
**Security is not optional. It is the law.**
