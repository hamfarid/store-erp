# Perfect Authentication Flow (Global System v26 Diamond 32)

**Status:** MANDATORY REFERENCE
**Philosophy:** "Security by Design" via Swarm Protocol.

## 1. 🧠 The Planner's Blueprint
Before writing code, we must define the security constraints:
*   **Constraint 1:** No LocalStorage for Tokens (XSS Risk). Use `HttpOnly` Cookies.
*   **Constraint 2:** Passwords must be hashed with `bcrypt` (Cost factor 12+).
*   **Constraint 3:** Rate Limiting is mandatory on `/login` routes.

## 2. 🛠️ The Executor's Implementation
*Note how The Executor follows the Planner's constraints exactly.*

```javascript
// auth.controller.js
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

async function register(req, res) {
  // 1. Input Validation (Sanitization)
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ error: 'Missing credentials' });

  // 2. Password Strength Check
  if (password.length < 12) return res.status(400).json({ error: 'Password too weak' });

  try {
    // 3. Hashing (Cost 12)
    const hashedPassword = await bcrypt.hash(password, 12);
    
    // 4. Database Insert (Parameterized Query)
    const user = await db.query(
      'INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email',
      [email, hashedPassword]
    );

    // 5. Token Generation
    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '15m' });
    
    // 6. Secure Cookie Delivery (HttpOnly)
    res.cookie('token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 15 * 60 * 1000 // 15 mins
    });

    res.status(201).json({ user });
  } catch (error) {
    // 7. Error Handling (No Leakage)
    console.error('Registration error:', error); 
    res.status(500).json({ error: 'Internal Server Error' }); // Generic message to user
  }
}
```

## 3. 🧐 The Reviewer's Audit Checklist
*   [ ] Is `bcrypt` cost factor >= 12? **(Yes)**
*   [ ] Is `HttpOnly` set to `true`? **(Yes)**
*   [ ] Is `process.env.JWT_SECRET` used (not hardcoded)? **(Yes)**
*   [ ] Are error messages generic (no stack traces)? **(Yes)**

## 4. ⚖️ The Critic's Edge Case Test
*   **Scenario:** "What if I send a 10MB password?" -> *Executor should add body-parser limit.*
*   **Scenario:** "What if the DB is down?" -> *Executor handled try/catch correctly.*
*   **Verdict:** **APPROVED**.
