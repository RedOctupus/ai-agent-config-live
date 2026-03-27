# AI Agent Configuration Backup

This repository contains backup and restoration scripts for AI Agent development environments, focusing on OpenClaw configuration.

## 📁 Repository Structure

```
ai-agent-config-live/
├── scripts/
│   ├── collect.ps1              # Phase 1-2 collection script
│   ├── install.ps1              # Phase 1 restoration script
│   ├── install-phase2.ps1       # Phase 2 restoration guidance
│   ├── clean-sensitive.ps1      # Sensitive data cleaner
│   ├── setup-github.ps1         # GitHub repository automation
│   ├── create-stable-release.ps1 # Stable version publisher
│   ├── test-phase2.ps1          # Phase 2 validation
│   └── INSTALL-GUIDE-PHASE2.md  # Phase 2 detailed guide
├── configs/
│   └── openclaw/                # OpenClaw configuration files
├── skills/                      # Skill inventories
├── cli-tools/                   # CLI tool information
├── environment/                 # System environment info
├── environments/                # Python/Node.js environments
├── .github/workflows/
│   └── auto-backup.yml          # Daily backup automation
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Collect Configuration (on source machine)

```powershell
# Run from the repository root
.\scripts\collect.ps1 -OutputPath .\backup
```

This will create a `backup` directory with:
- OpenClaw configuration files (`openclaw.json`, etc.)
- Skill inventory lists
- System environment information

### 2. Restore Configuration (on target machine)

```powershell
# First, clone this repository
git clone <repository-url>
cd ai-agent-config-live

# Phase 1: Restore core configuration
.\scripts\install.ps1 -ConfigPath .\backup

