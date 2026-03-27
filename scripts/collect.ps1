# AI Agent Configuration Collector
# Phase 1: Core OpenClaw configuration backup
# Usage: .\collect.ps1 -OutputPath .\backup

param(
    [string]$OutputPath = ".\backup",
    [switch]$Phase1Only = $false
)

Write-Host "🔍 Starting AI Agent configuration collection..." -ForegroundColor Cyan
Write-Host "📊 Mode: $(if ($Phase1Only) {'Phase 1 Only'} else {'All Phases'})" -ForegroundColor Cyan

# Create directory structure
$configPath = Join-Path $OutputPath "configs\openclaw"
$skillsPath = Join-Path $OutputPath "skills"
$envPath = Join-Path $OutputPath "environment"
$cliToolsPath = Join-Path $OutputPath "cli-tools"
$environmentsPath = Join-Path $OutputPath "environments"

New-Item -ItemType Directory -Path $configPath -Force | Out-Null
New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
New-Item -ItemType Directory -Path $envPath -Force | Out-Null

if (-not $Phase1Only) {
    New-Item -ItemType Directory -Path $cliToolsPath -Force | Out-Null
    New-Item -ItemType Directory -Path $environmentsPath -Force | Out-Null
}

# 1. Backup OpenClaw configuration
Write-Host "📋 Backing up OpenClaw configuration..." -ForegroundColor Green
$openclawConfigDir = "$env:USERPROFILE\.openclaw"
if (Test-Path $openclawConfigDir) {
    Get-ChildItem "$openclawConfigDir\*.json" | ForEach-Object {
        Copy-Item $_.FullName -Destination $configPath -Force
        Write-Host "  Copied: $($_.Name)" -ForegroundColor Gray
    }
} else {
    Write-Host "  Warning: OpenClaw config directory not found" -ForegroundColor Yellow
}

# 2. List built-in skills
Write-Host "📚 Listing built-in skills..." -ForegroundColor Green
$builtinSkillsDir = "$env:APPDATA\npm\node_modules\openclaw\skills"
if (Test-Path $builtinSkillsDir) {
    Get-ChildItem $builtinSkillsDir -Directory | Select-Object -ExpandProperty Name | 
        Out-File (Join-Path $skillsPath "builtin-skills.txt") -Encoding UTF8
    Write-Host "  Found $(Get-Content (Join-Path $skillsPath 'builtin-skills.txt') | Measure-Object | Select-Object -ExpandProperty Count) built-in skills" -ForegroundColor Gray
} else {
    Write-Host "  Warning: Built-in skills directory not found" -ForegroundColor Yellow
}

# 3. List ClawHub installed skills
Write-Host "📦 Checking ClawHub installed skills..." -ForegroundColor Green
try {
    $clawhubList = clawhub list 2>$null
    if ($clawhubList -and $clawhubList -notmatch "No installed skills") {
        $clawhubList | Out-File (Join-Path $skillsPath "clawhub-skills.txt") -Encoding UTF8
        Write-Host "  Found ClawHub skills" -ForegroundColor Gray
    } else {
        "No skills installed via ClawHub" | Out-File (Join-Path $skillsPath "clawhub-skills.txt") -Encoding UTF8
        Write-Host "  No ClawHub skills installed" -ForegroundColor Gray
    }
} catch {
    "ClawHub CLI not available or error occurred" | Out-File (Join-Path $skillsPath "clawhub-skills.txt") -Encoding UTF8
    Write-Host "  ClawHub CLI not available" -ForegroundColor Yellow
}

# 4. List custom skills from workspace
Write-Host "🔧 Checking custom skills..." -ForegroundColor Green
$customSkillsDir = "$env:USERPROFILE\.openclaw\workspace\skills"
if (Test-Path $customSkillsDir) {
    $customSkills = Get-ChildItem $customSkillsDir -Directory -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name
    if ($customSkills) {
        $customSkills | Out-File (Join-Path $skillsPath "custom-skills.txt") -Encoding UTF8
        Write-Host "  Found $($customSkills.Count) custom skills" -ForegroundColor Gray
    } else {
        "No custom skills" | Out-File (Join-Path $skillsPath "custom-skills.txt") -Encoding UTF8
        Write-Host "  No custom skills found" -ForegroundColor Gray
    }
} else {
    "Custom skills directory does not exist" | Out-File (Join-Path $skillsPath "custom-skills.txt") -Encoding UTF8
    Write-Host "  Custom skills directory not found" -ForegroundColor Gray
}

# 5. Collect system environment information
Write-Host "💻 Collecting system environment information..." -ForegroundColor Green
@"
# AI Agent Environment Configuration
# Collected on: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## System Information
OS: $([System.Environment]::OSVersion.VersionString)
PowerShell Version: $($PSVersionTable.PSVersion)
PowerShell Edition: $($PSVersionTable.PSEdition)

