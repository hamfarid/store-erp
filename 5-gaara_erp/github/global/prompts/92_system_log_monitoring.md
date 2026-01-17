# 📋 System Log Monitoring

**Priority:** HIGH  
**Phase:** All Phases (Continuous)  
**Status:** Production Ready

---

## 🎯 Purpose

Monitor system logs, application logs, and runtime errors in **real-time background** to provide comprehensive error tracking and debugging insights.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [What It Monitors](#what-it-monitors)
3. [Usage](#usage)
4. [Reports](#reports)
5. [Integration](#integration)
6. [Best Practices](#best-practices)

---

## 1. Overview

### What is System Log Monitoring?

A **background service** that continuously monitors various log sources to detect and track:
- Application errors
- System errors
- Network issues
- Database problems
- Console errors
- npm/package manager issues

### Why It Matters

**Development Impact:**
- Catch errors immediately
- Understand error patterns
- Debug faster
- Prevent issues from reaching production

**Business Impact:**
- Reduce downtime
- Improve reliability
- Better user experience
- Lower support costs

---

## 2. What It Monitors

### 1. npm/Node Logs 📦
**Monitors:**
- `~/.npm/_logs/*.log`
- Package installation errors
- Dependency conflicts
- Build failures

**Detects:**
- `npm ERR!` messages
- Version conflicts
- Missing dependencies
- Build script failures

---

### 2. Console Logs 🌐
**Monitors:**
- `logs/console.log`
- Browser console output
- JavaScript errors
- API call failures

**Detects:**
- `Uncaught Error`
- `TypeError`
- `ReferenceError`
- `Failed to fetch`
- `404 Not Found`

---

### 3. Application Logs 📱
**Monitors:**
- `logs/*.log`
- `logs/**/*.log`
- `.logs/*.log`
- `app.log`
- `error.log`

**Detects:**
- Application-specific errors
- Business logic errors
- Validation failures
- Authentication issues

---

### 4. System Errors 🖥️
**Monitors:**
- Unhandled exceptions
- Segmentation faults
- Memory errors
- Process crashes

**Detects:**
- `Unhandled exception`
- `Segmentation fault`
- `Out of memory`
- `Process terminated`

---

### 5. Network Errors 🌐
**Monitors:**
- `logs/network.log`
- API call logs
- HTTP request/response logs

**Detects:**
- `ECONNREFUSED`
- `ETIMEDOUT`
- `ENOTFOUND`
- `ERR_CONNECTION`
- `Failed to fetch`

---

### 6. Database Logs 🗄️
**Monitors:**
- `logs/database.log`
- `logs/db.log`
- `logs/sql.log`
- `prisma.log`

**Detects:**
- SQL errors
- Connection failures
- Query timeouts
- Constraint violations

---

## 3. Usage

### Installation

```bash
# Already included in .global/tools/
# No installation needed
```

---

### Start Monitoring

```bash
# Start in current directory
python3 .global/tools/system_log_monitor.py

# Start in specific project
python3 .global/tools/system_log_monitor.py /path/to/project

# Monitor for specific duration (60 seconds)
python3 .global/tools/system_log_monitor.py . --duration 60
```

---

### Background Monitoring

```bash
# Start as background process
nohup python3 .global/tools/system_log_monitor.py > /dev/null 2>&1 &

# Save PID
echo $! > logs/monitor.pid

# Stop monitoring
kill $(cat logs/monitor.pid)
```

---

### Add to package.json

```bash
npm pkg set scripts.monitor:start="python3 .global/tools/system_log_monitor.py ."
npm pkg set scripts.monitor:stop="kill \$(cat logs/monitor.pid) 2>/dev/null || true"
```

---

### Systemd Service (Linux)

```ini
# /etc/systemd/system/system-log-monitor.service
[Unit]
Description=System Log Monitor
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python3 /path/to/.global/tools/system_log_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable system-log-monitor
sudo systemctl start system-log-monitor

# Check status
sudo systemctl status system-log-monitor

# View logs
sudo journalctl -u system-log-monitor -f
```

---

## 4. Reports

### Real-time Logging

**Console Output:**
```
2025-11-17 14:30:15 - SystemLogMonitor - INFO - 🚀 Starting System Log Monitor...
2025-11-17 14:30:15 - SystemLogMonitor - INFO - 📦 Monitoring npm logs...
2025-11-17 14:30:15 - SystemLogMonitor - INFO - 🌐 Monitoring console logs...
2025-11-17 14:30:15 - SystemLogMonitor - INFO - 📱 Monitoring application logs...
2025-11-17 14:30:15 - SystemLogMonitor - INFO - 🖥️  Monitoring system errors...
2025-11-17 14:30:15 - SystemLogMonitor - INFO - 🌐 Monitoring network errors...
2025-11-17 14:30:15 - SystemLogMonitor - INFO - 🗄️  Monitoring database logs...
2025-11-17 14:30:15 - SystemLogMonitor - INFO - ✅ All monitors started
2025-11-17 14:31:23 - SystemLogMonitor - ERROR - [console] TypeError: Cannot read property 'name' of undefined
2025-11-17 14:32:45 - SystemLogMonitor - ERROR - [network] ECONNREFUSED: Connection refused
2025-11-17 14:35:15 - SystemLogMonitor - INFO - 📊 Current Status: 2 errors, 0 warnings
```

---

### Error Log (JSONL)

**File:** `logs/errors.jsonl`

```jsonl
{"timestamp": "2025-11-17T14:31:23.456Z", "source": "console", "message": "TypeError: Cannot read property 'name' of undefined", "level": "ERROR"}
{"timestamp": "2025-11-17T14:32:45.789Z", "source": "network", "message": "ECONNREFUSED: Connection refused", "level": "ERROR"}
```

---

### Final Report (Markdown)

**File:** `logs/SYSTEM_LOG_REPORT_20251117_143000.md`

```markdown
# System Log Monitor Report

**Generated:** 2025-11-17 14:30:00  
**Project:** my-project

---

## Summary

| Category | Count |
|----------|-------|
| **Errors** | 15 |
| **Warnings** | 3 |
| **Info** | 127 |

---

## Errors by Source

| Source | Count |
|--------|-------|
| console | 8 |
| network | 4 |
| database | 2 |
| npm | 1 |

---

## Errors by Type

| Type | Count |
|------|-------|
| Error | 7 |
| Failed | 4 |
| Refused | 2 |
| Timeout | 2 |

---

## Recent Errors (Last 20)

### console - 2025-11-17T14:31:23.456Z
```
TypeError: Cannot read property 'name' of undefined
    at UserComponent.render (UserComponent.js:45)
```

### network - 2025-11-17T14:32:45.789Z
```
ECONNREFUSED: Connection refused
    at TCPConnectWrap.afterConnect (net.js:1148:16)
```

---

## Recommendations

⚠️ **Errors detected** - Review and fix the errors listed above
🌐 **Network issues** - Check network connectivity and API endpoints
```

---

### JSON Summary

**File:** `logs/system_log_summary.json`

```json
{
  "timestamp": "2025-11-17T14:30:00.000Z",
  "project": "/path/to/project",
  "total_errors": 15,
  "total_warnings": 3,
  "total_info": 127,
  "errors_by_source": {
    "console": 8,
    "network": 4,
    "database": 2,
    "npm": 1
  },
  "warnings_by_source": {
    "console": 2,
    "npm": 1
  },
  "error_types": {
    "Error": 7,
    "Failed": 4,
    "Refused": 2,
    "Timeout": 2
  }
}
```

---

## 5. Integration

### With Development Workflow

```bash
# Start monitoring when starting development
npm run monitor:start &
npm run dev

# Stop when done
npm run monitor:stop
```

---

### With CI/CD

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Start log monitoring
        run: |
          python3 .global/tools/system_log_monitor.py . --duration 300 &
          echo $! > monitor.pid
      
      - name: Run tests
        run: npm test
      
      - name: Stop monitoring
        run: kill $(cat monitor.pid) || true
      
      - name: Upload log report
        uses: actions/upload-artifact@v3
        with:
          name: log-report
          path: logs/SYSTEM_LOG_REPORT_*.md
```

---

### With Docker

```dockerfile
# Dockerfile
FROM node:18

WORKDIR /app

COPY . .

RUN npm install

# Install Python for monitoring
RUN apt-get update && apt-get install -y python3

# Start monitoring in background
CMD python3 .global/tools/system_log_monitor.py & npm start
```

---

## 6. Best Practices

### DO ✅

1. **Monitor continuously** - Run in background during development
2. **Review reports regularly** - Daily or after each session
3. **Fix errors promptly** - Don't let them accumulate
4. **Track error patterns** - Identify recurring issues
5. **Use in CI/CD** - Catch issues in automated tests
6. **Keep logs organized** - Rotate old logs
7. **Set up alerts** - For critical errors
8. **Integrate with tools** - Sentry, LogRocket, etc.
9. **Monitor production** - Not just development
10. **Learn from errors** - Improve code quality

### DON'T ❌

1. **Don't ignore errors** - They indicate problems
2. **Don't disable monitoring** - To "improve performance"
3. **Don't delete logs** - Archive them instead
4. **Don't log sensitive data** - Passwords, tokens, etc.
5. **Don't overwhelm with logs** - Use appropriate log levels
6. **Don't forget to rotate** - Logs can grow large
7. **Don't skip analysis** - Review reports
8. **Don't rely solely on monitoring** - Also use debugging
9. **Don't ignore warnings** - They become errors
10. **Don't monitor without action** - Fix what you find

---

## 🎯 Integration with Our System

### All Phases
- Run monitoring in background
- Review logs after each phase
- Fix errors before proceeding

### Phase 4: Testing
- Monitor during test execution
- Catch runtime errors
- Verify error handling

### Phase 6: Deployment
- Setup production monitoring
- Configure alerts
- Integrate with logging services

### Checkpoints
- ✅ Monitoring running
- ✅ No critical errors
- ✅ Errors reviewed and fixed
- ✅ Reports generated
- ✅ Logs archived

---

## 📚 Resources

- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Systemd Services](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [Sentry](https://sentry.io/)
- [LogRocket](https://logrocket.com/)

---

## 🔧 Troubleshooting

### Monitoring not starting
```bash
# Check Python version
python3 --version

# Check permissions
ls -l .global/tools/system_log_monitor.py

# Run with verbose output
python3 .global/tools/system_log_monitor.py . 2>&1 | tee monitor.log
```

### No errors detected
```bash
# Check log file locations
ls -la logs/

# Verify log format
cat logs/error.log

# Test with sample error
echo "ERROR: Test error" >> logs/app.log
```

### High memory usage
```bash
# Check process
ps aux | grep system_log_monitor

# Limit monitoring scope
# Edit script to exclude certain log files
```

---

**Status:** ✅ Production Ready  
**Last Updated:** 2025-11-17  
**Version:** 1.0

