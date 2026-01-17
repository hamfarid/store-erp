# Threat Model & Risk Assessment

**Last Updated:** 2025-11-04  
**Owner:** Security Team  
**Status:** ✅ Current

---

## Overview

OWASP/STRIDE threat model for the Store application.

## STRIDE Analysis

### Spoofing (Authentication)

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|-----------|
| Credential stuffing | High | High | Rate limiting, lockout, MFA |
| Session hijacking | Medium | High | Secure cookies, HTTPS, CSRF |
| JWT token theft | Medium | High | Short TTL, rotation, revocation |
| API key compromise | Medium | High | Key rotation, monitoring |

### Tampering (Integrity)

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|-----------|
| SQL injection | Low | Critical | Parameterized queries (ORM) |
| API request tampering | Low | High | HTTPS, CSRF, signature validation |
| Database corruption | Low | Critical | Backups, transactions, constraints |
| Code injection | Low | Critical | Input validation, sanitization |

### Repudiation (Non-Repudiation)

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|-----------|
| User denies action | Medium | Medium | Audit logging, timestamps |
| Admin denies change | Low | Medium | Audit trail, approval workflow |
| Payment denial | Medium | High | Transaction logs, receipts |

### Information Disclosure (Confidentiality)

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|-----------|
| PII exposure | Medium | Critical | Encryption, access control, redaction |
| API response leakage | Low | Medium | Error handling, logging |
| Database breach | Low | Critical | Encryption, backups, monitoring |
| Log file exposure | Low | High | Secure storage, access control |
| Backup exposure | Low | Critical | Encryption, secure storage |

### Denial of Service (Availability)

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|-----------|
| API rate limiting bypass | Medium | High | Adaptive rate limiting |
| Database connection exhaustion | Low | High | Connection pooling, limits |
| Large file upload | Medium | Medium | File size limits, scanning |
| Slowloris attack | Low | Medium | Request timeouts |
| DDoS attack | Low | High | WAF, CDN, rate limiting |

### Elevation of Privilege (Authorization)

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|-----------|
| RBAC bypass | Low | Critical | Permission checks, tests |
| Admin account compromise | Low | Critical | MFA, monitoring, alerts |
| Role escalation | Low | High | Permission validation |
| API endpoint bypass | Low | High | Authentication on all endpoints |

## Attack Vectors

### External Attackers

1. **Brute Force Login**
   - **Method:** Automated login attempts
   - **Mitigation:** Lockout (5 attempts/15 min), rate limiting, MFA
   - **Detection:** Monitor failed login attempts

2. **SQL Injection**
   - **Method:** Malicious SQL in input fields
   - **Mitigation:** Parameterized queries (ORM), input validation
   - **Detection:** WAF, code analysis

3. **XSS Attack**
   - **Method:** Inject malicious scripts
   - **Mitigation:** CSP nonces, output encoding, input sanitization
   - **Detection:** CSP violations, WAF

4. **CSRF Attack**
   - **Method:** Trick user into unwanted action
   - **Mitigation:** CSRF tokens, SameSite cookies
   - **Detection:** Token validation failures

5. **API Abuse**
   - **Method:** Excessive requests, data scraping
   - **Mitigation:** Rate limiting, authentication, monitoring
   - **Detection:** Anomalous request patterns

### Insider Threats

1. **Malicious Admin**
   - **Method:** Abuse admin privileges
   - **Mitigation:** Audit logging, approval workflows, monitoring
   - **Detection:** Unusual admin actions

2. **Compromised Employee Account**
   - **Method:** Use employee credentials
   - **Mitigation:** MFA, monitoring, access controls
   - **Detection:** Unusual access patterns

3. **Data Exfiltration**
   - **Method:** Copy sensitive data
   - **Mitigation:** DLP, monitoring, encryption
   - **Detection:** Large data exports, unusual queries

### Supply Chain

1. **Dependency Vulnerability**
   - **Method:** Exploit vulnerable library
   - **Mitigation:** SBOM, scanning, updates
   - **Detection:** Grype, Trivy scans

2. **Compromised Dependency**
   - **Method:** Malicious code in library
   - **Mitigation:** Signature verification, monitoring
   - **Detection:** Behavior analysis

## Risk Matrix

| Risk | Likelihood | Impact | Priority | Mitigation |
|------|-----------|--------|----------|-----------|
| Credential stuffing | High | High | P0 | Lockout, MFA, rate limit |
| Database breach | Low | Critical | P0 | Encryption, backups, monitoring |
| SQL injection | Low | Critical | P0 | ORM, validation |
| Admin compromise | Low | Critical | P1 | MFA, monitoring |
| API abuse | Medium | High | P1 | Rate limiting, auth |
| XSS attack | Low | High | P1 | CSP, encoding |
| CSRF attack | Low | High | P1 | CSRF tokens |
| DDoS attack | Low | High | P2 | WAF, CDN |

## Security Controls

### Preventive Controls

- Authentication (JWT, MFA)
- Authorization (RBAC)
- Encryption (TLS, AES-256)
- Input validation
- Output encoding
- Rate limiting
- CSRF protection

### Detective Controls

- Audit logging
- Monitoring & alerting
- Anomaly detection
- Security scanning
- Penetration testing

### Corrective Controls

- Incident response
- Backup & recovery
- Patch management
- Security updates

## Compliance

### Standards Addressed

- **OWASP Top 10:** All items addressed
- **GDPR:** Data protection, deletion, consent
- **PCI DSS:** If handling payment cards
- **SOC 2:** Audit-ready

### Audit Trail

- All security events logged
- 90-day retention minimum
- Structured JSON format
- Includes: timestamp, user, action, resource, result, IP

## Incident Response

### Severity Levels

| Level | Response Time | Escalation |
|-------|---------------|------------|
| Critical | 15 min | VP Eng + CTO |
| High | 1 hour | Engineering Lead |
| Medium | 4 hours | Team Lead |
| Low | 24 hours | Backlog |

### Response Process

1. **Detection:** Alert triggered
2. **Triage:** Assess severity
3. **Containment:** Stop the bleeding
4. **Eradication:** Remove threat
5. **Recovery:** Restore systems
6. **Post-Incident:** RCA + improvements

## Security Roadmap

### Q1 2025

- [ ] Penetration testing
- [ ] Security training
- [ ] KMS/Vault integration

### Q2 2025

- [ ] Advanced threat detection
- [ ] Security incident response drill
- [ ] Compliance audit

### Q3 2025

- [ ] Zero-trust architecture
- [ ] Advanced authentication
- [ ] Security hardening

### Q4 2025

- [ ] Disaster recovery drill
- [ ] Security certification
- [ ] Continuous monitoring

---

**Next Steps:**

- [ ] Conduct penetration testing
- [ ] Implement advanced threat detection
- [ ] Create security incident response plan
- [ ] Schedule security training
