# PROMPT 85: COMPREHENSIVE MCP TESTING

**Objective:** Use MCP (Playwright) to test every aspect of the application: UI, navigation, buttons, forms, database operations, and API endpoints.

---

## 🎯 REQUIREMENTS

1.  **Frontend Testing:** Test every page, button, form, and navigation link.
2.  **Backend Testing:** Test every API endpoint with various inputs.
3.  **Database Testing:** Verify that all CRUD operations work correctly.
4.  **Navigation Testing:** Test all routes and page transitions.
5.  **Error Handling Testing:** Test error scenarios and verify that errors are handled gracefully.

---

## 📝 PHASES OF IMPLEMENTATION

### Phase 1: Setup MCP Playwright
1.  **Verify MCP Server:** Ensure the Playwright MCP server is configured in your environment.
2.  **List Tools:** Run `manus-mcp-cli tool list --server playwright` to see available tools.
3.  **Install Browser:** Run the `browser_install` tool to install the browser.

### Phase 2: Frontend Testing
1.  **Navigate to Each Page:** Use `browser_navigate` to visit every page in the application.
2.  **Click Every Button:** Use `browser_click` to click every button and verify the expected action occurs.
3.  **Fill Every Form:** Use `browser_fill_form` to fill out every form and submit it.
4.  **Test Navigation:** Click every navigation link and verify that the correct page loads.
5.  **Take Screenshots:** Use `browser_screenshot` to capture the state of each page.

### Phase 3: Backend Testing
1.  **Test API Endpoints:** Use MCP to send HTTP requests to every API endpoint.
2.  **Test Different Inputs:** Test each endpoint with valid, invalid, and edge-case inputs.
3.  **Verify Responses:** Verify that the API returns the correct status codes and response bodies.

### Phase 4: Database Testing
1.  **Test CRUD Operations:** Use the application's UI to create, read, update, and delete records.
2.  **Verify Database State:** After each operation, verify that the database is in the correct state.

### Phase 5: Error Handling Testing
1.  **Trigger Errors:** Intentionally trigger errors (e.g., submit a form with invalid data).
2.  **Verify Error Messages:** Verify that the application displays user-friendly error messages.
3.  **Check Logs:** Verify that errors are logged correctly in `logs/error.log`.

---

## ✅ SUCCESS CRITERIA

- All pages load correctly.
- All buttons work as expected.
- All forms can be submitted successfully.
- All navigation links work.
- All API endpoints return the correct responses.
- All database operations work correctly.
- All errors are handled gracefully.
