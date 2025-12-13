# T30: GitHub Branch Protection Configuration Guide

**Task:** Configure branch protection rules for the `main` branch  
**Repository:** hamfarid/Store  
**Date:** 2025-11-10  
**Status:** 📋 **MANUAL CONFIGURATION REQUIRED**

---

## Branch Protection Rules to Configure

### Access Instructions

1. Go to: https://github.com/hamfarid/Store/settings/branches
2. Click **"Add rule"** or **"Add branch protection rule"**
3. In **"Branch name pattern"**, enter: `main`

---

## Required Protection Rules

### ✅ **1. Require Pull Request Reviews Before Merging**

**Enable:** ✅ **Require a pull request before merging**

**Sub-settings:**
- ✅ **Require approvals:** `1` (minimum)
- ✅ **Dismiss stale pull request approvals when new commits are pushed**
- ✅ **Require review from Code Owners** (if CODEOWNERS file exists)
- ⬜ **Restrict who can dismiss pull request reviews** (optional)
- ✅ **Allow specified actors to bypass required pull requests** (select repository admins only)

**Purpose:** Ensures all changes go through code review before merging to main.

---

### ✅ **2. Require Status Checks to Pass Before Merging**

**Enable:** ✅ **Require status checks to pass before merging**

**Sub-settings:**
- ✅ **Require branches to be up to date before merging**

**Required status checks to select** (from your GitHub Actions workflows):
1. ✅ `backend-tests` - Backend unit tests
2. ✅ `e2e-tests` - End-to-end Playwright tests
3. ✅ `build-check` - Build verification
4. ✅ `security-scan` - OWASP ZAP security scan
5. ✅ `lint` - Code linting checks
6. ⚠️ `k6-performance` - Performance tests (optional, may be slow)

**Purpose:** Prevents merging code that fails automated tests.

---

### ✅ **3. Require Conversation Resolution Before Merging**

**Enable:** ✅ **Require conversation resolution before merging**

**Purpose:** Ensures all review comments are addressed.

---

### ✅ **4. Require Signed Commits** (Optional but Recommended)

**Enable:** ✅ **Require signed commits**

**Purpose:** Adds cryptographic verification to commits for enhanced security.

**Setup Instructions:** 
- Follow: https://docs.github.com/en/authentication/managing-commit-signature-verification

---

### ✅ **5. Require Linear History**

**Enable:** ✅ **Require linear history**

**Purpose:** Prevents merge commits, requires rebase or squash merging.

---

### ✅ **6. Include Administrators**

**Enable:** ✅ **Include administrators**

**Purpose:** Repository admins must also follow protection rules (recommended for best practices).

---

### ✅ **7. Restrict Push Access**

**Enable:** ✅ **Restrict who can push to matching branches**

**Allowed actors:**
- ⬜ **Do NOT allow direct pushes** (force all changes through PRs)
- OR
- ✅ **Allow only repository admins** (emergency access)

**Purpose:** Prevents accidental direct commits to main branch.

---

### ✅ **8. Allow Force Pushes** (DISABLE)

**Enable:** ⬜ **DO NOT enable** (leave unchecked)

**Purpose:** Prevents rewriting main branch history.

---

### ✅ **9. Allow Deletions** (DISABLE)

**Enable:** ⬜ **DO NOT enable** (leave unchecked)

**Purpose:** Prevents accidental deletion of main branch.

---

## Recommended Configuration Summary

```yaml
Branch: main
Protection Rules:
  ✅ Require pull request reviews: 1 approval
  ✅ Require status checks: backend-tests, e2e-tests, build-check, security-scan
  ✅ Require branches up to date
  ✅ Require conversation resolution
  ✅ Require signed commits (optional)
  ✅ Require linear history
  ✅ Include administrators
  ✅ Restrict pushes (PRs only)
  ⬜ Allow force pushes: DISABLED
  ⬜ Allow deletions: DISABLED
```

---

## Verification Steps

After configuring, verify the rules:

1. **Test Pull Request Creation:**
   ```bash
   git checkout -b test/branch-protection
   echo "test" >> README.md
   git add README.md
   git commit -m "test: Verify branch protection"
   git push origin test/branch-protection
   ```

2. **Attempt Direct Push to Main (Should Fail):**
   ```bash
   git checkout main
   echo "test" >> README.md
   git add README.md
   git commit -m "test: Should be blocked"
   git push origin main
   # Expected: ERROR: Protected branch hook declined
   ```

3. **Create Pull Request:**
   - Go to GitHub and create PR from test branch
   - Verify status checks are required
   - Verify approval is required before merge

---

## Alternative: GitHub CLI Configuration

If GitHub CLI (`gh`) is installed, use this command:

```bash
gh api repos/hamfarid/Store/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=backend-tests \
  --field required_status_checks[contexts][]=e2e-tests \
  --field required_status_checks[contexts][]=build-check \
  --field required_pull_request_reviews[required_approving_review_count]=1 \
  --field required_pull_request_reviews[dismiss_stale_reviews]=true \
  --field enforce_admins=true \
  --field required_linear_history=true \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field restrictions=null
```

---

## Current Status Check

**Current Branch:** `test/ci-cd-verification`  
**Active PR:** #26 "test: CI/CD Pipeline Verification (T19/T20)"  
**Main Branch Protected:** ⚠️ **TO BE VERIFIED**

**Check current protection:**
```bash
gh api repos/hamfarid/Store/branches/main/protection
```

---

## Post-Configuration Tasks

1. ✅ Update team documentation about PR workflow
2. ✅ Notify team members about new protection rules
3. ✅ Create PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
4. ✅ Set up CODEOWNERS file (`.github/CODEOWNERS`)
5. ✅ Document exception process for emergency fixes

---

## Exception Process (Emergency Hotfixes)

If emergency changes are needed:

1. **Repository Admin** can temporarily disable protection:
   - Go to Settings → Branches → main → Edit rule
   - Uncheck "Include administrators"
   - Make emergency fix
   - Re-enable protection immediately

2. **Better Approach:** Use emergency branch pattern:
   ```bash
   git checkout -b hotfix/critical-issue
   # Make fix
   git push origin hotfix/critical-issue
   # Create PR with "URGENT" label
   # Admin fast-track review and merge
   ```

---

## Completion Checklist

- [ ] Navigate to GitHub repository settings
- [ ] Add branch protection rule for `main`
- [ ] Enable all required settings (see summary above)
- [ ] Add required status checks
- [ ] Save protection rule
- [ ] Verify with test push (should fail)
- [ ] Verify with test PR (should require approval)
- [ ] Document configuration in team wiki
- [ ] Update README with PR workflow instructions

---

## Related Documentation

- **GitHub Docs:** https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- **Best Practices:** https://docs.github.com/en/code-security/getting-started/best-practices-for-securing-your-code
- **Status Checks:** https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks

---

## T30 Status: ⚠️ **AWAITING MANUAL CONFIGURATION**

**Next Steps:**
1. Repository owner/admin navigates to GitHub settings
2. Applies all protection rules as documented above
3. Verifies configuration with test PR
4. Updates this document with completion date

**Estimated Time:** 10-15 minutes
