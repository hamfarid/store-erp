# Performance Optimization Standards (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Engine:** Speckit Global System v26 Diamond 32
**Status:** MANDATORY REFERENCE
**Phase:** Optimize

## 1. The Performance Mindset
Performance is not an afterthought; it is a feature.
**Rule:** If it's slow, it's broken.
**Golden Rule:** Measure First. Do not optimize without profiling.

## 2. Frontend Optimization (React/Next.js)
### A. Bundle Size
- Use `next/dynamic` or `React.lazy` for route-based code splitting.
- Avoid importing heavy libraries (e.g., `moment.js`) for simple tasks.
- Use `import { func } from 'lib'` instead of `import * as lib`.

### B. Rendering
- Use `useMemo` and `useCallback` for expensive calculations.
- Virtualize long lists (use `react-window` or `tanstack-virtual`).
- Optimize images: Use WebP/AVIF, lazy loading (`loading="lazy"`), and proper sizing.

### C. Network
- Use SWR or React Query for caching and deduplication.
- Prefetch critical resources.
- Minimize round trips.

## 3. Backend Optimization (Node.js/Python)
### A. Database (The Bottleneck)
- **Indexing:** Ensure all foreign keys and query filters are indexed.
- **N+1 Queries:** Use `JOIN` (SQL), `.populate()` (Mongoose), or `DataLoader` to batch requests.
- **Selectivity:** Select only the columns you need (`SELECT id, name` vs `SELECT *`).
- **Connection Pooling:** Always use a pool, never open/close per request.

### B. Caching
- **Redis:** Cache expensive query results and API responses.
- **CDN:** Serve static assets via Cloudflare or AWS CloudFront.

### C. Compute
- Offload heavy tasks (emails, reports) to background workers (BullMQ, Celery).
- Use streams for large file processing.
- Enable Gzip/Brotli compression.

## 4. Profiling Tools
*   **Backend:** PyInstrument (Python), Clinic.js (Node).
*   **Frontend:** Chrome DevTools (Lighthouse, Performance Tab).
*   **Database:** `EXPLAIN ANALYZE` (PostgreSQL).

## 5. Speckit Verify: Performance
Run `speckit verify --perf` to check:
- Lighthouse score > 90.
- API response time < 200ms (p95).
- Database query analysis (EXPLAIN ANALYZE).
