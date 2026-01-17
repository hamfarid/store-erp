# 📋 Log Files Inventory - Store ERP System

**Generated:** November 11, 2025  
**Purpose:** Comprehensive inventory of all log files and logging systems

---

## 🗂️ Log File Structure

### Backend Logs

```
backend/
├── logs/                              # Main log directory
│   ├── app.log                       # Main application log
│   ├── error.log                     # Error-only log
│   ├── access.log                    # API access log
│   ├── database.log                  # Database operations log
│   ├── security.log                  # Security events log
│   ├── performance.log               # Performance metrics log
│   └── debug.log                     # Debug-level log (dev only)
│
├── instance/                         # Instance-specific logs
│   └── flask.log                     # Flask internal log
│
└── tmp/                             # Temporary logs
    └── startup.log                  # Startup diagnostics log
```

### Frontend Logs

```
frontend/
├── logs/                             # Frontend log directory
│   ├── console.log                  # Browser console log
│   ├── error.log                    # Frontend error log
│   └── api.log                      # API call log
│
└── test-results/                    # Test execution logs
    ├── e2e-test-results.txt         # E2E test results
    ├── unit-test-results.txt        # Unit test results
    └── coverage/                     # Test coverage reports
        └── lcov-report/
            └── index.html           # Coverage HTML report
```

### System Logs

```
./
├── system_log.md                     # System-wide changelog
├── UPDATED_FILES.md                  # File modification log
├── FINAL_REPORT.md                   # Project completion log
└── logs/                            # Root-level logs
    ├── git.log                      # Git operations log
    ├── docker.log                   # Docker operations log
    └── deployment.log               # Deployment log
```

---

## 📊 Logging Configuration

### Backend Logging (Python)

**Location:** `backend/src/utils/logger.py`

**Configuration:**
```python
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed'
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/error.log',
            'maxBytes': 10485760,
            'backupCount': 5,
            'level': 'ERROR',
            'formatter': 'detailed'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'error_file', 'console']
    }
}
```

**Log Levels:**
- `DEBUG` - Detailed debugging information (development only)
- `INFO` - General informational messages
- `WARNING` - Warning messages for potential issues
- `ERROR` - Error messages for failures
- `CRITICAL` - Critical errors that require immediate attention

### Frontend Logging (JavaScript)

**Location:** `frontend/src/utils/logger.js`

**Configuration:**
```javascript
const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
  NONE: 4
};

const CURRENT_LOG_LEVEL = process.env.NODE_ENV === 'production' 
  ? LOG_LEVELS.WARN 
  : LOG_LEVELS.DEBUG;

const logger = {
  debug: (message, ...args) => {
    if (CURRENT_LOG_LEVEL <= LOG_LEVELS.DEBUG) {
      console.debug(`[DEBUG] ${message}`, ...args);
    }
  },
  info: (message, ...args) => {
    if (CURRENT_LOG_LEVEL <= LOG_LEVELS.INFO) {
      console.info(`[INFO] ${message}`, ...args);
    }
  },
  warn: (message, ...args) => {
    if (CURRENT_LOG_LEVEL <= LOG_LEVELS.WARN) {
      console.warn(`[WARN] ${message}`, ...args);
    }
  },
  error: (message, ...args) => {
    if (CURRENT_LOG_LEVEL <= LOG_LEVELS.ERROR) {
      console.error(`[ERROR] ${message}`, ...args);
    }
  }
};
```

---

## 🔍 Log File Details

### 1. Application Log (`backend/logs/app.log`)

**Purpose:** Main application activity log  
**Rotation:** 10MB, 5 backups  
**Level:** INFO and above  
**Contains:**
- API requests and responses
- Business logic operations
- Database queries
- Cache operations
- Background tasks

**Sample Entry:**
```
2025-11-11 10:50:14,929 - app - INFO - [app.py:123] - Starting Flask application
2025-11-11 10:50:15,123 - database - INFO - [database.py:45] - Database connection established
2025-11-11 10:50:15,456 - auth - INFO - [auth.py:78] - User 'admin' logged in successfully
```

### 2. Error Log (`backend/logs/error.log`)

