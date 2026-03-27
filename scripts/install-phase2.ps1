# Phase 2 Installer: CLI Tools and Environments
# Usage: .\install-phase2.ps1 -ConfigPath .\backup [-InstallAll]

param(
    [string]$ConfigPath = ".\backup",
    [switch]$InstallAll = $false
)

Write-Host "🛠️ Phase 2: CLI Tools and Environment Restoration" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# Check backup structure
if (-not (Test-Path $ConfigPath)) {
    Write-Host "❌ Backup directory not found: $ConfigPath" -ForegroundColor Red
    exit 1
}

# Check if Phase 2 data exists
$cliToolsFile = Join-Path $ConfigPath "cli-tools\installed-cli.txt"
if (-not (Test-Path $cliToolsFile)) {
    Write-Host "⚠️  Phase 2 data not found. Run collect.ps1 first or use Phase 1 only." -ForegroundColor Yellow
    exit 1
}

Write-Host "📋 Phase 2 backup data found:" -ForegroundColor Green
Write-Host "  CLI Tools: $cliToolsFile" -ForegroundColor Gray

# Show CLI tools from backup
Write-Host ""
Write-Host "🔧 CLI Tools in Backup:" -ForegroundColor Green
Get-Content $cliToolsFile | ForEach-Object {
    Write-Host "  $_" -ForegroundColor Gray
}

# Show environment info
$pythonInfo = Join-Path $ConfigPath "environments\python-info.txt"
$nodejsInfo = Join-Path $ConfigPath "environments\nodejs-info.txt"

if (Test-Path $pythonInfo) {
    Write-Host ""
    Write-Host "🐍 Python Environment:" -ForegroundColor Green
    Get-Content $pythonInfo | Select-Object -First 5 | ForEach-Object {
        Write-Host "  $_" -ForegroundColor Gray
    }
}

if (Test-Path $nodejsInfo) {
    Write-Host ""
    Write-Host "📦 Node.js Environment:" -ForegroundColor Green
    Get-Content $nodejsInfo | Select-Object -First 5 | ForEach-Object {
        Write-Host "  $_" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "📋 Restoration Options:" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

# Platform detection
$platform = "Windows"
if ($PSVersionTable.Platform -eq "Unix") {
    if (Get-Command uname -ErrorAction SilentlyContinue) {
        $uname = uname -s
        if ($uname -eq "Darwin") {
            $platform = "macOS"
        } else {
            $platform = "Linux"
        }
    }
}

Write-Host "Detected Platform: $platform" -ForegroundColor Green

# Manual restoration guide
Write-Host ""
Write-Host "📝 Manual Restoration Guide:" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow

switch ($platform) {
    "Windows" {
        Write-Host "## Windows (PowerShell)" -ForegroundColor Green
        Write-Host ""
        Write-Host "1. Install CLI tools using winget:" -ForegroundColor Gray
        Write-Host "   winget install Git.Git" -ForegroundColor DarkGray
        Write-Host "   winget install OpenJS.NodeJS" -ForegroundColor DarkGray
        Write-Host "   winget install Python.Python.3.13" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "2. Install OpenClaw tools:" -ForegroundColor Gray
        Write-Host "   npm install -g openclaw" -ForegroundColor DarkGray
        Write-Host "   npm install -g clawhub" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "3. Set up Python environment:" -ForegroundColor Gray
        Write-Host "   python -m venv venv" -ForegroundColor DarkGray
        Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor DarkGray
        Write-Host "   pip install -r .\backup\environments\python-requirements.txt" -ForegroundColor DarkGray
    }
    "macOS" {
        Write-Host "## macOS (Homebrew)" -ForegroundColor Green
        Write-Host ""
        Write-Host "1. Install CLI tools using Homebrew:" -ForegroundColor Gray
        Write-Host "   brew install git" -ForegroundColor DarkGray
        Write-Host "   brew install node" -ForegroundColor DarkGray
        Write-Host "   brew install python" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "2. Install OpenClaw tools:" -ForegroundColor Gray
        Write-Host "   npm install -g openclaw" -ForegroundColor DarkGray
        Write-Host "   npm install -g clawhub" -ForegroundColor DarkGray
    }
    "Linux" {
        Write-Host "## Linux (Ubuntu/Debian)" -ForegroundColor Green
        Write-Host ""
        Write-Host "1. Install CLI tools using apt:" -ForegroundColor Gray
        Write-Host "   sudo apt update" -ForegroundColor DarkGray
        Write-Host "   sudo apt install git nodejs npm python3 python3-pip" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "2. Install OpenClaw tools:" -ForegroundColor Gray
        Write-Host "   sudo npm install -g openclaw" -ForegroundColor DarkGray
        Write-Host "   sudo npm install -g clawhub" -ForegroundColor DarkGray
    }
}

# Optional: Check existing installations
Write-Host ""
Write-Host "🔍 Check Current Installations:" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan

$toolsToCheck = @("git", "node", "npm", "python", "openclaw", "clawhub")
foreach ($tool in $toolsToCheck) {
    try {
        $version = "Unknown"
        if ($tool -eq "openclaw") {
            $result = openclaw --version 2>&1
            if ($LASTEXITCODE -eq 0) { $version = $result }
        } elseif ($tool -eq "clawhub") {
            $result = clawhub -V 2>&1
            if ($LASTEXITCODE -eq 0) { $version = $result }
        } elseif ($tool -eq "git") {
            $version = git --version 2>&1
        } elseif ($tool -eq "node") {
            $version = node --version 2>&1
        } elseif ($tool -eq "npm") {
            $version = npm --version 2>&1
        } elseif ($tool -eq "python") {
            $version = python --version 2>&1
        }
        
        if ($version -match "not found|command not found|is not recognized") {
            Write-Host "  ❌ $tool: Not installed" -ForegroundColor Red
        } else {
            Write-Host "  ✅ $tool: $version" -ForegroundColor Green
        }
    } catch {
        Write-Host "  ❌ $tool: Check failed" -ForegroundColor Red
    }
}

# Summary
Write-Host ""
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "===========" -ForegroundColor Cyan
Write-Host "✅ Phase 2 installation is mostly manual due to:" -ForegroundColor Gray
Write-Host "   - Platform-specific package managers" -ForegroundColor Gray
Write-Host "   - Permission requirements" -ForegroundColor Gray
Write-Host "   - Version management complexities" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Detailed instructions in: scripts\INSTALL-GUIDE-PHASE2.md" -ForegroundColor Gray
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "1. Follow the platform-specific guide above" -ForegroundColor Gray
Write-Host "2. Verify tool installations with the check above" -ForegroundColor Gray
Write-Host "3. Run collect.ps1 again to capture new environment" -ForegroundColor Gray
Write-Host "4. Update README.md with any custom installation notes" -ForegroundColor Gray