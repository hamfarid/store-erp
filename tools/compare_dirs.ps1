Param(
  [string]$Upper = 'Store',
  [string]$Lower = 'store'
)
$ErrorActionPreference = 'Stop'
if (!(Test-Path $Upper)) { Write-Output 'NO_Store_DIR'; exit 0 }
if (!(Test-Path $Lower)) { Write-Output 'NO_store_DIR'; exit 0 }
$A = (Get-Item $Upper).FullName
$B = (Get-Item $Lower).FullName
function RelPath([string]$root, [string]$full) { return $full.Substring($root.Length).TrimStart('\') }
$filesA = Get-ChildItem -Path $A -File -Recurse
$filesB = Get-ChildItem -Path $B -File -Recurse
$mapA = @{}
foreach ($f in $filesA) {
  $rel = RelPath $A $f.FullName
  $mapA[$rel.ToLower()] = @{ Path = $f.FullName; Hash = (Get-FileHash -Algorithm SHA256 -Path $f.FullName).Hash }
}
$onlyInB = New-Object System.Collections.ArrayList
$diffs = New-Object System.Collections.ArrayList
foreach ($f in $filesB) {
  $rel = RelPath $B $f.FullName
  $key = $rel.ToLower()
  if (-not $mapA.ContainsKey($key)) {
    [void]$onlyInB.Add($rel)
  } else {
    $hashB = (Get-FileHash -Algorithm SHA256 -Path $f.FullName).Hash
    if ($hashB -ne $mapA[$key].Hash) { [void]$diffs.Add($rel) }
  }
}
$mapB = @{}
foreach ($f in $filesB) { $rel = RelPath $B $f.FullName; $mapB[$rel.ToLower()] = 1 }
$onlyInA = New-Object System.Collections.ArrayList
foreach ($f in $filesA) {
  $rel = RelPath $A $f.FullName
  if (-not $mapB.ContainsKey($rel.ToLower())) { [void]$onlyInA.Add($rel) }
}
$result = [PSCustomObject]@{ OnlyInLower = $onlyInB; OnlyInUpper = $onlyInA; ContentDiffs = $diffs }
$result | ConvertTo-Json -Depth 4

