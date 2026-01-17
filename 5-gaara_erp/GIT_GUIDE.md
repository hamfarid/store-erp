# Gaara ERP - Git & GitHub Guide

## 🚀 Quick Start

### First Time Setup

```bash
# Run setup script
./scripts/git-setup.sh
```

This will:
1. Initialize git repository (if needed)
2. Add GitHub remote
3. Stage all files
4. Create initial commit
5. Push to GitHub

### Quick Push

```bash
# Quick push with custom message
./scripts/git-push.sh "Your commit message"

# Or interactive
./scripts/git-push.sh
```

## 📝 Manual Git Commands

### Initialize Repository

```bash
# Initialize git
git init

# Add remote
git remote add origin https://github.com/yourusername/gaara-erp.git

# Or if using SSH
git remote add origin git@github.com:yourusername/gaara-erp.git
```

### First Commit

```bash
# Stage all files
git add .

# Commit
git commit -m "feat: Initial commit - Complete Gaara ERP infrastructure"

# Push
git push -u origin main
```

### Regular Workflow

```bash
# Check status
git status

# Stage changes
git add .

# Or stage specific files
git add Dockerfile docker-compose.yml

# Commit
git commit -m "feat: Add Docker configuration"

# Push
git push
```

## 🌿 Branch Management

### Create Feature Branch

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Or using new syntax
git switch -c feature/new-feature

# Push new branch
git push -u origin feature/new-feature
```

### Switch Branches

```bash
# Switch to main
git checkout main

# Or
git switch main
```

### Merge Branch

```bash
# Switch to main
git checkout main

# Merge feature branch
git merge feature/new-feature

# Push
git push
```

## 📋 Commit Message Guidelines

### Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

```bash
git commit -m "feat: Add Docker configuration and deployment scripts"

git commit -m "fix: Correct frontend port configuration (5173 instead of 3000)"

git commit -m "docs: Add comprehensive API documentation"

git commit -m "chore: Update dependencies and configuration files"
```

## 🔄 Common Operations

### View Changes

```bash
# View unstaged changes
git diff

# View staged changes
git diff --staged

# View commit history
git log --oneline

# View file history
git log --follow <filename>
```

### Undo Changes

```bash
# Unstage files
git reset HEAD <file>

# Discard changes to file
git checkout -- <file>

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Update from Remote

```bash
# Fetch changes
git fetch origin

# Pull changes
git pull origin main

# Or rebase
git pull --rebase origin main
```

## 🔐 GitHub Setup

### Generate SSH Key

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
# Then add to GitHub: Settings > SSH and GPG keys
```

### Clone Repository

```bash
# Clone via HTTPS
git clone https://github.com/yourusername/gaara-erp.git

# Clone via SSH
git clone git@github.com:yourusername/gaara-erp.git
```

## 📦 What to Commit

### ✅ Commit These

- Source code files
- Configuration files (`.env.example`, not `.env`)
- Documentation (`.md` files)
- Docker files
- Scripts
- CI/CD configurations

### ❌ Don't Commit

- `.env` files (use `.env.example`)
- `node_modules/`
- `__pycache__/`
- `*.log` files
- Database files
- Build artifacts
- Secrets and keys

## 🏷️ Tagging Releases

```bash
# Create tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tags
git push origin v1.0.0

# Push all tags
git push --tags
```

## 🔍 Troubleshooting

### Remote Not Found

```bash
# Check remotes
git remote -v

# Add remote
git remote add origin <url>

# Update remote
git remote set-url origin <url>
```

### Push Rejected

```bash
# Pull first
git pull origin main --rebase

# Then push
git push origin main
```

### Large Files

```bash
# If you need to track large files, use Git LFS
git lfs install
git lfs track "*.pdf"
git lfs track "*.zip"
```

## 📚 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Last Updated**: 2025-01-15
