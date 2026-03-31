# Security Best Practices

## Authentication

- Use strong password hashing (Argon2, bcrypt)
- Implement JWT with short expiration times
- Use refresh tokens for long sessions

## Input Validation

- Validate all inputs against a schema
- Sanitize all user-facing output
- Use parameterized queries for SQL

## API Security

- Implement rate limiting
- Use HTTPS everywhere
- Set proper CORS policies
- Use security headers (CSP, HSTS, etc.)
