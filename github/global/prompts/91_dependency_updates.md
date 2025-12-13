# 🔄 Automated Dependency Updates

**Priority:** MEDIUM  
**Phase:** 5 (Security) & 6 (Deployment)  
**Status:** Production Ready

---

## 🎯 Purpose

Automate dependency updates using **Dependabot**, **Renovate**, or **npm-check-updates** to keep packages secure and up-to-date.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Update Strategies](#update-strategies)
3. [Tools](#tools)
4. [Implementation](#implementation)
5. [Best Practices](#best-practices)

---

## 1. Overview

### Why Update Dependencies?

**Security:**
- 60% of breaches involve unpatched vulnerabilities
- New vulnerabilities discovered daily
- Outdated packages = security risks

**Performance:**
- Newer versions often faster
- Bug fixes included
- Better optimization

**Features:**
- New capabilities
- Better APIs
- Improved DX

**Compatibility:**
- Stay compatible with ecosystem
- Avoid breaking changes later
- Easier migration

---

## 2. Update Strategies

### 1. Patch Updates (Automatic)
**Version:** `1.2.3` → `1.2.4`  
**Risk:** Very Low  
**Frequency:** Immediately  
**Auto-merge:** ✅ Yes

### 2. Minor Updates (Semi-automatic)
**Version:** `1.2.3` → `1.3.0`  
**Risk:** Low  
**Frequency:** Weekly  
**Auto-merge:** ⚠️ After tests pass

### 3. Major Updates (Manual)
**Version:** `1.2.3` → `2.0.0`  
**Risk:** High (breaking changes)  
**Frequency:** Monthly  
**Auto-merge:** ❌ No (requires review)

---

## 3. Tools

### 1. Dependabot (GitHub)

**Setup:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  # npm dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    reviewers:
      - "your-username"
    assignees:
      - "your-username"
    commit-message:
      prefix: "chore"
      prefix-development: "chore"
      include: "scope"
    
    # Auto-merge patch updates
    allow:
      - dependency-type: "all"
    
    # Group updates
    groups:
      development-dependencies:
        dependency-type: "development"
        update-types:
          - "minor"
          - "patch"
      
      production-dependencies:
        dependency-type: "production"
        update-types:
          - "patch"
    
    # Ignore specific packages
    ignore:
      - dependency-name: "react"
        versions: ["17.x"]
      - dependency-name: "webpack"
        update-types: ["version-update:semver-major"]
  
  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
```

**Features:**
- ✅ Automatic PR creation
- ✅ Security updates
- ✅ Grouped updates
- ✅ Auto-merge (with GitHub Actions)
- ✅ Free for public repos

---

### 2. Renovate

**Setup:**
```json
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:base"
  ],
  "schedule": ["before 10am on monday"],
  "timezone": "America/New_York",
  "labels": ["dependencies"],
  "assignees": ["your-username"],
  "reviewers": ["your-username"],
  
  "packageRules": [
    {
      "description": "Auto-merge patch updates",
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "pr",
      "automergeStrategy": "squash"
    },
    {
      "description": "Auto-merge minor dev dependencies",
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["minor"],
      "automerge": true
    },
    {
      "description": "Group all non-major updates",
      "matchUpdateTypes": ["minor", "patch"],
      "groupName": "all non-major dependencies",
      "groupSlug": "all-minor-patch"
    },
    {
      "description": "Separate major updates",
      "matchUpdateTypes": ["major"],
      "addLabels": ["breaking-change"]
    },
    {
      "description": "Pin dependencies",
      "matchDepTypes": ["dependencies"],
      "rangeStrategy": "pin"
    }
  ],
  
  "vulnerabilityAlerts": {
    "labels": ["security"],
    "assignees": ["security-team"]
  },
  
  "lockFileMaintenance": {
    "enabled": true,
    "schedule": ["before 10am on monday"]
  }
}
```

**Features:**
- ✅ More configuration options
- ✅ Multi-platform (GitHub, GitLab, Bitbucket)
- ✅ Custom rules
- ✅ Dependency dashboard
- ✅ Free for open source

---

### 3. npm-check-updates

**Installation:**
```bash
npm install -g npm-check-updates
```

**Usage:**
```bash
# Check for updates
ncu

# Check specific package
ncu react

# Update package.json (dry run)
ncu -u

# Update and install
ncu -u && npm install

# Interactive mode
ncu -i

# Only patch updates
ncu -t patch

# Only minor updates
ncu -t minor

# Exclude packages
ncu -x react,webpack

# Filter by pattern
ncu -f "eslint-*"
```

**Script:**
```bash
# scripts/update-dependencies.sh
#!/bin/bash

echo "🔄 Checking for dependency updates..."

# Check for updates
ncu

# Ask for confirmation
read -p "Update dependencies? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
  # Backup package.json
  cp package.json package.json.backup
  
  # Update
  ncu -u
  npm install
  
  # Run tests
  npm test
  
  if [ $? -eq 0 ]; then
    echo "✅ Updates successful!"
    rm package.json.backup
  else
    echo "❌ Tests failed! Rolling back..."
    mv package.json.backup package.json
    npm install
  fi
fi
```

---

### 4. Snyk

**Installation:**
```bash
npm install -g snyk
snyk auth
```

**Usage:**
```bash
# Test for vulnerabilities
snyk test

# Fix vulnerabilities
snyk fix

# Monitor project
snyk monitor

# Upgrade to fix vulnerabilities
snyk upgrade
```

**Configuration:**
```yaml
# .snyk
version: v1.22.0
ignore: {}
patch: {}
```

---

## 4. Implementation

### Step 1: Setup Dependabot

```bash
# Create config
mkdir -p .github
cat > .github/dependabot.yml << 'EOF'
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    groups:
      development-dependencies:
        dependency-type: "development"
        update-types: ["minor", "patch"]
EOF

# Commit
git add .github/dependabot.yml
git commit -m "chore: add Dependabot configuration"
git push
```

---

### Step 2: Setup Auto-merge

```yaml
# .github/workflows/auto-merge-dependabot.yml
name: Auto-merge Dependabot PRs

on:
  pull_request:
    branches: [main]

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Check PR
        id: check
        uses: actions/github-script@v6
        with:
          script: |
            const pr = context.payload.pull_request;
            const title = pr.title.toLowerCase();
            
            // Only auto-merge patch updates
            const isPatch = title.includes('patch') || 
                           title.match(/bump .* from \d+\.\d+\.\d+ to \d+\.\d+\.\d+/);
            
            return isPatch;
      
      - name: Enable auto-merge
        if: steps.check.outputs.result == 'true'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

### Step 3: Create Update Script

```javascript
// scripts/check-updates.js
const { execSync } = require('child_process');
const fs = require('fs');

function checkUpdates() {
  console.log('🔄 Checking for dependency updates...\n');
  
  try {
    // Get outdated packages
    const result = execSync('npm outdated --json', { encoding: 'utf8' });
    const outdated = JSON.parse(result);
    
    const updates = {
      patch: [],
      minor: [],
      major: []
    };
    
    for (const [pkg, info] of Object.entries(outdated)) {
      const current = info.current.split('.');
      const latest = info.latest.split('.');
      
      if (latest[0] > current[0]) {
        updates.major.push({ pkg, current: info.current, latest: info.latest });
      } else if (latest[1] > current[1]) {
        updates.minor.push({ pkg, current: info.current, latest: info.latest });
      } else if (latest[2] > current[2]) {
        updates.patch.push({ pkg, current: info.current, latest: info.latest });
      }
    }
    
    // Generate report
    const report = `# Dependency Updates Report

**Date:** ${new Date().toISOString()}

---

## Summary

| Type | Count |
|------|-------|
| Patch | ${updates.patch.length} |
| Minor | ${updates.minor.length} |
| Major | ${updates.major.length} |

---

## Patch Updates (Safe to auto-update)

${updates.patch.length > 0 ? updates.patch.map(u => 
  `- **${u.pkg}**: ${u.current} → ${u.latest}`
).join('\n') : '*No patch updates available*'}

---

## Minor Updates (Review recommended)

${updates.minor.length > 0 ? updates.minor.map(u => 
  `- **${u.pkg}**: ${u.current} → ${u.latest}`
).join('\n') : '*No minor updates available*'}

---

## Major Updates (Breaking changes possible)

${updates.major.length > 0 ? updates.major.map(u => 
  `- **${u.pkg}**: ${u.current} → ${u.latest} ⚠️`
).join('\n') : '*No major updates available*'}

---

## Recommendations

${updates.patch.length > 0 ? '✅ **Patch updates:** Safe to apply immediately\n' : ''}
${updates.minor.length > 0 ? '⚠️ **Minor updates:** Review changelog and test\n' : ''}
${updates.major.length > 0 ? '🚨 **Major updates:** Review breaking changes carefully\n' : ''}

---

**Generated by:** Dependency Update System  
**Version:** 1.0
`;

    fs.writeFileSync('reports/DEPENDENCY_UPDATES.md', report);
    fs.writeFileSync('reports/dependency-updates.json', JSON.stringify(updates, null, 2));
    
    console.log('📊 Update Summary:');
    console.log(`Patch: ${updates.patch.length}`);
    console.log(`Minor: ${updates.minor.length}`);
    console.log(`Major: ${updates.major.length}`);
    console.log('\n📁 Report: reports/DEPENDENCY_UPDATES.md');
    
  } catch (error) {
    console.log('✅ All dependencies up to date!');
  }
}

checkUpdates();
```

---

### Step 4: Add to package.json

```bash
npm pkg set scripts.deps:check="node scripts/check-updates.js"
npm pkg set scripts.deps:update="ncu -u && npm install"
npm pkg set scripts.deps:patch="ncu -t patch -u && npm install"
npm pkg set scripts.deps:minor="ncu -t minor -u && npm install"
```

---

### Step 5: Schedule Regular Checks

```yaml
# .github/workflows/dependency-check.yml
name: Dependency Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Check for updates
        run: npm run deps:check
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: dependency-report
          path: reports/DEPENDENCY_UPDATES.md
      
      - name: Create issue if updates available
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const updates = JSON.parse(fs.readFileSync('reports/dependency-updates.json', 'utf8'));
            const total = updates.patch.length + updates.minor.length + updates.major.length;
            
            if (total > 0) {
              const report = fs.readFileSync('reports/DEPENDENCY_UPDATES.md', 'utf8');
              github.rest.issues.create({
                owner: context.repo.owner,
                repo: context.repo.repo,
                title: `📦 ${total} dependency updates available`,
                body: report,
                labels: ['dependencies']
              });
            }
```

---

## 5. Best Practices

### DO ✅

1. **Update regularly** - Weekly for patches, monthly for others
2. **Test after updates** - Always run tests
3. **Read changelogs** - Understand what changed
4. **Update one at a time** - For major versions
5. **Use lock files** - package-lock.json, yarn.lock
6. **Monitor security** - Use Snyk, Dependabot
7. **Auto-merge patches** - Safe and saves time
8. **Group minor updates** - Easier to review
9. **Review major updates** - Breaking changes
10. **Keep CI green** - Don't merge if tests fail

### DON'T ❌

1. **Don't ignore updates** - Security risks
2. **Don't update blindly** - Read changelogs
3. **Don't skip tests** - Updates can break things
4. **Don't update everything at once** - Hard to debug
5. **Don't ignore warnings** - They're there for a reason
6. **Don't use outdated packages** - Security vulnerabilities
7. **Don't auto-merge major** - Breaking changes
8. **Don't forget lock files** - Commit them
9. **Don't ignore deprecations** - Plan migration
10. **Don't delay major updates** - Gets harder over time

---

## 🎯 Integration with Our System

### Phase 5: Security
- Check for security updates
- Apply critical patches
- Review vulnerabilities

### Phase 6: Deployment
- Setup Dependabot/Renovate
- Configure auto-merge
- Schedule regular checks

### Checkpoints
- ✅ No critical vulnerabilities
- ✅ All patches applied
- ✅ Automated updates configured
- ✅ Tests pass after updates
- ✅ Lock files committed

---

## 📚 Resources

- [Dependabot](https://docs.github.com/en/code-security/dependabot)
- [Renovate](https://docs.renovatebot.com/)
- [npm-check-updates](https://github.com/raineorshine/npm-check-updates)
- [Snyk](https://snyk.io/)

---

**Status:** ✅ Production Ready  
**Last Updated:** 2025-11-17  
**Version:** 1.0

