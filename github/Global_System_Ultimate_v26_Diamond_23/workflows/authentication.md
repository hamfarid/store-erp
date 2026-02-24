# 🔐 Authentication Workflow (Global System Ultimate Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System Ultimate + Sentinel
**Status:** MANDATORY

## Workflow

```
Design (Speckit) → Implement (Speckit) → Verify (Sentinel)
```

## Phase 1: Design (Speckit)
1.  **Analyze:** Determine auth requirements (JWT, OAuth, Session).
2.  **Plan:** Define User Model and Auth Flow in `specs/auth.spec.md`.
3.  **Security First:** Plan for Hashing (Argon2), Rate Limiting, and HTTPS.

## Phase 2: Implement (Speckit)
1.  **Tasks:** Generate tasks for User Model, Login, Register, Logout.
2.  **Code:** Implement using TDD.
3.  **Constraint:** NEVER store plain-text passwords.

## Phase 3: Verify (Sentinel)
1.  **Sentinel Check:** Ensure no secrets (e.g., JWT_SECRET) are hardcoded.
2.  **CodeRabbit Check:** Verify hashing algorithms and token storage.
3.  **Penetration Test:** Run automated attacks (Brute Force, SQLi) using `speckit verify`.

## Remember
**Authentication is the gate. Make it strong.**
