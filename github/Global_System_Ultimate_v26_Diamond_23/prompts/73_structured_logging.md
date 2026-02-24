# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# ▓                                                                         ▓
# ▓               PROMPT 73: STRUCTURED LOGGING IMPLEMENTATION              ▓
# ▓                                                                         ▓
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

**Objective:** Implement a robust, structured, multi-file logging system for the project.

---

## 🎯 REQUIREMENTS

1.  **Library:** Use a standard, production-grade logging library (Winston for Node.js, Python's `logging` module, etc.).
2.  **JSON Format:** All log output must be in JSON format.
3.  **Multiple Files:** Log to different files based on level (`debug.log`, `info.log`, `error.log`, etc.).
4.  **Timestamp:** All logs must have a UTC timestamp.
5.  **Context:** Include relevant context (e.g., `userId`, `phase`, `requestId`).
6.  **Error Logging:** Errors must include a full stack trace.
7.  **Configuration:** The logging system must be configurable via environment variables.

---

## 📝 PHASES OF IMPLEMENTATION

### Phase 1: Setup & Configuration
1.  **Install Library:** Add the chosen logging library to the project's dependencies.
2.  **Create Config File:** Create a configuration file (e.g., `src/config/logger.js`) that sets up the logger.
3.  **Define Transports:** Configure transports to write to the correct files based on log level.
4.  **Set Log Level:** The log level should be configurable via an environment variable (e.g., `LOG_LEVEL=info`).

### Phase 2: Integration
1.  **Create Logger Instance:** Create a singleton logger instance that can be imported throughout the application.
2.  **Replace `console.log`:** Replace all instances of `console.log`, `console.error`, etc., with the new logger.
3.  **Add Middleware (Backend):** Create a middleware to log all incoming HTTP requests and their responses.
4.  **Add Context:** Add context to logs where appropriate (e.g., in the request middleware, add `userId` and `requestId`).

### Phase 3: Error Handling
1.  **Global Error Handler:** Implement a global error handler that catches all unhandled exceptions.
2.  **Log Errors:** The global error handler must log the error to `logs/error.log` with a full stack trace.
3.  **Consistent Error Format:** Ensure all errors are logged in a consistent format.

### Phase 4: Verification
1.  **Run Tests:** Run all existing tests to ensure the new logging system has not introduced any regressions.
2.  **Manual Verification:** Manually trigger different actions in the application and verify that logs are being written to the correct files in the correct format.
3.  **Error Test:** Manually trigger an error and verify that it is logged correctly in `logs/error.log`.

---

## ✅ SUCCESS CRITERIA

- All `console.log` statements are removed.
- Logs are written to `logs/` in JSON format.
- Log level is configurable.
- Errors are logged with stack traces.
- The system is fully integrated and tested.
