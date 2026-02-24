# 📡 Monitoring & Alerts Template (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel (Health Check)

## 1. The Philosophy
If you can't measure it, you can't manage it.

## 2. Health Check Endpoint
You MUST implement a `/health` endpoint that checks dependencies.

```javascript
app.get('/health', async (req, res) => {
  const health = {
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
    status: 'OK',
    checks: {}
  };
  
  // Sentinel Check: Database Connectivity
  try {
    await db.query('SELECT 1');
    health.checks.database = 'OK';
  } catch (error) {
    health.checks.database = 'FAIL';
    health.status = 'DEGRADED';
    // Log critical failure
    console.error('Health Check Failed: Database unreachable');
  }
  
  // Sentinel Check: Redis Connectivity
  try {
    await redis.ping();
    health.checks.redis = 'OK';
  } catch (error) {
    health.checks.redis = 'FAIL';
    health.status = 'DEGRADED';
  }
  
  const statusCode = health.status === 'OK' ? 200 : 503;
  res.status(statusCode).json(health);
});
```
