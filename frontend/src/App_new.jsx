import React from 'react'

function App() {
  return (
    <div style={{ 
      padding: '50px', 
      textAlign: 'center', 
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#f0f9ff',
      minHeight: '100vh',
      direction: 'rtl'
    }}>
      <h1 style={{ 
        color: '#3B82F6', 
        fontSize: '48px', 
        marginBottom: '20px' 
      }}>
        🎉 نجح!
      </h1>
      <h2 style={{ 
        color: '#1e40af', 
        fontSize: '32px', 
        marginBottom: '30px' 
      }}>
        React Frontend يعمل بشكل مثالي!
      </h2>
      <div style={{
        backgroundColor: 'white',
        padding: '30px',
        borderRadius: '12px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        maxWidth: '600px',
        margin: '0 auto'
      }}>
        <p style={{ fontSize: '20px', color: '#374151', marginBottom: '20px' }}>
          ✅ React يعمل
        </p>
        <p style={{ fontSize: '20px', color: '#374151', marginBottom: '20px' }}>
          ✅ Vite يعمل
        </p>
        <p style={{ fontSize: '20px', color: '#374151', marginBottom: '20px' }}>
          ✅ JavaScript يعمل
        </p>
        <p style={{ fontSize: '20px', color: '#374151' }}>
          ✅ CSS يعمل
        </p>
      </div>
      <div style={{ marginTop: '30px' }}>
        <p style={{ fontSize: '18px', color: '#6b7280' }}>
          الرابط: http://localhost:3005
        </p>
        <p style={{ fontSize: '18px', color: '#6b7280' }}>
          HTML Interface: http://127.0.0.1:8000
        </p>
      </div>
    </div>
  )
}

export default App
