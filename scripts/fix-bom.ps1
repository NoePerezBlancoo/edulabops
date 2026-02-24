Param(
  [string[]]$Extensions = @("conf","yml","yaml","env","ini","cfg","txt")
)

$files = git ls-files | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }

foreach ($f in $files) {
  $ext = ([System.IO.Path]::GetExtension($f) -replace "^\.","").ToLower()
  if ($Extensions -notcontains $ext) { continue }

  $p = Join-Path (Get-Location) $f
  if (-not (Test-Path $p)) { continue }

  $b = [System.IO.File]::ReadAllBytes($p)
  if ($b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF) {
    [System.IO.File]::WriteAllBytes($p, $b[3..($b.Length-1)])
    Write-Host "Removed BOM: $f"
  }
}