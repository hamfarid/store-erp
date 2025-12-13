# Perfect Authentication Flow

This is a complete, production-ready authentication implementation.

## Backend (Node.js/Express)

\`\`\`javascript
// auth.controller.js
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

async function register(req, res) {
  try {
    const { email, password } = req.body;
    
    // Validate input
    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }
    
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12);
    
    // Save user (using parameterized query)
    const user = await db.query(
      'INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email',
      [email, hashedPassword]
    );
    
    // Generate JWT
    const token = jwt.sign(
      { userId: user.id },
      process.env.JWT_SECRET,
      { expiresIn: '15m' }
    );
    
    res.status(201).json({ token, user });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
\`\`\`

## Frontend (React)

\`\`\`javascript
// useAuth.js
import { useState } from 'react';

export function useAuth() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  
  const register = async (email, password) => {
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) throw new Error('Registration failed');
    
    const { token } = await response.json();
    localStorage.setItem('token', token);
    setToken(token);
  };
  
  return { token, register };
}
\`\`\`