## Tool Versions
Python: $(python --version 2>&1)
Node.js: $(node --version 2>&1)
npm: $(npm --version 2>&1)
Git: $(git --version 2>&1)
OpenClaw: $(openclaw --version 2>&1)
ClawHub: $(clawhub -V 2>&1)

## Environment Variables
User Profile: $env:USERPROFILE
OpenClaw Workspace: $env:USERPROFILE\.openclaw\workspace
OpenClaw Config: $env:USERPROFILE\.openclaw

## Important Paths (first 5 entries)
PATH:
$($env:PATH -split ';' | Select-Object -First 5 | ForEach-Object { "  $_" })
"@ | Out-File (Join-Path $envPath "system-info.txt") -Encoding UTF8

# Phase 2: CLI Tools and Environment Configuration
if (-not $Phase1Only) {
    # 6. Collect CLI tools information
    Write-Host "🔧 Collecting CLI tools information..." -ForegroundColor Green
    $cliTools = @()
    
    # Check for common CLI tools
    $toolsToCheck = @(
        @{Name="git"; Command="git --version"},
        @{Name="node"; Command="node --version"},
        @{Name="npm"; Command="npm --version"},
        @{Name="python"; Command="python --version"},
        @{Name="pip"; Command="pip --version"},
        @{Name="openclaw"; Command="openclaw --version"},
        @{Name="clawhub"; Command="clawhub -V"},
        @{Name="powershell"; Command="$PSVersionTable.PSVersion.ToString()"},
        @{Name="code"; Command="code --version"},
        @{Name="gh"; Command="gh --version"}
    )
    
    foreach ($tool in $toolsToCheck) {
        try {
            $version = "Not found"
            if ($tool.Name -eq "powershell") {
                $version = Invoke-Expression $tool.Command
            } else {
                $result = Invoke-Expression $tool.Command 2>&1
                if ($LASTEXITCODE -eq 0 -or $? -eq $true) {
                    $version = ($result | Select-Object -First 1).ToString().Trim()
                }
            }
            $cliTools += @{Name=$tool.Name; Version=$version; Command=$tool.Command}
            Write-Host "  $($tool.Name): $version" -ForegroundColor Gray
        } catch {
            $cliTools += @{Name=$tool.Name; Version="Error checking"; Command=$tool.Command}
            Write-Host "  $($tool.Name): Error checking" -ForegroundColor Yellow
        }
    }
    
    # Save CLI tools list
    $cliTools | ForEach-Object {
        "$($_.Name): $($_.Version)" | Out-File (Join-Path $cliToolsPath "installed-cli.txt") -Encoding UTF8 -Append
    }
    
    # 7. Collect Python environment information
    Write-Host "🐍 Collecting Python environment information..." -ForegroundColor Green
    try {
        # Check for Python virtual environments
        $pythonInfo = @"
# Python Environment Information
# Collected on: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## Python Version
$(python --version 2>&1)

## PIP Version
$(pip --version 2>&1)

## Installed Packages (global)
$(pip list --format=freeze 2>&1)
"@
        $pythonInfo | Out-File (Join-Path $environmentsPath "python-info.txt") -Encoding UTF8
        Write-Host "  Python environment information saved" -ForegroundColor Gray
        
        # Try to export requirements if pip freeze works
        $requirements = pip freeze 2>&1
        if ($LASTEXITCODE -eq 0) {
            $requirements | Out-File (Join-Path $environmentsPath "python-requirements.txt") -Encoding UTF8
            Write-Host "  Python requirements saved" -ForegroundColor Gray
        }
    } catch {
        Write-Host "  Failed to collect Python environment information" -ForegroundColor Yellow
    }
    
    # 8. Collect Node.js environment information
    Write-Host "📦 Collecting Node.js environment information..." -ForegroundColor Green
    try {
        $nodeInfo = @"
# Node.js Environment Information
# Collected on: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## Node.js Version
$(node --version 2>&1)

## npm Version
$(npm --version 2>&1)

## Global Packages
$(npm list -g --depth=0 2>&1 | Select-Object -First 50)
"@
        $nodeInfo | Out-File (Join-Path $environmentsPath "nodejs-info.txt") -Encoding UTF8
        Write-Host "  Node.js environment information saved" -ForegroundColor Gray
    } catch {
        Write-Host "  Failed to collect Node.js environment information" -ForegroundColor Yellow
    }
}

Write-Host "✅ Collection complete!" -ForegroundColor Cyan
Write-Host "📁 Output saved to: $OutputPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review the collected configuration" -ForegroundColor Gray
Write-Host "2. Check for sensitive information (API keys, tokens)" -ForegroundColor Gray
Write-Host "3. Commit to version control" -ForegroundColor Gray