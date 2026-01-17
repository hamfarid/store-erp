# PROMPT 81: ERROR HANDLING

**Objective:** Implement a robust and consistent error handling system.

---

## 🎯 REQUIREMENTS

1.  **Custom Error Classes:** Create custom error classes for different types of errors (e.g., `ValidationError`, `AuthenticationError`).
2.  **Global Error Handler:** Implement a global error handler to catch all unhandled exceptions.
3.  **User-Friendly Messages:** Return user-friendly error messages to the client.
4.  **Logging:** Log all errors with a full stack trace.
5.  **HTTP Status Codes:** Use appropriate HTTP status codes for different types of errors.

---

## 📝 PHASES OF IMPLEMENTATION

### Phase 1: Custom Errors
1.  **Create Base Error:** Create a base `AppError` class that all other custom errors will extend.
2.  **Create Custom Errors:** Create custom error classes for common error scenarios (e.g., `NotFoundError`, `ForbiddenError`).

### Phase 2: Global Error Handler
1.  **Create Middleware:** Create a global error handling middleware for the backend.
2.  **Handle Errors:** The middleware should catch all errors, log them, and send a user-friendly response to the client.

### Phase 3: Integration
1.  **Throw Custom Errors:** Go through the codebase and replace generic `Error` objects with the new custom error classes.
2.  **Handle Errors in UI:** Implement a consistent way to display errors to the user in the frontend.

### Phase 4: Verification
1.  **Test Error Scenarios:** Write tests to ensure that the error handling system works as expected for different error scenarios.
2.  **Manual Verification:** Manually trigger different errors and verify that they are handled correctly.

---

## ✅ SUCCESS CRITERIA

- All errors are handled gracefully.
- Users are shown user-friendly error messages.
- All errors are logged with a full stack trace.
- The application uses appropriate HTTP status codes.
