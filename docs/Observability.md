# Observability Architecture

**FILE:** docs/Observability.md  
**PURPOSE:** Document frontend observability system with traceId, structured logging, and performance monitoring  
**OWNER:** Frontend Team  
**LAST-AUDITED:** 2025-10-23

## Overview

The observability system provides comprehensive tracking of:
- **Distributed Tracing**: TraceId propagation across frontend and backend
- **Structured Logging**: Consistent log format with severity levels
- **Performance Monitoring**: Core Web Vitals and API response times
- **Error Tracking**: Automatic error reporting with context
- **User Actions**: Click tracking, form submissions, navigation

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Application                          │
├─────────────────────────────────────────────────────────┤
│  Components → Hooks (useObservability) → Utilities      │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  TraceId     │  │   Logger     │  │ Performance  │  │
│  │  Generator   │  │   (Structured)   │  Monitor     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│  API Interceptors (axios) + Error Boundary              │
├─────────────────────────────────────────────────────────┤
│  Backend API (/api/logs, /api/metrics, /api/errors)    │
└─────────────────────────────────────────────────────────┘
```

## TraceId System

### Generation
```javascript
import { generateTraceId, getSessionTraceId, createOperationTraceId } from '@/utils/traceId'

// Session-level traceId (persists across page navigation)
const sessionTraceId = getSessionTraceId()

// Operation-level traceId (for specific requests)
const operationTraceId = createOperationTraceId('login')
```

### Propagation
- **Session TraceId**: Stored in `sessionStorage._trace_id`
- **Current TraceId**: Stored in `sessionStorage._current_trace_id`
- **HTTP Headers**: Injected as `X-Trace-Id` in all API requests
- **Logs**: Included in every log entry

### Flow
```
User Action
    ↓
Generate/Get TraceId
    ↓
Inject into API Request (X-Trace-Id header)
    ↓
Backend receives and logs with same TraceId
    ↓
Response includes X-Trace-Id header
    ↓
Frontend extracts and stores for correlation
```

## Structured Logging

### Log Entry Format
```javascript
{
  traceId: "uuid-v4",
  timestamp: "2025-10-23T12:34:56.789Z",
  severity: "INFO|WARN|ERROR|CRITICAL|DEBUG",
  action: "button_click|api_request|error_occurred",
  message: "User-friendly message",
  userId: "user_id or anonymous",
  tenantId: "tenant_id or default",
  route: "/dashboard",
  url: "http://localhost:5502/dashboard",
  userAgent: "Mozilla/5.0...",
  timed_ms: 1234,
  outcome: "success|error|pending|warning",
  data: { /* additional context */ }
}
```

### Severity Levels
- **DEBUG**: Development-only detailed information
- **INFO**: General informational messages
- **WARN**: Warning conditions (slow requests, deprecated usage)
- **ERROR**: Error conditions (failed requests, exceptions)
- **CRITICAL**: Critical errors (app crashes, security issues)

### Usage Examples

#### Log Button Click
```javascript
import { logClick } from '@/utils/logger'

logClick('submit-btn', 'Submit Form', {
  formId: 'login-form',
  fieldCount: 3
})
```

#### Log API Request
```javascript
import { logApiRequest } from '@/utils/logger'

logApiRequest('POST', '/api/products', 1234, 201, {
  productId: 123,
  outcome: 'success'
})
```

#### Log Custom Event
```javascript
import { logEvent } from '@/utils/logger'

logEvent('user_login', {
  username: 'john@example.com',
  loginMethod: 'email',
  outcome: 'success'
})
```

#### Log Error
```javascript
import { logError } from '@/utils/logger'

try {
  // some operation
} catch (error) {
  logError(error, {
    operation: 'fetch_products',
    context: 'ProductList component'
  })
}
```

## Performance Monitoring

### Core Web Vitals
- **LCP** (Largest Contentful Paint): ≤ 2.5s ✓
- **FID** (First Input Delay): ≤ 100ms ✓
- **CLS** (Cumulative Layout Shift): ≤ 0.1 ✓

### Metrics Tracked
```javascript
{
  lcp: 1234,           // ms
  fid: 45,             // ms
  cls: 0.05,           // unitless
  pageLoadTime: 2345,  // ms
  apiRequests: [
    {
      method: 'GET',
      url: '/api/products',
      timingMs: 234,
      statusCode: 200,
      timestamp: '2025-10-23T12:34:56.789Z'
    }
  ]
}
```

### Usage
```javascript
import performanceMonitor from '@/utils/performanceMonitor'

// Get current metrics
const metrics = performanceMonitor.getMetrics()

