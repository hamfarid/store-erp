import React, { useEffect, useState } from 'react';
import './App.css';

// Global System Ultimate - Frontend Template
// Verified Feb 2026: React 19.2.4 (Server Components)

interface SystemStatus {
  system: string;
  version: string;
  status: string;
  mode: string;
}

function App() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Dynamic API URL from Environment
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetch(`${API_URL}/`)
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(err => setError(err.message));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 Global System Ultimate</h1>
        <p>Universal AI Development Framework</p>
        
        <div className="status-card">
          <h2>System Status</h2>
          {error ? (
            <p className="error">Error: {error}</p>
          ) : status ? (
            <ul>
              <li><strong>System:</strong> {status.system}</li>
              <li><strong>Version:</strong> {status.version}</li>
              <li><strong>Status:</strong> {status.status}</li>
              <li><strong>Mode:</strong> {status.mode}</li>
            </ul>
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
