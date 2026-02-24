# Performance Tuning Protocol

## Objective
Optimize application performance for speed, scalability, and efficiency.

## Checklist
1. **Database:** Analyze slow queries, add indexes, and optimize schema.
2. **Caching:** Implement Redis/Memcached for frequently accessed data.
3. **Frontend:** Minify assets, lazy load images, and use CDN.
4. **Backend:** Profile CPU/Memory usage, optimize algorithms, and use async I/O.
5. **Network:** Reduce payload size, use HTTP/2, and enable compression (Gzip/Brotli).

## Tools
- PySpy / cProfile
- Chrome DevTools
- pgBadger (PostgreSQL)
