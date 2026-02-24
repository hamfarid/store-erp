# MCP Security Rules
 (v26.0.2 Diamond 32 GAARA AI)

> **Standard**: Model Context Protocol (MCP) Security Specification (Nov 2025)
> **Enforcement**: Mandatory for all MCP Server integrations.

## 1. Authentication & Authorization

### 1.1 OAuth 2.1 Mandate
*   **Requirement**: All MCP servers accessing user data MUST use OAuth 2.1.
*   **Prohibited**: Static API keys in configuration files (except for local development with `.env`).
*   **Flow**: Use the Authorization Code Flow with PKCE for all user-facing integrations.

### 1.2 Least Privilege Scopes
*   **Principle**: Request only the scopes absolutely necessary for the task.
*   **Review**: Scopes must be reviewed and approved by the user before connection.
*   **Example**:
    *   ✅ `repo:read` (if only reading code)
    *   ❌ `repo` (full access)

## 2. Data Handling

### 2.1 No Data Persistence
*   **Rule**: MCP servers should be stateless whenever possible.
*   **Exception**: Caching (must be encrypted and ephemeral).
*   **Prohibited**: Storing user code or data in long-term storage without explicit consent.

### 2.2 Input Validation
*   **Sanitization**: All inputs to MCP tools must be sanitized to prevent injection attacks.
*   **Validation**: Use Pydantic (Python) or Zod (TypeScript) for strict schema validation.

## 3. Network Security

### 3.1 Transport Security
*   **Requirement**: All MCP communication must occur over TLS 1.3+.
*   **Localhost**: Local connections must use secure IPC or verified localhost bindings.

### 3.2 Server Isolation
*   **Sandboxing**: MCP servers should run in isolated environments (Docker containers or sandboxed processes).
*   **Network Policy**: Restrict outbound network access to only required endpoints.

## 4. Error Handling & Logging

### 4.1 Safe Logging
*   **Rule**: Never log sensitive data (tokens, PII, code snippets).
*   **Masking**: Automatically mask secrets in logs.

### 4.2 Error Messages
*   **Sanitization**: Do not expose internal stack traces or system paths to the LLM or user.
*   **Standard**: Return structured error objects defined in the MCP spec.

## 5. Compliance Checklist

- [ ] OAuth 2.1 implemented?
- [ ] Scopes minimized?
- [ ] Input validation active?
- [ ] TLS 1.3 enforced?
- [ ] Logs sanitized?
- [ ] Server sandboxed?
