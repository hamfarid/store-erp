# Runs the MCP sequentialthinking Docker image.
# Usage (PowerShell):
#   ./scripts/mcp_run_sequentialthinking.ps1
#   ./scripts/mcp_run_sequentialthinking.ps1 -- -v  # extra docker args after --

[CmdletBinding()]
Param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$DockerArgs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  throw "Required command not found on PATH: docker"
}

$base = @('run', '--rm', '-i', 'mcp/sequentialthinking')
if ($DockerArgs -and $DockerArgs.Count -gt 0) {
  docker @base @DockerArgs
} else {
  docker @base
}

