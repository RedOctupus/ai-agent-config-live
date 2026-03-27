# Phase 2 Installation Guide
# CLI Tools and Environment Setup

This guide explains how to restore the CLI tools and development environments captured in Phase 2.

## Overview

Phase 2 extends the basic OpenClaw configuration backup with:

1. **CLI Tools Inventory** - List of installed command-line tools
2. **Python Environment** - Python packages and virtual environment
3. **Node.js Environment** - Node.js packages and npm configuration

## Restoration Process

### Step 1: Review Collected Information

Check the backup directory for Phase 2 files:

```
backup/
├── cli-tools/
│   └── installed-cli.txt      # List of CLI tools with versions
├── environments/
│   ├── python-info.txt       # Python environment details
│   ├── python-requirements.txt # Python package list
│   └── nodejs-info.txt       # Node.js environment details
```

### Step 2: Install CLI Tools

#### Windows (PowerShell)

```powershell
# Review what tools were installed
Get-Content .\backup\cli-tools\installed-cli.txt

# Install missing tools using winget (Windows Package Manager)
winget install Git.Git
winget install OpenJS.NodeJS
winget install Python.Python.3.13

# Install OpenClaw
npm install -g openclaw

# Install ClawHub
npm install -g clawhub
```

#### macOS (Homebrew)

```bash
# Review tools
cat backup/cli-tools/installed-cli.txt

# Install tools
brew install git
brew install node
brew install python

# Install OpenClaw
npm install -g openclaw

# Install ClawHub
npm install -g clawhub
```

#### Linux (Ubuntu/Debian)

```bash
# Review tools
cat backup/cli-tools/installed-cli.txt

# Install tools
sudo apt update
sudo apt install git nodejs npm python3 python3-pip

# Install OpenClaw
sudo npm install -g openclaw

# Install ClawHub
sudo npm install -g clawhub
```

### Step 3: Set Up Python Environment

```powershell
# Check Python version from backup
Get-Content .\backup\environments\python-info.txt | Select-Object -First 5

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install packages from requirements
pip install -r .\backup\environments\python-requirements.txt
```

### Step 4: Set Up Node.js Environment

```powershell
# Check Node.js version from backup
Get-Content .\backup\environments\nodejs-info.txt | Select-Object -First 5

# Initialize npm project (if needed)
npm init -y

# Install global packages from backup
# Note: Review nodejs-info.txt for specific packages
npm install -g typescript
npm install -g nodemon
npm install -g eslint
```

## Platform-Specific Notes

### Windows
- Use PowerShell for scripting
- Paths use backslashes (`\`)
- Environment variables accessed via `$env:VARIABLE`
- Administrator may be required for some installations

### macOS
- Use Terminal with bash/zsh
- Homebrew is the recommended package manager
- Paths use forward slashes (`/`)
- May need to configure PATH for newly installed tools

### Linux
- Package manager varies (apt, yum, dnf, pacman)
- May need to configure repository sources
- Some tools require compilation from source

## Troubleshooting

### Common Issues

1. **Permission Errors**
   - Windows: Run PowerShell as Administrator
   - macOS/Linux: Use `sudo` for system-wide installations

2. **Version Mismatches**
   - Tools may have newer versions available
   - Consider using version managers:
     - Python: `pyenv`
     - Node.js: `nvm`
     - Ruby: `rbenv`

3. **Missing Dependencies**
   - Some CLI tools require additional system libraries
   - Check tool documentation for prerequisites

4. **Path Configuration**
   - Newly installed tools may not be in PATH
   - Restart terminal or source shell configuration

### Verification

After installation, verify tools are working:

```powershell
# Check tool versions
git --version
node --version
npm --version
python --version
pip --version
openclaw --version
clawhub -V
```

## Automated Installation (Advanced)

For automated installation, modify the `install.ps1` script to include Phase 2 functionality:

```powershell
# Add to install.ps1 after OpenClaw configuration restoration

# Phase 2: CLI Tools Installation
Write-Host "🔧 Installing CLI tools from backup..." -ForegroundColor Green
$cliToolsFile = Join-Path $ConfigPath "cli-tools\installed-cli.txt"
if (Test-Path $cliToolsFile) {
    $tools = Get-Content $cliToolsFile
    # Parse and install tools based on platform
    # This would require platform-specific logic
}
```

## Next Steps

After completing Phase 2 restoration:

1. **Test the environment**: Run basic commands for each tool
2. **Configure IDE/editor**: Set up with the restored environment
3. **Update configurations**: Adjust paths and settings for new machine
4. **Create new backup**: Run collection script to capture updated state

## Security Notes

- Review installed packages for security updates
- Use virtual environments to isolate project dependencies
- Consider using Docker for reproducible environments
- Regularly update tools to patch vulnerabilities