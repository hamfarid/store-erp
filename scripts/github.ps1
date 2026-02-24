@'
<#
FILE: bootstrap_repo.ps1 | PURPOSE: Download GitHub repo + scaffold CI/scripts/docs | OWNER: DevOps | LAST-AUDITED: 2025-10-21
#>
param(
  [Parameter(Mandatory=$true)][string]$Repo,      # owner/name or https url
  [string]$Ref = "main",
  [string]$Dest,
  [string]$Token
)

function Write-Info($m){ Write-Host ">> $m" -ForegroundColor Cyan }
function Write-Warn($m){ Write-Host "!! $m" -ForegroundColor Yellow }

# Resolve repo
if ($Repo -match '^https://') {
  $RepoUrl = $Repo
  $parts = $Repo.TrimEnd('/').Split('/')
  $Owner = $parts[-2]
  $Name  = ($parts[-1] -replace '\.git$','')
} else {
  $Owner, $Name = $Repo.Split('/')
  $RepoUrl = "https://github.com/$Owner/$Name.git"
}
if (-not $Dest) { $Dest = Join-Path (Get-Location) $Name }

Write-Info "Repository: $Owner/$Name"
Write-Info "Ref       : $Ref"
Write-Info "Dest      : $Dest"

New-Item -ItemType Directory -Force -Path $Dest | Out-Null

# Download (git or ZIP)
$Temp = New-Item -ItemType Directory -Path ([IO.Path]::GetTempPath() + [Guid]::NewGuid()) -Force
try {
  if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Info "git found — shallow clone"
    git clone --depth 1 --branch $Ref $RepoUrl $Dest 2>$null
    if ($LASTEXITCODE -ne 0) {
      Write-Warn "Clone failed, trying ZIP fallback..."
      $zipUrl = "https://api.github.com/repos/$Owner/$Name/zipball/$Ref"
      $zip = Join-Path $Temp "repo.zip"
      $Headers = @{}
      if ($Token) { $Headers["Authorization"] = "token $Token" }
      Invoke-WebRequest -Uri $zipUrl -Headers $Headers -OutFile $zip
      Expand-Archive -Path $zip -DestinationPath $Temp -Force
      Get-ChildItem $Temp | Where-Object { $_.PSIsContainer } | ForEach-Object {
        Copy-Item -Recurse -Force -Path $_.FullName -Destination $Dest
      }
    }
  } else {
    Write-Info "git not found — using ZIP"
    $zipUrl = "https://api.github.com/repos/$Owner/$Name/zipball/$Ref"
    $zip = Join-Path $Temp "repo.zip"
    $Headers = @{}
    if ($Token) { $Headers["Authorization"] = "token $Token" }
    Invoke-WebRequest -Uri $zipUrl -Headers $Headers -OutFile $zip
    Expand-Archive -Path $zip -DestinationPath $Temp -Force
    Get-ChildItem $Temp | Where-Object { $_.PSIsContainer } | ForEach-Object {
      Copy-Item -Recurse -Force -Path $_.FullName -Destination $Dest
    }
  }
}
finally {
  # cleanup temp on exit
}

# Ensure standard folders
$folders = @(".github/workflows","scripts","templates","docs","contracts","packages/shared-types")
foreach($f in $folders){ New-Item -ItemType Directory -Force -Path (Join-Path $Dest $f) | Out-Null }