**Purpose:** Error-only log for quick troubleshooting  
**Rotation:** 10MB, 5 backups  
**Level:** ERROR and CRITICAL  
**Contains:**
- Application errors
- Database errors
- Authentication failures
- Validation errors
- System exceptions

**Sample Entry:**
```
2025-11-11 10:50:14,929 - database - ERROR - [database.py:67] - ❌ خطأ في إنشاء الجداول: Foreign key associated with column 'sales_invoices.customer_id' could not find table 'customers' with which to generate a foreign key to target column 'id'
```

### 3. Access Log (`backend/logs/access.log`)

**Purpose:** HTTP request/response log  
**Rotation:** 10MB, 5 backups  
**Level:** INFO  
**Contains:**
- HTTP method and path
- Request IP address
- Response status code
- Response time
- User agent

**Sample Entry:**
```
2025-11-11 10:50:15,789 - access - INFO - 127.0.0.1 - GET /api/products - 200 - 45ms
2025-11-11 10:50:16,123 - access - INFO - 127.0.0.1 - POST /api/auth/login - 200 - 123ms
```

### 4. Database Log (`backend/logs/database.log`)

**Purpose:** Database operations log  
**Rotation:** 10MB, 5 backups  
**Level:** DEBUG (dev) / INFO (prod)  
**Contains:**
- SQL queries
- Database connections
- Transaction commits/rollbacks
- Migration operations
- Query performance

**Sample Entry:**
```
2025-11-11 10:50:15,123 - sqlalchemy.engine - INFO - [database.py:45] - SELECT * FROM users WHERE id = 1
2025-11-11 10:50:15,156 - sqlalchemy.engine - DEBUG - [database.py:67] - BEGIN (implicit)
2025-11-11 10:50:15,189 - sqlalchemy.engine - DEBUG - [database.py:89] - COMMIT
```

### 5. Security Log (`backend/logs/security.log`)

**Purpose:** Security-related events  
**Rotation:** 10MB, 10 backups (keep longer)  
**Level:** INFO  
**Contains:**
- Login attempts (successful/failed)
- Permission denied events
- JWT token generation
- Password changes
- Suspicious activity

**Sample Entry:**
```
2025-11-11 10:50:15,456 - security - INFO - User 'admin' logged in from 127.0.0.1
2025-11-11 10:50:16,789 - security - WARNING - Failed login attempt for user 'admin' from 192.168.1.100
2025-11-11 10:50:17,123 - security - INFO - User 'admin' changed password
```

### 6. Performance Log (`backend/logs/performance.log`)

**Purpose:** Performance metrics and monitoring  
**Rotation:** 10MB, 5 backups  
**Level:** INFO  
**Contains:**
- Request response times
- Database query times
- Cache hit/miss rates
- Memory usage
- CPU usage

**Sample Entry:**
```
2025-11-11 10:50:15,789 - performance - INFO - API /api/products response_time=45ms
2025-11-11 10:50:16,123 - performance - INFO - Database query products response_time=12ms
2025-11-11 10:50:16,456 - performance - INFO - Cache hit_rate=85% miss_rate=15%
```

### 7. Debug Log (`backend/logs/debug.log`)

**Purpose:** Detailed debugging information (development only)  
**Rotation:** 10MB, 3 backups  
**Level:** DEBUG  
**Contains:**
- Variable values
- Function calls
- Stack traces
- Detailed error information
- Development diagnostics

**Sample Entry:**
```
2025-11-11 10:50:15,123 - app - DEBUG - [app.py:123] - Processing request with params: {'id': 1, 'name': 'Product'}
2025-11-11 10:50:15,156 - app - DEBUG - [app.py:145] - Validation passed for product data
2025-11-11 10:50:15,189 - app - DEBUG - [app.py:167] - Saving product to database
```

---

## 🛠️ Log Management Tools

### Log Rotation

**Backend (Python):**
- Using `RotatingFileHandler`
- Max size: 10MB per file
- Backup count: 5 files
- Total storage: ~50MB per log type

**Configuration:**
```python
handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
```

### Log Aggregation