# Phase 2: CLI tools and environments
.\scripts\install-phase2.ps1 -ConfigPath .\backup
```

**Important:** The installation scripts will:
- Backup your existing OpenClaw configuration
- Restore configuration files from the backup
- Show what skills were installed
- Provide platform-specific CLI tool installation guides
- Guide you through environment setup

## 🔧 Prerequisites

Before restoring configuration, ensure you have:

- [OpenClaw](https://openclaw.ai/) installed
- [Node.js](https://nodejs.org/) and npm
- [Python](https://python.org/) (for some skills)
- [Git](https://git-scm.com/)
- [ClawHub CLI](https://clawhub.ai/) (optional, for skill management)

## 📋 What's Included (Phase 1 & 2)

### Phase 1: Core Configuration & Skills
- **OpenClaw configuration**: `openclaw.json`, model providers, gateway settings
- **Skill inventory**: Built-in (52), ClawHub (0), custom (0) skills
- **Environment snapshot**: OS info, tool versions, system paths

### Phase 2: CLI Tools & Development Environments
- **CLI tool inventory**: Git, Node.js, Python, OpenClaw, ClawHub, etc.
- **Python environment**: 432 packages, virtual environment configuration
- **Node.js environment**: Global packages, npm configuration
- **Cross-platform recovery guides**: Windows (PowerShell), macOS (Homebrew), Linux (apt)

### Phase 2 Files Generated
```
backup/
├── cli-tools/
│   └── installed-cli.txt      # CLI tools with versions
├── environments/
│   ├── python-info.txt       # Python environment details
│   ├── python-requirements.txt # 432 packages list
│   ├── python-packages.txt   # Complete package list
│   ├── nodejs-info.txt       # Node.js environment details
│   ├── nodejs-packages.txt   # Global npm packages
│   └── environment-vars.txt  # Key environment variables
```

## ⚠️ Security Notes

**Important:** Configuration files may contain sensitive information:

- API keys and tokens
- Authentication credentials
- Personal preferences

**Before committing to version control:**
1. Review `configs/openclaw/openclaw.json` for API keys
2. Consider using environment variables for sensitive data
3. Use `.gitignore` to exclude sensitive files if needed

## 🔄 Update Process

To update the backup with current configuration:

1. Run the collection script again:
   ```powershell
   .\scripts\collect.ps1 -OutputPath .\backup
   ```

2. Review changes:
   ```powershell
   git status
   ```

3. Commit and push updates:
   ```powershell
   git add .
   git commit -m "Update configuration"
   git push
   ```

## 🛠️ Manual Steps After Restoration

Some configuration cannot be fully automated:

1. **API Keys**: You may need to regenerate or update API keys
2. **File Paths**: Update any machine-specific paths in configuration
3. **Skill Installation**: Install missing skills manually:
   ```powershell
   # For ClawHub skills
   clawhub install <skill-name>
   
   # For custom skills
   # Copy skill directories to ~\.openclaw\workspace\skills\
   ```

4. **Environment Variables**: Set up any required environment variables

## 📈 Current Status & Future Plans

### ✅ Completed Phases
- **Phase 1**: Core OpenClaw configuration backup & restore
- **Phase 2**: CLI tools & development environment backup

### 🔄 In Development
- **Phase 3**: CLI tool automated installation scripts
- **Phase 4**: Virtual environment auto-setup (venv, nvm, pyenv)

### 📅 Planned Enhancements
- **Phase 5**: Claude Code/Codex configuration integration
- **Phase 6**: Docker containerization support
- **Phase 7**: Health check & configuration drift detection

## 🤝 Contributing

This is a personal configuration backup system. Feel free to adapt it for your own needs by:

1. Forking the repository
2. Modifying the scripts for your environment
3. Adding support for additional tools (Claude Code, Codex, etc.)

## 🚀 GitHub Repository Setup

### Two-Repository Strategy

This project uses two GitHub repositories:

1. **`ai-agent-config-live`** - Continuous updates, daily backups
2. **`ai-agent-config-stable`** - Versioned releases, manual updates

### Automated Setup

Run the setup script to create both repositories:

```powershell
.\scripts\setup-github.ps1 -GitHubUsername "your-username"
```

You'll need a [GitHub Personal Access Token](https://github.com/settings/tokens) with `repo` and `workflow` scopes.

### Manual Setup

1. **Create repositories on GitHub:**
   - `ai-agent-config-live` (private recommended)
   - `ai-agent-config-stable` (private recommended)

2. **Push to live repository:**
   ```bash
   git remote add origin https://github.com/your-username/ai-agent-config-live.git
   git push -u origin master
   ```

3. **Set up stable repository:**
   ```bash
   git clone https://github.com/your-username/ai-agent-config-live.git ai-agent-config-stable
   cd ai-agent-config-stable
   git remote set-url origin https://github.com/your-username/ai-agent-config-stable.git
   git push -u origin master
   ```

### Creating Stable Releases

To create a stable release from the live repository:

```powershell
.\scripts\create-stable-release.ps1 -Version "v1.0.0"
```

This will:
1. Create a Git tag for the version
2. Generate release notes
3. Optionally update the stable repository

## ⚙️ Automation

### GitHub Actions
The repository includes a GitHub Actions workflow (`.github/workflows/auto-backup.yml`) that:
- Runs daily at 12:00 UTC
- Can be triggered manually
- Simulates backup collection (needs customization for your environment)

### Customizing Automation
Edit `.github/workflows/auto-backup.yml` to:
- Add actual configuration collection
- Set up environment-specific triggers
- Configure notification settings

## 🔒 Security Best Practices

### Before Committing
1. Run the sensitivity cleaning script:
   ```powershell
   .\scripts\clean-sensitive.ps1
   ```

2. Review configuration files for:
   - API keys and tokens
   - Personal information
   - Machine-specific paths

3. Use environment variables for sensitive data:
   ```powershell
   # Instead of hardcoded values in configs
   $env:OPENCLAW_API_KEY = "your-key-here"
   ```

### Repository Settings
1. **Private repositories** recommended for personal configurations
2. **Branch protection** for stable repository
3. **Secrets management** for automation tokens

## 📈 Development Roadmap

### ✅ Completed Phases
- **Phase 1**: Core OpenClaw configuration backup & restore
- **Phase 2**: CLI tools & development environment backup

### 🔄 Active Development
- **Phase 3**: CLI tool automated installation scripts
- **Phase 4**: Virtual environment auto-setup (venv, nvm, pyenv)

### 📅 Future Plans
- **Phase 5**: Claude Code/Codex configuration integration  
- **Phase 6**: Docker containerization support
- **Phase 7**: Health check & configuration drift detection

## 🤝 Contributing

This is a personal configuration backup system. Feel free to adapt it for your own needs by:

1. Forking the repository
2. Modifying the scripts for your environment
3. Adding support for additional tools (Claude Code, Codex, etc.)
4. Sharing improvements via pull requests

## 📄 License

This repository is for personal use. No specific license is applied.

---

**Last Updated**: 2026-03-27

**Phase**: 1-2 - Core Configuration + CLI/Environment Backup

**Status**: ✅ GitHub ready, automation configured