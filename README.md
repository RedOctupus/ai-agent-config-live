# AI Agent Configuration Backup

This repository contains backup and restoration scripts for AI Agent development environments, focusing on OpenClaw configuration.

## 📁 Repository Structure

```
ai-agent-config-backup/
├── scripts/
│   ├── collect.ps1          # Configuration collection script
│   └── install.ps1          # Configuration restoration script
├── configs/
│   └── openclaw/           # OpenClaw configuration files
├── skills/
│   ├── builtin-skills.txt  # List of built-in OpenClaw skills
│   ├── clawhub-skills.txt  # List of ClawHub installed skills
│   └── custom-skills.txt   # List of custom skills
├── environment/
│   └── system-info.txt     # System environment information
└── README.md               # This file
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
cd ai-agent-config-backup

# Run the installation script
.\scripts\install.ps1 -ConfigPath .\backup
```

**Important:** The installation script will:
- Backup your existing OpenClaw configuration
- Restore configuration files from the backup
- Show you what skills were installed
- Provide next steps for manual configuration

## 🔧 Prerequisites

Before restoring configuration, ensure you have:

- [OpenClaw](https://openclaw.ai/) installed
- [Node.js](https://nodejs.org/) and npm
- [Python](https://python.org/) (for some skills)
- [Git](https://git-scm.com/)
- [ClawHub CLI](https://clawhub.ai/) (optional, for skill management)

## 📋 What's Included (Phase 1)

### Core Configuration
- OpenClaw main configuration (`openclaw.json`)
- Model provider settings
- Skill enable/disable states
- Gateway configuration

### Skill Inventory
- **Built-in skills**: All skills included with OpenClaw installation
- **ClawHub skills**: Skills installed via ClawHub registry
- **Custom skills**: User-created skills in workspace

### Environment Information
- Operating system details
- Tool versions (Python, Node.js, Git, etc.)
- Important environment paths

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

## 📈 Future Enhancements (Planned)

- **Phase 2**: CLI tool installation automation
- **Phase 3**: Virtual environment setup (Python, Node.js)
- **Phase 4**: GitHub Actions for automatic backup
- **Phase 5**: Stable version repository with release tags

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

## 📈 Future Enhancements

### Phase 3 Planned Features
- CLI tool installation automation
- Virtual environment setup scripts
- Cross-platform support (Linux, macOS)
- Health check and validation scripts
- Integration with Claude Code and Codex configurations

### Phase 4 Planned Features
- Docker containerization
- Cloud backup integration
- Configuration drift detection
- Automated testing of restoration

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