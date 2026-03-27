# CLI Tools Configuration

This directory contains configuration for CLI tools used in the AI Agent development environment.

## Structure

```
cli-tools/
├── installed-cli.txt          # List of installed CLI tools (generated)
├── install-scripts/          # Installation scripts for each tool
├── tool-versions.txt        # Version information for tools
└── platform-specific/       # Platform-specific configurations
    ├── windows/
    ├── macos/
    └── linux/
```

## Tools to Track

### Core AI Tools
- OpenClaw CLI (`openclaw`)
- ClawHub CLI (`clawhub`)
- Claude Code CLI (if available)
- Codex CLI (if available)

### Development Tools
- Git (`git`)
- Node.js (`node`, `npm`)
- Python (`python`, `pip`)
- PowerShell Core (`pwsh`)

### Package Managers
- npm (Node.js)
- pip (Python)
- brew (macOS)
- winget/choco (Windows)

## Collection Process

The `collect.ps1` script will:
1. Scan for installed CLI tools
2. Record version information
3. Generate installation scripts where possible
4. Create platform-specific configurations

## Installation Process

The `install.ps1` script will:
1. Check for required tools
2. Install missing tools using platform-specific methods
3. Configure tool settings
4. Verify installations

## Platform Support

### Windows
- PowerShell scripts
- winget/chocolatey package managers
- Manual download/installation fallbacks

### macOS
- Shell scripts
- Homebrew package manager
- Manual installation fallbacks

### Linux
- Shell scripts
- apt/yum/dnf package managers
- Manual installation fallbacks