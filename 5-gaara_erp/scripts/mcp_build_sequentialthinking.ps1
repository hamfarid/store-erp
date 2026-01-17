# Builds the MCP sequentialthinking Docker image using the official MCP servers repo.
# Defaults to cloning into D:\APPS_AI\servers and checking out tag 2025.4.6.
# Usage (PowerShell):
#   ./scripts/mcp_build_sequentialthinking.ps1
#   ./scripts/mcp_build_sequentialthinking.ps1 -BaseDir "D:\APPS_AI" -RepoName "servers" -Tag "2025.4.6"

[CmdletBinding()]
Param(
  [string]$BaseDir = 'D:\APPS_AI',
  [string]$RepoName = 'servers',
  [string]$Tag = '2025.4.6'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Require-Cmd($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "Required command not found on PATH: $name"
  }
}

Require-Cmd git
Require-Cmd docker

$RepoDir = Join-Path $BaseDir $RepoName
$RepoUrl = 'https://github.com/modelcontextprotocol/servers.git'

Write-Host "[INFO] BaseDir      = $BaseDir"
Write-Host "[INFO] RepoName     = $RepoName"
Write-Host "[INFO] Tag          = $Tag"
Write-Host "[INFO] Target Repo  = $RepoDir"

if (-not (Test-Path -LiteralPath $BaseDir)) {
  Write-Host "[INFO] Creating base directory: $BaseDir"
  New-Item -ItemType Directory -Path $BaseDir | Out-Null
}

if (-not (Test-Path -LiteralPath $RepoDir)) {
  Write-Host "[INFO] Cloning MCP servers repo..."
  git clone $RepoUrl $RepoDir
} else {
  Write-Host "[INFO] Repo already exists. Pulling latest tags..."
}

Push-Location $RepoDir
try {
  git fetch --all --tags
  Write-Host "[INFO] Checking out tag $Tag"
  git checkout $Tag

  Write-Host "[INFO] Building Docker image mcp/sequentialthinking"
  docker build -t mcp/sequentialthinking -f src/sequentialthinking/Dockerfile .

  Write-Host "[SUCCESS] Built Docker image: mcp/sequentialthinking"
} finally {
  Pop-Location
}