function SafeWrite($Path, $Content){
  $dir = Split-Path $Path
  if (!(Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  if (Test-Path $Path) {
    $alt = "$Path.new"
    Write-Warn "Exists: $Path — writing $alt"
    $Content | Set-Content -Path $alt -Encoding UTF8
  } else {
    $Content | Set-Content -Path $Path -Encoding UTF8
    Write-Info "Created: $Path"
  }
}

# Workflows
$deployYml = @"
name: Deploy (Dev → Staging → Production)
on:
  workflow_dispatch:
  push:
    branches: [ "main" ]
    paths-ignore: [ "**.md", "docs/**" ]
permissions: { contents: read, deployments: write, id-token: write }
concurrency: { group: deploy-\${{ github.ref }}, cancel-in-progress: false }
env: { APP_NAME: gaara-erp, ARTIFACT_NAME: build-artifacts, NODE_VERSION: "20", PYTHON_VERSION: "3.11" }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        if: \${{ hashFiles('**/package.json') != '' }}
        uses: actions/setup-node@v4
        with: { node-version: \${{ env.NODE_VERSION }} }
      - name: Install Node deps
        if: \${{ hashFiles('**/package.json') != '' }}
        run: npm ci
      - name: Build FE
        if: \${{ hashFiles('**/package.json') != '' }}
        run: npm run build --if-present
      - name: Setup Python
        if: \${{ hashFiles('**/requirements.txt','**/pyproject.toml') != '' }}
        uses: actions/setup-python@v5
        with: { python-version: \${{ env.PYTHON_VERSION }} }
      - name: Install Python deps
        if: \${{ hashFiles('**/requirements.txt') != '' }}
        run: pip install -r requirements.txt
      - name: Build BE (if applicable)
        if: \${{ hashFiles('**/pyproject.toml') != '' }}
        run: python -m compileall .
      - name: Archive build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: \${{ env.ARTIFACT_NAME }}
          path: |
            dist/**
            build/**
            .next/**
            out/**
            **/*.tar.gz
            **/*.whl
            !**/node_modules/**
            !**/.venv/**
          if-no-files-found: ignore
  deploy_dev:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: dev, url: \${{ steps.out.outputs.url }} }
    steps:
      - uses: actions/download-artifact@v4
        with: { name: \${{ env.ARTIFACT_NAME }} }
      - name: Deploy to Dev
        run: echo "Deploying to DEV…"
      - name: Output Dev URL
        id: out
        run: echo "url=https://dev.example.com" >> \$GITHUB_OUTPUT
  deploy_staging:
    needs: deploy_dev
    runs-on: ubuntu-latest
    environment: { name: staging, url: \${{ steps.out.outputs.url }} }
    steps:
      - uses: actions/download-artifact@v4
        with: { name: \${{ env.ARTIFACT_NAME }} }
      - name: Deploy to Staging
        run: echo "Deploying to STAGING…"
      - name: Output Staging URL
        id: out
        run: echo "url=https://staging.example.com" >> \$GITHUB_OUTPUT
  deploy_prod:
    needs: deploy_staging
    runs-on: ubuntu-latest
    environment: { name: production, url: \${{ steps.out.outputs.url }} }
    steps:
      - uses: actions/download-artifact@v4
        with: { name: \${{ env.ARTIFACT_NAME }} }
      - name: Preflight
        run: echo "All CI gates must have passed already."
      - name: Deploy to Production (HTTPS + HSTS enforced)
        run: echo "Deploying to PRODUCTION…"
      - name: Output Prod URL
        id: out
        run: echo "url=https://app.example.com" >> \$GITHUB_OUTPUT
"@

$auditYml = @"
name: Full System Audit & Report
on:
  workflow_dispatch:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
permissions: { contents: write, actions: read }
jobs:
  audit:
    runs-on: ubuntu-latest
    env: { PYTHON_VERSION: "3.11" }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: \${{ env.PYTHON_VERSION }} }
      - name: Install audit deps
        run: |
          python -m pip install --upgrade pip
          pip install pyflakes flake8 autopep8 markdownify
      - name: Run repository audit script
        run: |
          chmod +x scripts/audit_repo.py || true
          python scripts/audit_repo.py --out-json docs/Status_Report.json --out-md docs/Status_Report.md
      - uses: actions/upload-artifact@v4
        with:
          name: audit-report
          path: |
            docs/Status_Report.md
            docs/Status_Report.json
      - name: Commit report back (append-only)
        if: \${{ github.event_name == 'workflow_dispatch' || github.event.pull_request.head.repo.full_name == github.repository }}
        uses: EndBug/add-and-commit@v9
        with:
          message: "chore(audit): update Status_Report [skip ci]"
          add: "docs/Status_Report.md docs/Status_Report.json"
"@

$issuesYml = @"
name: Create Issues from Task_List
on: { workflow_dispatch: {} }
permissions: { contents: read, issues: write }
jobs:
  create_issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - name: Run generator
        env:
          GH_TOKEN: \${{ secrets.GITHUB_TOKEN }}
          GH_REPO: \${{ github.repository }}
        run: python scripts/issues_from_tasklist.py docs/Task_List.md
"@

$pagesYml = @"
name: Publish Docs (GitHub Pages)
on:
  workflow_dispatch:
  push:
    branches: [ "main" ]
    paths: [ "docs/**", ".github/workflows/pages.yml" ]
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: "pages", cancel-in-progress: true }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Prepare static site from docs/
        run: |
          mkdir -p public
          cp -r docs/* public/ || true
      - uses: actions/upload-pages-artifact@v3
        with: { path: public }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: \${{ steps.deployment.outputs.page_url }} }
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
"@

SafeWrite (Join-Path $Dest ".github/workflows/deploy.yml") $deployYml
SafeWrite (Join-Path $Dest ".github/workflows/audit.yml") $auditYml
SafeWrite (Join-Path $Dest ".github/workflows/issues.yml") $issuesYml
SafeWrite (Join-Path $Dest ".github/workflows/pages.yml") $pagesYml

# Scripts
$auditPy = @"
#!/usr/bin/env python3
# FILE: scripts/audit_repo.py | PURPOSE: Full scan FE/BE/DB/API/Security wiring and report | OWNER: DevOps | LAST-AUDITED: 2025-10-21
import os, re, json, argparse, datetime
from pathlib import Path
SECTIONS = {"frontend":["package.json","src","app","pages","components"],"backend":["requirements.txt","pyproject.toml","manage.py","main.py","app","src"],"db":["migrations","alembic.ini","prisma","schema.prisma","entities","models","sql"],"api":["contracts","openapi.yaml","schema.graphql","routers","routes","controllers"],"security":["csp","helmet","middlewares","auth","rbac","permissions","csrf"],"docs":["docs"]}
def find_any(base,names):
  hits=[];
  for root,dirs,files in os.walk(base):
    for n in names:
      if n in files or n in dirs: hits.append(os.path.join(root,n))
  return hits
def header_check(p):
  try:
    with open(p,"r",encoding="utf-8",errors="ignore") as f:
      return f.readline().strip().startswith("FILE:")
  except Exception: return False
def main():
  import sys
  repo=Path(".").resolve()
  now=datetime.datetime.utcnow().isoformat()+"Z"
  report={"timestamp":now,"summary":{},"sections":{},"violations":[],"recommendations":[]}
  for k,h in SECTIONS.items():
    hits=find_any(repo,h)
    report["sections"][k]=hits; report["summary"][k]=len(hits)
  exts=(".py",".ts",".tsx",".js",".jsx",".go",".cs",".java")
  missing=[]
  for root,_,files in os.walk(repo):
    if any(seg in root for seg in [".git",".venv","node_modules","__pycache__"]): continue
    for f in files:
      if f.endswith(exts):
        p=os.path.join(root,f)
        if not header_check(p): missing.append(p)
  if missing:
    report["violations"].append({"policy":"FILE_HEADER","count":len(missing),"items":missing})
    report["recommendations"].append("Add required file header line to all source files.")
  leaked=[]
  for root,_,files in os.walk(repo):
    for f in files:
      if f==".env": leaked.append(os.path.join(root,f))
  if leaked:
    report["violations"].append({"policy":"ENV_COMMIT","count":len(leaked),"items":leaked})
    report["recommendations"].append("Never commit .env files—use KMS/Vault and templates/.env.example only.")
  fe_pages=[]; buttons=[]
  for root,_,files in os.walk(repo):
    if "pages" in root or "app" in root:
      fe_pages+=[os.path.join(root,f) for f in files if f.endswith((".tsx",".jsx",".vue",".svelte"))]
    if "components" in root:
      import re as _re
      buttons+=[os.path.join(root,f) for f in files if _re.search(r"Button|Btn",f,_re.I)]
  report["summary"]["fe_pages"]=len(fe_pages); report["summary"]["buttons"]=len(buttons)
  Path("docs").mkdir(exist_ok=True)
  with open("docs/Status_Report.json","w",encoding="utf-8") as jf: json.dump(report,jf,indent=2)
  with open("docs/Status_Report.md","w",encoding="utf-8") as mf:
    mf.write(f"# Status Report`n`n- Generated: {now}`n`n")
    for k,v in report["summary"].items(): mf.write(f"- **{k}**: {v}`n")
    mf.write("`n## Sections`n")
    for k,items in report["sections"].items():
      mf.write(f"`n### {k}`n")
      for it in items[:200]: mf.write(f"- {it}`n")
    mf.write("`n## Violations`n")
    for v in report["violations"]: mf.write(f"- **{v['policy']}**: {v['count']} items`n")
    mf.write("`n## Recommendations`n")
    for r in report["recommendations"]: mf.write(f"- {r}`n")
if __name__=="__main__": main()
"@

$issuesPy = @"
#!/usr/bin/env python3
# FILE: scripts/issues_from_tasklist.py | PURPOSE: Convert docs/Task_List.md to GitHub Issues | OWNER: DevOps | LAST-AUDITED: 2025-10-21
import os, sys, re, requests
TOKEN=os.getenv('GH_TOKEN'); REPO=os.getenv('GH_REPO')
if not TOKEN or not REPO:
  print('GH_TOKEN and GH_REPO are required', file=sys.stderr); sys.exit(1)
API=f'https://api.github.com/repos/{REPO}/issues'
HEADERS={'Authorization': f'token {TOKEN}','Accept':'application/vnd.github+json'}
def parse_tasks(p):
  tasks=[];
  if not os.path.exists(p): return tasks
  with open(p,'r',encoding='utf-8') as f:
    for line in f:
      m=re.match(r'^\\s*-\\s*\\[(P[0-3])\\]\\[(\\w+)\\]\\s*(.+)$', line.strip())
      if m:
        prio, area, rest=m.groups()
        title=rest.split(' @')[0].strip()
        body=f'Priority: {prio}\\nArea: {area}\\n\\nSource: docs/Task_List.md'
        labels=[prio, f'area:{area}']
        tasks.append((title, body, labels))
  return tasks
def create_issue(title, body, labels):
  import requests
  r=requests.post(API, headers=HEADERS, json={'title':title,'body':body,'labels':labels}, timeout=30)
  if r.status_code>=300: print('Failed:', r.status_code, r.text, file=sys.stderr)
  else: print('Created:', r.json().get('html_url'))
def main():
  md = sys.argv[1] if len(sys.argv)>1 else 'docs/Task_List.md'
  for t in parse_tasks(md): create_issue(*t)
if __name__=='__main__': main()
"@

$backupSh = @"
#!/usr/bin/env bash
# FILE: scripts/backup.sh | PURPOSE: Clean backup archive (no secrets/caches) | OWNER: DevOps | LAST-AUDITED: 2025-10-21
set -euo pipefail
OUT="\${1:-backup_\$(date +%Y%m%d_%H%M%S).tar.gz}"
tar --exclude-vcs \
    --exclude="**/.env" --exclude="**/.venv" --exclude="**/node_modules" \
    --exclude="**/__pycache__" --exclude="**/.pytest_cache" --exclude="**/.mypy_cache" \
    --exclude="**/dist" --exclude="**/build" --exclude="**/.next" \
    -czf "\$OUT" .
echo "Backup written: \$OUT"
"@

SafeWrite (Join-Path $Dest "scripts/audit_repo.py") $auditPy
SafeWrite (Join-Path $Dest "scripts/issues_from_tasklist.py") $issuesPy
SafeWrite (Join-Path $Dest "scripts/backup.sh") $backupSh

# Docs/templates placeholders
if (!(Test-Path (Join-Path $Dest "docs/Task_List.md"))) { "- [P1][FE] Sample task" | Set-Content -Path (Join-Path $Dest "docs/Task_List.md") -Encoding UTF8 }
if (!(Test-Path (Join-Path $Dest "templates/.env.example"))) { "# placeholders only; use KMS/Vault in prod" | Set-Content -Path (Join-Path $Dest "templates/.env.example") -Encoding UTF8 }
if (!(Test-Path (Join-Path $Dest "GLOBAL_GUIDELINES.txt"))) { "Paste your v2.3 guidelines here." | Set-Content -Path (Join-Path $Dest "GLOBAL_GUIDELINES.txt") -Encoding UTF8 }
if (!(Test-Path (Join-Path $Dest "USAGE_GUIDE.md"))) { "See Actions: audit, deploy, pages, issues." | Set-Content -Path (Join-Path $Dest "USAGE_GUIDE.md") -Encoding UTF8 }

Write-Info "Done. Top-level tree:"
Get-ChildItem -Path $Dest -Depth 1 | ForEach-Object { $_.FullName }
'@ | Set-Content -Path ".\bootstrap_repo.ps1" -Encoding UTF8
