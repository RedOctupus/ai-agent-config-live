# Create Stable Release Script
# This script helps create a stable release from the live repository

param(
    [string]$Version = "v1.0.0",
    [string]$StableRepoUrl = "",
    [switch]$DryRun = $false
)

Write-Host "🏷️ Creating Stable Release: $Version" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Check if we're in a Git repository
if (-not (Test-Path ".git")) {
    Write-Host "❌ Not in a Git repository. Run this script from the repository root." -ForegroundColor Red
    exit 1
}

# Get current branch
$currentBranch = git rev-parse --abbrev-ref HEAD
if ($currentBranch -ne "master") {
    Write-Host "⚠️  You are not on the master branch. Current branch: $currentBranch" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        Write-Host "Operation cancelled." -ForegroundColor Red
        exit 0
    }
}

# Create tag
Write-Host "🔖 Creating Git tag: $Version" -ForegroundColor Green
if (-not $DryRun) {
    git tag -a $Version -m "Stable release: $Version"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create tag. Tag might already exist." -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Tag created locally" -ForegroundColor Green
} else {
    Write-Host "📋 (Dry run) Would create tag: $Version" -ForegroundColor Gray
}

# Push tag to remote
Write-Host "📤 Pushing tag to remote repository..." -ForegroundColor Green
if (-not $DryRun) {
    git push origin $Version
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to push tag. Check your remote configuration." -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Tag pushed to remote" -ForegroundColor Green
} else {
    Write-Host "📋 (Dry run) Would push tag to remote" -ForegroundColor Gray
}

# If stable repository URL is provided, clone and update it
if (-not [string]::IsNullOrEmpty($StableRepoUrl)) {
    Write-Host ""
    Write-Host "📦 Updating stable repository..." -ForegroundColor Cyan
    
    $tempDir = "$env:TEMP\ai-agent-stable-$([System.Guid]::NewGuid().ToString().Substring(0,8))"
    
    try {
        Write-Host "Cloning stable repository..." -ForegroundColor Green
        if (-not $DryRun) {
            git clone $StableRepoUrl $tempDir
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to clone stable repository"
            }
            
            # Copy all files from current directory to stable repo (excluding .git)
            Write-Host "Copying files..." -ForegroundColor Green
            Get-ChildItem -Path . -Force | Where-Object { $_.Name -ne ".git" } | ForEach-Object {
                Copy-Item -Path $_.FullName -Destination $tempDir -Recurse -Force
            }
            
            # Commit and push to stable repo
            Set-Location $tempDir
            git add -A
            git commit -m "Update to version $Version from live repository"
            git push origin master
            
            # Create tag in stable repo too
            git tag -a $Version -m "Stable release: $Version"
            git push origin $Version
            
            Write-Host "✅ Stable repository updated with version $Version" -ForegroundColor Green
        } else {
            Write-Host "📋 (Dry run) Would clone stable repo and update with version $Version" -ForegroundColor Gray
        }
    } catch {
        Write-Host "❌ Failed to update stable repository: $_" -ForegroundColor Red
    } finally {
        if (Test-Path $tempDir) {
            Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
        }
        Set-Location $PSScriptRoot
    }
}

# Create release notes template
Write-Host ""
Write-Host "📝 Creating release notes template..." -ForegroundColor Green
$releaseNotes = @"
# Release $Version - AI Agent Configuration

**Release Date**: $(Get-Date -Format 'yyyy-MM-dd')

## Overview
This release contains a stable snapshot of the AI Agent development environment configuration.

## Changes since last stable release
- [List major changes here]

## Configuration Details

### OpenClaw Configuration
- Model providers configured: [Number]
- Skills enabled: [Number]
- Settings: [Brief summary]

### CLI Tools Included
- [List key CLI tools]

### Environment Specifications
- Python packages: [Count]
- Node.js packages: [Count]
- System requirements: [Brief]

## Installation Instructions

1. Clone the stable repository:
   ```bash
   git clone [STABLE_REPO_URL] --branch $Version
   ```

2. Run the installation script:
   ```powershell
   cd ai-agent-config-stable
   .\scripts\install.ps1 -ConfigPath .\backup
   ```

3. Update API keys and sensitive information

## Upgrade Notes
- [Any upgrade instructions]

## Known Issues
- [List any known issues]

## Files Included
\`\`\`
$(if (-not $DryRun) {
    Get-ChildItem -Recurse -File | Select-Object -ExpandProperty Name | Sort-Object
} else {
    "[File list would be generated here]"
})
\`\`\`
"@

$releaseNotes | Out-File "RELEASE-$Version.md" -Encoding UTF8
Write-Host "✅ Release notes template created: RELEASE-$Version.md" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Stable release process complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Review the release notes: RELEASE-$Version.md" -ForegroundColor Gray
Write-Host "2. Create a GitHub Release with the tag $Version" -ForegroundColor Gray
Write-Host "3. Upload the release notes and any additional files" -ForegroundColor Gray
Write-Host "4. Update the stable repository if separate" -ForegroundColor Gray
Write-Host ""
Write-Host "🔗 GitHub Release URL template:" -ForegroundColor Gray
Write-Host "   https://github.com/[USERNAME]/ai-agent-config-live/releases/tag/$Version" -ForegroundColor Gray