# AI Agent Configuration Installer
# Phase 1: Core OpenClaw configuration restoration
# Usage: .\install.ps1 -ConfigPath .\backup

param(
    [string]$ConfigPath = ".\backup"
)

Write-Host "🚀 Starting AI Agent configuration restoration..." -ForegroundColor Cyan
Write-Host "⚠️  Warning: This script will modify your OpenClaw configuration." -ForegroundColor Yellow
Write-Host "   Make sure to backup your existing configuration first." -ForegroundColor Yellow
Write-Host ""

# Check if config directory exists
if (-not (Test-Path $ConfigPath)) {
    Write-Host "❌ Configuration directory not found: $ConfigPath" -ForegroundColor Red
    Write-Host "   Please provide the correct path to your backup configuration." -ForegroundColor Gray
    exit 1
}

# 1. Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Green

$prereqCheck = @{
    "OpenClaw" = { openclaw --version 2>&1 | Out-Null; $? }
    "Node.js" = { node --version 2>&1 | Out-Null; $? }
    "npm" = { npm --version 2>&1 | Out-Null; $? }
    "Git" = { git --version 2>&1 | Out-Null; $? }
    "Python" = { python --version 2>&1 | Out-Null; $? }
}

$missingPrereqs = @()
foreach ($tool in $prereqCheck.Keys) {
    if (& $prereqCheck[$tool]) {
        Write-Host "  ✅ $tool installed" -ForegroundColor Gray
    } else {
        Write-Host "  ❌ $tool not found" -ForegroundColor Red
        $missingPrereqs += $tool
    }
}

if ($missingPrereqs.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Missing prerequisites:" -ForegroundColor Yellow
    foreach ($tool in $missingPrereqs) {
        Write-Host "   - $tool" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "Please install missing tools before proceeding." -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        Write-Host "Installation aborted." -ForegroundColor Red
        exit 1
    }
}

# 2. Backup existing OpenClaw configuration
Write-Host ""
Write-Host "💾 Backing up existing OpenClaw configuration..." -ForegroundColor Green
$openclawBackupDir = "$env:TEMP\openclaw-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$openclawConfigDir = "$env:USERPROFILE\.openclaw"

if (Test-Path $openclawConfigDir) {
    New-Item -ItemType Directory -Path $openclawBackupDir -Force | Out-Null
    Get-ChildItem "$openclawConfigDir\*.json" | ForEach-Object {
        Copy-Item $_.FullName -Destination $openclawBackupDir -Force
    }
    Write-Host "  Existing configuration backed up to: $openclawBackupDir" -ForegroundColor Gray
} else {
    Write-Host "  No existing OpenClaw configuration found" -ForegroundColor Gray
}

# 3. Restore OpenClaw configuration
Write-Host ""
Write-Host "🔄 Restoring OpenClaw configuration..." -ForegroundColor Green
$sourceConfigDir = Join-Path $ConfigPath "configs\openclaw"
if (Test-Path $sourceConfigDir) {
    $configFiles = Get-ChildItem $sourceConfigDir -Filter "*.json"
    if ($configFiles.Count -gt 0) {
        # Create OpenClaw config directory if it doesn't exist
        New-Item -ItemType Directory -Path $openclawConfigDir -Force | Out-Null
        
        foreach ($file in $configFiles) {
            Copy-Item $file.FullName -Destination $openclawConfigDir -Force
            Write-Host "  Restored: $($file.Name)" -ForegroundColor Gray
        }
        
        Write-Host "  ✅ OpenClaw configuration restored" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  No configuration files found in backup" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠️  Configuration directory not found in backup" -ForegroundColor Yellow
}

# 4. Show skill information
Write-Host ""
Write-Host "📚 Skill information from backup:" -ForegroundColor Green
$skillsDir = Join-Path $ConfigPath "skills"
if (Test-Path $skillsDir) {
    $builtinSkills = Join-Path $skillsDir "builtin-skills.txt"
    $clawhubSkills = Join-Path $skillsDir "clawhub-skills.txt"
    $customSkills = Join-Path $skillsDir "custom-skills.txt"
    
    if (Test-Path $builtinSkills) {
        $count = (Get-Content $builtinSkills | Measure-Object).Count
        Write-Host "  Built-in skills: $count skills listed" -ForegroundColor Gray
    }
    
    if (Test-Path $clawhubSkills) {
        $content = Get-Content $clawhubSkills -Raw
        Write-Host "  ClawHub skills: $content" -ForegroundColor Gray
    }
    
    if (Test-Path $customSkills) {
        $content = Get-Content $customSkills -Raw
        Write-Host "  Custom skills: $content" -ForegroundColor Gray
    }
}

# 5. Show system environment information
Write-Host ""
Write-Host "💻 Original system environment:" -ForegroundColor Green
$envInfoFile = Join-Path $ConfigPath "environment\system-info.txt"
if (Test-Path $envInfoFile) {
    Get-Content $envInfoFile | Select-Object -First 20 | ForEach-Object {
        Write-Host "  $_" -ForegroundColor Gray
    }
}

# 6. Next steps
Write-Host ""
Write-Host "✅ Restoration complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Review the restored configuration at: $openclawConfigDir" -ForegroundColor Gray
Write-Host "2. Check API keys and sensitive information in openclaw.json" -ForegroundColor Gray
Write-Host "3. Update any environment-specific paths or settings" -ForegroundColor Gray
Write-Host "4. Test OpenClaw functionality:" -ForegroundColor Gray
Write-Host "   - Run: openclaw status" -ForegroundColor Gray
Write-Host "   - Run: openclaw config" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  Important notes:" -ForegroundColor Red
Write-Host "   - API keys and tokens from the backup may need to be regenerated" -ForegroundColor Gray
Write-Host "   - File paths may differ between machines" -ForegroundColor Gray
Write-Host "   - Review the system-info.txt for original environment details" -ForegroundColor Gray
Write-Host ""
Write-Host "Backup of original configuration saved to: $openclawBackupDir" -ForegroundColor Gray