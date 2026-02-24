# Error Log: Don't Make This Error Again

## 1. Infinite Loop in React useEffect
- **Error:** Using `new Date()` as a dependency in `useEffect` caused an infinite re-render loop.
- **Fix:** Use `useMemo` or `useState` to stabilize the dependency.
- **Lesson:** Always verify dependency stability in React hooks.

## 2. Missing Environment Variables
- **Error:** Deployment failed because `API_KEY` was not set in the production environment.
- **Fix:** Added a pre-deployment check script to verify all required env vars.
- **Lesson:** Use a `.env.example` file and validate config on startup.
