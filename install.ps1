param(
  [switch]$Claude,
  [switch]$Codex,
  [switch]$Local,
  [switch]$Uninstall,
  [switch]$Help
)

$ErrorActionPreference = "Stop"
$PluginName = "security-coverage"
$Commands = @("security-assess", "security-plan", "security-implement")
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Show-Usage {
  Write-Host @"
security-coverage installer

Usage:
  .\install.ps1 [options]

Options:
  -Claude       install Claude commands and skill only
  -Codex        install Codex commands, skill, and plugin files only
  -Local        install into the current project (.\.claude and/or .\.codex)
  -Uninstall    remove installed files
  -Help         show this help

Default:
  .\install.ps1 installs globally for both Claude and Codex.
"@
}

if ($Help) {
  Show-Usage
  exit 0
}

if (-not $Claude -and -not $Codex) {
  $Claude = $true
  $Codex = $true
}

function Copy-DirReplace {
  param([string]$Source, [string]$Destination)
  if (Test-Path $Destination) {
    Remove-Item $Destination -Recurse -Force
  }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
  Copy-Item $Source $Destination -Recurse -Force
}

function Copy-PluginReplace {
  param([string]$Destination)
  if (Test-Path $Destination) {
    Remove-Item $Destination -Recurse -Force
  }
  New-Item -ItemType Directory -Force -Path $Destination | Out-Null
  New-Item -ItemType Directory -Force -Path "$Destination\.codex-plugin", "$Destination\commands", "$Destination\skills" | Out-Null
  Copy-Item "$RootDir\.codex-plugin\plugin.json" "$Destination\.codex-plugin\plugin.json" -Force
  Copy-Item "$RootDir\SKILL.md", "$RootDir\README.md", "$RootDir\LICENSE", "$RootDir\.gitignore", "$RootDir\.gitattributes", "$RootDir\install.sh", "$RootDir\install.ps1", "$RootDir\package.json" $Destination -Force
  Copy-Item "$RootDir\commands\*" "$Destination\commands\" -Recurse -Force
  Copy-Item "$RootDir\skills\*" "$Destination\skills\" -Recurse -Force
}

function Install-Commands {
  param([string]$Target)
  New-Item -ItemType Directory -Force -Path $Target | Out-Null
  foreach ($Command in $Commands) {
    Copy-Item "$RootDir\commands\$Command.md" "$Target\$Command.md" -Force
  }
}

function Assert-File {
  param([string]$Path)
  if (-not (Test-Path $Path -PathType Leaf)) {
    throw "Missing expected file: $Path"
  }
}

function Assert-Dir {
  param([string]$Path)
  if (-not (Test-Path $Path -PathType Container)) {
    throw "Missing expected directory: $Path"
  }
}

function Install-Claude {
  if ($Local) {
    $Base = Join-Path (Get-Location) ".claude"
  } else {
    $Base = Join-Path $HOME ".claude"
  }

  if ($Uninstall) {
    Remove-Item "$Base\skills\$PluginName" -Recurse -Force -ErrorAction SilentlyContinue
    foreach ($Command in $Commands) {
      Remove-Item "$Base\commands\$Command.md" -Force -ErrorAction SilentlyContinue
    }
    Write-Host "Removed Claude install from $Base"
    return
  }

  Copy-DirReplace "$RootDir\skills\$PluginName" "$Base\skills\$PluginName"
  Install-Commands "$Base\commands"
  Assert-Dir "$Base\skills\$PluginName"
  Assert-File "$Base\skills\$PluginName\SKILL.md"
  foreach ($Command in $Commands) {
    Assert-File "$Base\commands\$Command.md"
  }
  Write-Host "Installed Claude files to $Base"
}

function Install-Codex {
  if ($Local) {
    $Base = Join-Path (Get-Location) ".codex"
  } elseif ($env:CODEX_HOME) {
    $Base = $env:CODEX_HOME
  } else {
    $Base = Join-Path $HOME ".codex"
  }

  if ($Uninstall) {
    Remove-Item "$Base\skills\$PluginName", "$Base\plugins\$PluginName" -Recurse -Force -ErrorAction SilentlyContinue
    foreach ($Command in $Commands) {
      Remove-Item "$Base\commands\$Command.md" -Force -ErrorAction SilentlyContinue
    }
    Write-Host "Removed Codex install from $Base"
    return
  }

  Copy-DirReplace "$RootDir\skills\$PluginName" "$Base\skills\$PluginName"
  Copy-PluginReplace "$Base\plugins\$PluginName"
  Install-Commands "$Base\commands"
  Assert-Dir "$Base\skills\$PluginName"
  Assert-File "$Base\skills\$PluginName\SKILL.md"
  Assert-File "$Base\plugins\$PluginName\.codex-plugin\plugin.json"
  foreach ($Command in $Commands) {
    Assert-File "$Base\commands\$Command.md"
  }
  Write-Host "Installed Codex files to $Base"
}

if ($Claude) {
  Install-Claude
}

if ($Codex) {
  Install-Codex
}

if ($Uninstall) {
  Write-Host "Uninstall complete."
} else {
  Write-Host "Install complete."
}
