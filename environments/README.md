# Virtual Environments Configuration

This directory contains configuration for virtual environments used in AI Agent development.

## Structure

```
environments/
├── python/
│   ├── requirements.txt      # Python package requirements
│   ├── requirements-dev.txt  # Development requirements
│   ├── environment.yml       # Conda environment specification
│   └── pipenv-files/         # Pipenv configuration
├── nodejs/
│   ├── package.json         # Node.js dependencies
│   ├── package-lock.json    # Lock file
│   └── .nvmrc              # Node version manager config
├── conda/
│   └── environment.yml      # Conda environment
└── system/
    └── env-vars.txt        # System environment variables
```

## Python Environments

### Virtual Environments
- `venv`: Standard Python virtual environment
- `conda`: Conda environments
- `pipenv`: Pipenv virtual environments

### Collection Process
1. Identify active Python environments
2. Export package lists (`pip freeze`, `conda env export`)
3. Capture environment-specific configurations
4. Store activation scripts

### Restoration Process
1. Create new virtual environment
2. Install packages from requirements
3. Configure environment settings
4. Set up activation hooks

## Node.js Environments

### Package Management
- `npm`: Node Package Manager
- `yarn`: Alternative package manager
- `pnpm`: Fast, disk space efficient package manager

### Collection Process
1. Find `package.json` files in workspace
2. Record global npm packages
3. Capture Node.js version
4. Store npm configuration

### Restoration Process
1. Install Node.js (if not present)
2. Install global packages
3. Install project dependencies
4. Configure npm settings

## Cross-Platform Considerations

### Windows
- PowerShell activation scripts
- Path environment variable handling
- Windows-specific package requirements

### macOS/Linux
- Bash activation scripts
- Shell environment variables
- Unix-specific configurations

## Best Practices

1. **Version Pinning**: Pin specific package versions for reproducibility
2. **Environment Isolation**: Keep project environments separate
3. **Platform Markers**: Use platform-specific requirements when needed
4. **Documentation**: Document environment setup and usage
5. **Testing**: Test environment creation on target platforms