**Tools:**
- **Development:** Console + File logs
- **Production:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Monitoring:** Grafana + Loki

### Log Analysis

**Commands:**
```bash
# View last 100 lines
tail -n 100 logs/app.log

# Follow log in real-time
tail -f logs/app.log

# Search for errors
grep "ERROR" logs/app.log

# Count error occurrences
grep -c "ERROR" logs/app.log

# Find errors in last hour
grep "2025-11-11 10:" logs/error.log
```

---

## 📈 Log Monitoring

### Key Metrics to Monitor

1. **Error Rate**
   - Target: < 1% of requests
   - Alert: > 5% error rate

2. **Response Time**
   - Target: < 200ms average
   - Alert: > 1000ms average

3. **Database Performance**
   - Target: < 50ms average query time
   - Alert: > 500ms query time

4. **Security Events**
   - Monitor: Failed login attempts
   - Alert: > 5 failed attempts in 5 minutes

5. **System Health**
   - Monitor: Memory usage
   - Alert: > 80% memory usage

### Monitoring Tools

**Development:**
- Flask Debug Toolbar
- SQLAlchemy Echo
- Browser DevTools

**Production:**
- Grafana dashboards
- Prometheus metrics
- Sentry error tracking
- Datadog APM

---

## 🔧 Debugging with Logs

### Enable Debug Mode

**Backend:**
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
export LOG_LEVEL=DEBUG
python backend/app.py
```

**Frontend:**
```bash
npm run dev -- --mode development
```

### Common Log Queries

**Find all errors:**
```bash
grep -r "ERROR" backend/logs/
```

**Find database errors:**
```bash
grep "Foreign key" backend/logs/error.log
```

**Find slow queries:**
```bash
grep "response_time=[5-9][0-9][0-9]ms" backend/logs/performance.log
```

**Find security issues:**
```bash
grep "Failed login" backend/logs/security.log
```

---

## 📝 Current Issues (from logs)

### 1. Foreign Key Error
**File:** `backend/logs/error.log`  
**Message:** Foreign key associated with column 'sales_invoices.customer_id' could not find table 'customers'  
**Status:** 🔄 Being fixed - Model loading order issue  
**Solution:** Load base models (Customer) before dependent models (SalesInvoice)

### 2. Import Errors
**File:** Multiple Python files  
**Message:** Unable to import 'models.user', 'models.supplier', etc.  
**Status:** ⚠️ Pylint false positives - Models exist  
**Solution:** Update import paths or configure Pylint

### 3. Type Checking Issues
**File:** `enhanced_models.py`, `invoice_unified.py`  
**Message:** RelationshipProperty[Any] is not iterable  
**Status:** ⚠️ Pylance type checking issue  
**Solution:** Add type hints or ignore with # type: ignore

---

## ✅ Recommendations

### 1. Centralized Logging
- ✅ Implement structured logging (JSON format)
- ✅ Use correlation IDs for request tracking
- ✅ Add contextual information to logs

### 2. Log Retention
- ✅ Keep error logs for 30 days
- ✅ Keep access logs for 14 days
- ✅ Archive old logs to S3/Azure Storage

### 3. Security
- ✅ Never log sensitive data (passwords, tokens)
- ✅ Sanitize user input in logs
- ✅ Encrypt logs at rest

### 4. Performance
- ✅ Use async logging for high-volume logs
- ✅ Implement log sampling for debug logs
- ✅ Use log levels appropriately

---

## 🎯 Next Steps

1. **Fix Current Errors**
   - ✅ Fix foreign key error (model loading order)
   - ⏳ Update import paths
   - ⏳ Add type hints for Pylance

2. **Enhance Logging**
   - Add correlation IDs
   - Implement structured logging
   - Add log aggregation

3. **Monitoring Setup**
   - Configure Grafana dashboards
   - Set up alerts
   - Implement health checks

4. **Documentation**
   - Document logging best practices
   - Create troubleshooting guide
   - Add log examples to docs

---

**Status:** 🔄 In Progress  
**Priority:** High  
**Owner:** Development Team  
**Last Updated:** November 11, 2025
