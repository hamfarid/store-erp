# FILE: docs/Secret_Scanning_Guide.md | PURPOSE: Secret Scanning Documentation | OWNER: Security Team | RELATED: .secrets.baseline | LAST-AUDITED: 2025-11-19

# Secret Scanning Guide

**Purpose**: Automated detection of hardcoded secrets in the codebase  
**Tool**: `detect-secrets` v1.5.0 (Yelp)  
**Status**: ✅ **ACTIVE** - Integrated with CI/CD

---

## Overview

Secret scanning is a critical security measure that prevents accidental commits of sensitive information such as:
- API keys
- Passwords
- Private keys
- Access tokens
- Database credentials
- AWS/Azure/GCP credentials

**OSF Framework Compliance**:
- Security: 35% weight - Prevents credential leaks
- Correctness: 20% weight - Ensures no secrets in code
- Reliability: 15% weight - Automated, consistent scanning

---

## Installation

### Local Development

```bash
# Install detect-secrets
pip install detect-secrets==1.5.0

# Verify installation
detect-secrets --version
```

### CI/CD

Secret scanning is automatically run on:
- ✅ Every push to `main`, `develop`, `staging` branches
- ✅ Every pull request
- ✅ Daily scheduled scan at 2 AM UTC

See `.github/workflows/security-scan.yml` for details.

---

## Usage

### 1. Initial Baseline Creation

```bash
# Generate baseline (already done)
detect-secrets scan > .secrets.baseline
```

**Current Status**: ✅ Baseline created on 2025-11-19  
**Result**: 🎉 **No secrets detected!**

### 2. Scan for New Secrets

```bash
# Scan and compare with baseline
detect-secrets scan --baseline .secrets.baseline

# Fail if new secrets found
detect-secrets scan --baseline .secrets.baseline --fail-on-unaudited
```

### 3. Audit Detected Secrets

If secrets are detected:

```bash
# Interactive audit
detect-secrets audit .secrets.baseline
```

For each detected secret:
- Press `y` if it's a real secret (will fail CI)
- Press `n` if it's a false positive (will be ignored)
- Press `s` to skip

### 4. Update Baseline

After auditing false positives:

```bash
# Update baseline with audited results
detect-secrets scan --baseline .secrets.baseline --update
```

---

## Plugins Enabled

The following secret detectors are active:

1. ✅ **ArtifactoryDetector** - Artifactory tokens
2. ✅ **AWSKeyDetector** - AWS access keys
3. ✅ **AzureStorageKeyDetector** - Azure storage keys
4. ✅ **Base64HighEntropyString** - High-entropy base64 strings
5. ✅ **BasicAuthDetector** - Basic auth credentials
6. ✅ **CloudantDetector** - Cloudant credentials
7. ✅ **DiscordBotTokenDetector** - Discord bot tokens
8. ✅ **GitHubTokenDetector** - GitHub tokens
9. ✅ **HexHighEntropyString** - High-entropy hex strings
10. ✅ **IbmCloudIamDetector** - IBM Cloud IAM keys
11. ✅ **IbmCosHmacDetector** - IBM COS HMAC credentials
12. ✅ **IPPublicDetector** - Public IP addresses
13. ✅ **JwtTokenDetector** - JWT tokens
14. ✅ **KeywordDetector** - Common secret keywords
15. ✅ **MailchimpDetector** - Mailchimp API keys
16. ✅ **NpmDetector** - NPM tokens
17. ✅ **PrivateKeyDetector** - Private keys (RSA, SSH, etc.)
18. ✅ **SendGridDetector** - SendGrid API keys
19. ✅ **SlackDetector** - Slack tokens
20. ✅ **SoftlayerDetector** - Softlayer credentials
21. ✅ **SquareOAuthDetector** - Square OAuth secrets
22. ✅ **StripeDetector** - Stripe API keys
23. ✅ **TwilioKeyDetector** - Twilio API keys

---

## Filters Applied

The following heuristic filters reduce false positives:

1. ✅ **is_indirect_reference** - Ignores variable references
2. ✅ **is_likely_id_string** - Ignores ID-like strings
3. ✅ **is_lock_file** - Ignores lock files
4. ✅ **is_not_alphanumeric_string** - Ignores non-alphanumeric
5. ✅ **is_potential_uuid** - Ignores UUIDs
6. ✅ **is_prefixed_with_dollar_sign** - Ignores env vars
7. ✅ **is_sequential_string** - Ignores sequential strings
8. ✅ **is_swagger_file** - Ignores Swagger files
9. ✅ **is_templated_secret** - Ignores template placeholders

---

## CI/CD Integration

### GitHub Actions Workflow

**File**: `.github/workflows/security-scan.yml`

**Jobs**:
1. **secret-scan** - Scans for hardcoded secrets
2. **dependency-scan** - Checks for vulnerable dependencies (safety)
3. **code-quality** - Security linting (bandit, flake8)
4. **security-summary** - Aggregates results

**Triggers**:
- Push to main/develop/staging
- Pull requests
- Daily at 2 AM UTC

**Failure Conditions**:
- ❌ New secrets detected
- ❌ Unaudited secrets in baseline

---

## Best Practices

### 1. Never Commit Secrets

✅ **DO**:
- Use environment variables (`.env` files)
- Use secret management tools (AWS Secrets Manager, Azure Key Vault)
- Use `python-decouple` for configuration

❌ **DON'T**:
- Hardcode API keys in code
- Commit `.env` files (add to `.gitignore`)
- Use default secrets in production

### 2. Regular Scans

- ✅ Run `detect-secrets scan` before committing
- ✅ Review CI/CD scan results
- ✅ Update baseline after auditing false positives

### 3. Incident Response

If a secret is accidentally committed:

1. **Immediately revoke** the compromised secret
2. **Generate new credentials**
3. **Update environment variables**
4. **Remove from Git history**:
   ```bash
   # Use BFG Repo-Cleaner or git-filter-repo
   git filter-repo --path <file-with-secret> --invert-paths
   ```
5. **Force push** (coordinate with team)
6. **Document in incident log**

---

## Verification

### Current Status

✅ **Baseline Created**: 2025-11-19  
✅ **Secrets Detected**: 0  
✅ **CI/CD Integrated**: Yes  
✅ **Daily Scans**: Enabled  

### Test Secret Detection

To verify the scanner works:

```bash
# Create a test file with a fake secret
echo "aws_access_key_id = AKIAIOSFODNN7EXAMPLE" > test_secret.txt

# Scan
detect-secrets scan test_secret.txt

# Clean up
rm test_secret.txt
```

Expected: Secret should be detected! ✅

---

## Troubleshooting

### False Positives

If legitimate code is flagged:

1. Audit the baseline: `detect-secrets audit .secrets.baseline`
2. Mark as false positive (press `n`)
3. Update baseline: `detect-secrets scan --baseline .secrets.baseline --update`
4. Commit updated baseline

### CI/CD Failures

If CI fails due to secret detection:

1. Review the scan results in GitHub Actions artifacts
2. Identify the detected secret
3. Remove the secret from code
4. Use environment variables instead
5. Re-run the pipeline

---

## References

- **detect-secrets Documentation**: https://github.com/Yelp/detect-secrets
- **OSF Framework**: `docs/P0_Security_Fix_Plan.md`
- **Security Guidelines**: `docs/Security.md`

---

**Last Updated**: 2025-11-19  
**Maintained By**: Security Team  
**Review Frequency**: Quarterly


