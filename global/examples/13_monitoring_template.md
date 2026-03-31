# Monitoring & Alerts Template

## Health Check Endpoint

```javascript
app.get('/health', async (req, res) => {
  const health = {
    uptime: process.uptime(),
    timestamp: Date.now(),
    status: 'OK',
    checks: {}
  };
  
  // Check database
  try {
    await db.ping();
    health.checks.database = 'OK';
  } catch (error) {
    health.checks.database = 'FAIL';
    health.status = 'DEGRADED';
  }
  
  // Check external API
  try {
    await externalAPI.ping();
    health.checks.externalAPI = 'OK';
  } catch (error) {
    health.checks.externalAPI = 'FAIL';
    health.status = 'DEGRADED';
  }
  
  const statusCode = health.status === 'OK' ? 200 : 503;
  res.status(statusCode).json(health);
});
```
