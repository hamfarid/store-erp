import React from 'react'

export default function CSRFStatusBanner({ status, error }) {
  const text = error ? 'error' : (status ? 'ready' : 'priming…')
  return (
    <div style={{
      position: 'fixed', bottom: 8, left: 8, zIndex: 9999,
      background: '#111827', color: '#fff', padding: '6px 10px',
      borderRadius: 6, fontSize: 12, opacity: 0.9
    }}>
      CSRF: {text}
    </div>
  )
}
