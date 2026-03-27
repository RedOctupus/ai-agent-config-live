# GitHub Repository Setup Script
# This script helps set up GitHub repositories for AI Agent configuration backup

param(
    [string]$RepoNameLive = "ai-agent-config-live",
    [string]$RepoNameStable = "ai-agent-config-stable",
    [string]$GitHubUsername = "",
    [string]$GitHubToken = ""
)

Write-Host "🚀 GitHub Repository Setup for AI Agent Configuration" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Green

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Git is installed" -ForegroundColor Gray

# Check if we're in a Git repository
if (-not (Test-Path ".git")) {
    Write-Host "❌ Not in a Git repository. Run this script from the repository root." -ForegroundColor Red
    exit 1
}

Write-Host "✅ In a Git repository" -ForegroundColor Gray

# Ask for GitHub credentials if not provided
if ([string]::IsNullOrEmpty($GitHubUsername)) {
    $GitHubUsername = Read-Host "Enter your GitHub username"
}

if ([string]::IsNullOrEmpty($GitHubToken)) {
    Write-Host ""
    Write-Host "🔑 GitHub Personal Access Token required" -ForegroundColor Yellow
    Write-Host "Create a token at: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host "Required scopes: repo, workflow" -ForegroundColor Gray
    Write-Host ""
    $GitHubToken = Read-Host "Enter your GitHub Personal Access Token" -AsSecureString
    $GitHubToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($GitHubToken)
    )
}

# Function to create GitHub repository using REST API
function Create-GitHubRepo {
    param(
        [string]$Name,
        [string]$Description,
        [bool]$Private = $false
    )
    
    $body = @{
        name = $Name
        description = $Description
        private = $Private
        auto_init = $false
        has_issues = $true
        has_projects = $false
        has_wiki = $false
        has_downloads = $false
    } | ConvertTo-Json
    
    $headers = @{
        "Authorization" = "token $GitHubToken"
        "Accept" = "application/vnd.github.v3+json"
        "User-Agent" = "OpenClaw-Agent"
    }
    
    try {
        Write-Host "Creating repository: $Name..." -ForegroundColor Green
        $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
            -Method Post `
            -Headers $headers `
            -Body $body `
            -ContentType "application/json"
        
        Write-Host "✅ Repository created: $($response.html_url)" -ForegroundColor Green
        return $response
    } catch {
        Write-Host "❌ Failed to create repository: $Name" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Create Live repository
Write-Host ""
Write-Host "📦 Creating Live Repository (Continuous Updates)" -ForegroundColor Cyan
$liveRepo = Create-GitHubRepo -Name $RepoNameLive `
    -Description "AI Agent configuration - live/continuous updates" `
    -Private $true

if (-not $liveRepo) {
    Write-Host "❌ Failed to create live repository. Exiting." -ForegroundColor Red
    exit 1
}

# Add remote and push
Write-Host ""
Write-Host "🔄 Setting up remote and pushing code..." -ForegroundColor Green
git remote add origin $liveRepo.clone_url
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to add remote. Remote might already exist." -ForegroundColor Yellow
    Write-Host "   Removing existing remote and trying again..." -ForegroundColor Gray
    git remote remove origin 2>$null
    git remote add origin $liveRepo.clone_url
}

# Set up authentication for push
$remoteUrl = $liveRepo.clone_url -replace "https://", "https://${GitHubUsername}:${GitHubToken}@"
git remote set-url origin $remoteUrl

Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin master
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to push to GitHub. Trying with force..." -ForegroundColor Yellow
    git push -u origin master --force
}

# Create Stable repository
Write-Host ""
Write-Host "📦 Creating Stable Repository (Versioned Releases)" -ForegroundColor Cyan
$stableRepo = Create-GitHubRepo -Name $RepoNameStable `
    -Description "AI Agent configuration - stable/versioned releases" `
    -Private $true

if ($stableRepo) {
    Write-Host ""
    Write-Host "📋 Stable repository created. Manual setup required:" -ForegroundColor Yellow
    Write-Host "1. Clone the stable repository: git clone $($stableRepo.clone_url)" -ForegroundColor Gray
    Write-Host "2. Copy files from live repository" -ForegroundColor Gray
    Write-Host "3. Create first release tag" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   Or use the included script: scripts/create-stable-release.ps1" -ForegroundColor Gray
}

# Create GitHub Actions workflow for auto-backup
Write-Host ""
Write-Host "⚙️ Creating GitHub Actions workflow..." -ForegroundColor Green
$workflowDir = ".github\workflows"
New-Item -ItemType Directory -Path $workflowDir -Force | Out-Null

$workflowContent = @'
name: Auto Backup Configuration
on:
  schedule:
    - cron: '0 12 * * *'  # Daily at 12:00 UTC
  workflow_dispatch:  # Manual trigger

jobs:
  backup:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.13'
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
    
    - name: Run backup collection (simulation)
      run: |
        echo "Backup simulation - real implementation would collect configuration"
        echo "Date: $(date)" > backup-info.txt
        echo "This is a placeholder for actual backup logic" >> backup-info.txt
    
    - name: Commit and push if changed
      run: |
        git config --global user.name 'GitHub Actions'
        git config --global user.email 'actions@github.com'
        git add -A
        git diff --quiet && git diff --staged --quiet || git commit -m "Auto-backup: $(date)"
        git push
'@

$workflowContent | Out-File "$workflowDir\auto-backup.yml" -Encoding UTF8
Write-Host "✅ GitHub Actions workflow created: .github/workflows/auto-backup.yml" -ForegroundColor Green

# Add workflow file to Git
git add "$workflowDir\auto-backup.yml"
git commit -m "Add GitHub Actions workflow for auto-backup" 2>$null

# Push workflow file
git push

Write-Host ""
Write-Host "✅ GitHub setup complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Repository URLs:" -ForegroundColor Yellow
Write-Host "   Live (continuous updates): $($liveRepo.html_url)" -ForegroundColor Gray
if ($stableRepo) {
    Write-Host "   Stable (versioned releases): $($stableRepo.html_url)" -ForegroundColor Gray
}
Write-Host ""
Write-Host "🔧 Next steps:" -ForegroundColor Yellow
Write-Host "1. Review the GitHub Actions workflow: .github/workflows/auto-backup.yml" -ForegroundColor Gray
Write-Host "2. Configure repository secrets for automation" -ForegroundColor Gray
Write-Host "3. Create first stable release from the live repository" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  Security note: Your GitHub token was used in this script." -ForegroundColor Red
Write-Host "   Consider revoking it and using repository secrets for automation." -ForegroundColor Red