// Get summary for debugging
const summary = performanceMonitor.getSummary()
// Output:
// {
//   vitals: {
//     lcp: "1234ms ✓",
//     fid: "45ms ✓",
//     cls: "0.05 ✓"
//   },
//   pageLoadTime: "2345ms",
//   apiRequests: { total: 5, averageTime: "234ms", slowRequests: 0 }
// }
```

## React Hooks

### useObservability
Track component lifecycle and renders
```javascript
import { useObservability } from '@/hooks/useObservability'

function MyComponent(props) {
  const { traceId, renderCount } = useObservability('MyComponent', props)
  return <div>Render #{renderCount}</div>
}
```

### useAsyncObservability
Track async operations with timing
```javascript
import { useAsyncObservability } from '@/hooks/useObservability'

function MyComponent() {
  const fetchData = useAsyncObservability(
    async (id) => {
      const res = await fetch(`/api/data/${id}`)
      return res.json()
    },
    'fetch_data'
  )
  
  return <button onClick={() => fetchData(123)}>Load</button>
}
```

### useFormObservability
Track form submissions
```javascript
import { useFormObservability } from '@/hooks/useObservability'

function LoginForm() {
  const { trackSubmit } = useFormObservability('login_form')
  
  const handleSubmit = async (formData) => {
    const tracker = trackSubmit(formData)
    try {
      await login(formData)
      tracker.success()
    } catch (error) {
      tracker.error(error)
    }
  }
}
```

### usePageObservability
Track page views
```javascript
import { usePageObservability } from '@/hooks/useObservability'

function Dashboard() {
  const { traceId } = usePageObservability('Dashboard')
  return <div>Dashboard</div>
}
```

## Error Boundary

### Enhanced Error Boundary
```javascript
import ErrorBoundaryEnhanced from '@/components/ErrorBoundaryEnhanced'

function App() {
  return (
    <ErrorBoundaryEnhanced>
      <YourApp />
    </ErrorBoundaryEnhanced>
  )
}
```

Features:
- Automatic error reporting to backend
- Error ID and TraceId display
- Stack trace visibility (dev mode)
- Recovery options (retry, reload, home)
- User-friendly Arabic/English UI

## Initialization

### In App.jsx
```javascript
import { initializeObservability } from '@/utils/observabilityInit'

function App() {
  useEffect(() => {
    initializeObservability()
  }, [])
  
  return <YourApp />
}
```

### In main.jsx
```javascript
import { initializeObservability } from '@/utils/observabilityInit'

initializeObservability()

ReactDOM.createRoot(document.getElementById('root')).render(
  <App />
)
```

## Backend Integration

### Expected Endpoints
- `POST /api/logs` - Receive structured logs
- `POST /api/metrics/report` - Receive performance metrics
- `POST /api/errors/report` - Receive error reports

### Log Entry Format (Backend)
```python
{
    "traceId": "uuid-v4",
    "timestamp": "2025-10-23T12:34:56.789Z",
    "severity": "INFO",
    "action": "api_request",
    "message": "GET /api/products",
    "userId": "user_123",
    "tenantId": "tenant_456",
    "route": "/dashboard",
    "timed_ms": 234,
    "outcome": "success",
    "data": {...}
}
```

## Best Practices

1. **Always use traceId**: Include in all logs and API calls
2. **Structured logging**: Use consistent format with severity levels
3. **Performance tracking**: Monitor slow requests (> 3s)
4. **Error reporting**: Log errors immediately with context
5. **User privacy**: Don't log sensitive data (passwords, tokens)
6. **Batch logs**: Use auto-flush (5s interval) to reduce overhead
7. **Development mode**: Use console.debug for detailed logging

## Debugging

### Print Observability Summary
```javascript
import { printObservabilitySummary } from '@/utils/observabilityInit'

printObservabilitySummary()
```

### Get Current Status
```javascript
import { getObservabilityStatus } from '@/utils/observabilityInit'

const status = getObservabilityStatus()
console.log(status)
```

### Access Global TraceId
```javascript
const traceId = window.__TRACE_ID__.getSessionTraceId()
```

## Files

- `frontend/src/utils/traceId.js` - TraceId generation and management
- `frontend/src/utils/logger.js` - Structured logging system
- `frontend/src/utils/performanceMonitor.js` - Core Web Vitals tracking
- `frontend/src/utils/observabilityInit.js` - Initialization
- `frontend/src/hooks/useObservability.js` - React hooks
- `frontend/src/components/ErrorBoundaryEnhanced.jsx` - Error boundary
- `frontend/src/services/api.js` - API interceptors with traceId injection

