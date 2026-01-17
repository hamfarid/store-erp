# GitHub Workflows

These workflow files need to be manually added to `.github/workflows/` directory on GitHub.

## Why Manual?

GitHub requires special permissions to create/modify workflows via API/CLI. 

## How to Add

### Option 1: Via GitHub Web Interface

1. Go to https://github.com/hamfarid/global
2. Navigate to `.github/workflows/` (create if doesn't exist)
3. Click "Add file" → "Create new file"
4. Copy content from `workflows/ci.yml` → paste as `.github/workflows/ci.yml`
5. Repeat for `workflows/deploy.yml`

### Option 2: Via Git (if you have proper permissions)

```bash
cd global
mkdir -p .github/workflows
cp workflows/ci.yml .github/workflows/
cp workflows/deploy.yml .github/workflows/
git add .github/workflows/
git commit -m "Add GitHub workflows"
git push
```

## Files

- `ci.yml` - Continuous Integration pipeline
- `deploy.yml` - Deployment workflow

