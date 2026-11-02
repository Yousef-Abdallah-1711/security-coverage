param(
  [switch]$Claude,
  [switch]$Codex,
  [switch]$Local,
  [switch]$Uninstall,
  [switch]$Help
)

$ErrorActionPreference = 'Stop'
$Python = Get-Command python -ErrorAction SilentlyContinue
$PythonArgs = @()
if ($Python) {
  & $Python.Source -c 'import sys; raise SystemExit(sys.version_info < (3, 8))' *> $null
  if ($LASTEXITCODE -ne 0) { $Python = $null }
}
if (-not $Python) {
  $Python = Get-Command py -ErrorAction SilentlyContinue
  $PythonArgs = @('-3')
  if ($Python) {
    & $Python.Source -3 -c 'import sys; raise SystemExit(sys.version_info < (3, 8))' *> $null
    if ($LASTEXITCODE -ne 0) { $Python = $null }
  }
}
if (-not $Python) { throw 'Security Coverage installer requires Python 3.8 or newer.' }
$Installer = Join-Path $PSScriptRoot 'scripts/install.py'
$Arguments = @($PythonArgs + $Installer)
if ($Claude) { $Arguments += '--claude' }
if ($Codex) { $Arguments += '--codex' }
if ($Local) { $Arguments += '--local' }
if ($Uninstall) { $Arguments += '--uninstall' }
if ($Help) { $Arguments += '--help' }
& $Python.Source @Arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
