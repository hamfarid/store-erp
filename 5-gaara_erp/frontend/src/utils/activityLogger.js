// FILE: frontend/src/utils/activityLogger.js | PURPOSE: Frontend activity logger (client-side) for actions like EXPORT | OWNER: Frontend Team | RELATED: utils/export.js, contexts/AuthContext.jsx | LAST-AUDITED: 2025-10-29

/**
 * Lightweight client-side activity logger.
 * In the future, wire this to a backend endpoint (e.g., /api/activity-logs).
 */
export function logActivity({ traceId, userId, route, action, entityType, format, recordCount, outcome, timed_ms }) {
  try {
    const payload = {
      timestamp: new Date().toISOString(),
      traceId: traceId || cryptoRandomId(),
      userId: userId || null,
      route: route || (typeof location !== 'undefined' ? location.pathname : ''),
      action,
      entityType,
      format,
      recordCount,
      outcome,
      timed_ms
    }
     
    console.info('[activity]', payload)
    // TODO: send to backend when endpoint is available
    // fetch('/api/activity-logs', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
  } catch (e) {
     
    console.warn('logActivity failed', e)
  }
}

function cryptoRandomId() {
  try {
    if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
      const bytes = new Uint8Array(16)
      crypto.getRandomValues(bytes)
      return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('')
    }
  } catch (error) {
    console.warn('cryptoRandomId fallback to Math.random()', error)
  }
  return Math.random().toString(36).slice(2)
}

