# ❌ Errors Tracking System

> **Purpose:** Organize and track all errors by severity, integrated with **Sentinel** and **Speckit**.

## Structure

- `critical/` - System-breaking errors (🔴) - **Sentinel Blocks Commit**
- `high/` - Significant functionality errors (🟠) - **Sentinel Blocks Commit**
- `medium/` - User experience errors (🟡) - **Speckit Warning**
- `low/` - Minor errors (🟢) - **Speckit Warning**
- `resolved/` - Archived resolved errors (✅)

## Main File

See `DONT_MAKE_THESE_ERRORS_AGAIN.md` for the complete error log and prevention strategies.

## Integration

*   **Speckit Verify:** Automatically checks these directories.
*   **Sentinel:** Enforces Zero-Error Tolerance for Critical/High errors.

---

❌ **Learn from every error!** ❌
