# 🔌 Project Template: API-Only (Global System v26 Diamond 32)

**Status:** MANDATORY BLUEPRINT
**Enforcement:** Automated by Speckit (Plan Phase)

## 1. The Philosophy
An API is a contract. It must be strict, versioned, and documented.

## 2. The Mandatory Structure
```
api-project/
├── src/
│   ├── controllers/    # Logic
│   ├── models/         # Data
│   ├── routes/         # Endpoints
│   ├── middleware/     # Auth/Validation
│   ├── services/       # Business Logic
│   ├── utils/          # Helpers
│   ├── config/         # Env
│   └── app.js          # Entry
├── tests/              # Mandatory Tests
├── docs/               # OpenAPI
└── .env.example        # No Secrets
```

## 3. The Stack
*   **Runtime:** Node.js or Python.
*   **Framework:** Express or FastAPI.
*   **Auth:** JWT (Access + Refresh).
*   **Docs:** Swagger/OpenAPI (Auto-generated).

## 4. Security Mandates
1.  **Rate Limiting:** MANDATORY on all public routes.
2.  **Input Validation:** MANDATORY (Joi/Pydantic).
3.  **Sanitization:** MANDATORY (No SQL Injection).
4.  **Headers:** Helmet/CORS configured.

## 5. Testing
*   **Unit:** 80% Coverage.
*   **Integration:** Critical paths (Auth, Payments).
*   **E2E:** Happy path.
