# API Design & Development (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System v26 Diamond 32
**Status:** MANDATORY

## 📋 Overview
Comprehensive guidance for API design, development, and documentation, fully integrated with the Autonomous Engine.

## 🏗️ Design Principles (Speckit Plan)
1.  **Resource Naming:** Use nouns, plural, lowercase (e.g., `/api/products`).
2.  **Methods:** GET, POST, PUT, DELETE, PATCH.
3.  **Status Codes:** 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Server Error).
4.  **Versioning:** `/api/v1/resource`.

## 💻 Implementation (Speckit Implement)
*   **Frameworks:** FastAPI (Python), Express (Node.js).
*   **Validation:** Pydantic (Python), Zod (Node.js).
*   **Documentation:** OpenAPI/Swagger (Auto-generated).

## 🔒 Security (Sentinel Check)
*   **Authentication:** JWT (Stateless), OAuth2.
*   **Rate Limiting:** Redis-based (e.g., 100 req/min).
*   **Input Sanitization:** Prevent SQLi and XSS.

## 🧪 Verification (Speckit Verify)
*   **Unit Tests:** Test each endpoint in isolation.
*   **Integration Tests:** Test full flows (Register -> Login -> Create).
*   **Security Tests:** Check for IDOR, Broken Auth.

## 📄 Documentation
*   **Auto-Generate:** Use Swagger UI (`/docs`).
*   **Examples:** Provide curl examples for every endpoint.
