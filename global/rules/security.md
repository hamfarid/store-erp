# 🔒 Security Rules

## Mindset
**You are paranoid. Everything is a threat until proven safe.**

## Core Principles
- Trust no input
- Validate everything
- Assume breach
- Defense in depth

## Input Validation
- Validate all user inputs
- Sanitize all outputs
- Use whitelist, not blacklist
- Reject invalid data

## Authentication
- Use strong password hashing (bcrypt, Argon2)
- Implement MFA when possible
- Use secure session management
- Implement rate limiting

## Authorization
- Principle of least privilege
- Check permissions on every request
- Don't trust client-side checks
- Implement RBAC properly

## Data Protection
- Encrypt sensitive data
- Use HTTPS everywhere
- Secure API keys
- Don't log sensitive data

## SQL Injection
- Use parameterized queries
- Never concatenate SQL
- Use ORM safely
- Validate inputs

## XSS Prevention
- Escape all outputs
- Use Content Security Policy
- Sanitize HTML inputs
- Use framework protections

## CSRF Protection
- Use CSRF tokens
- Validate origin
- Use SameSite cookies
- Check Referer header

## Remember
**Assume everything is malicious. Protect everything.**

Be paranoid. Be thorough. Be secure.
