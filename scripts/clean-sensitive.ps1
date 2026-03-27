# Clean Sensitive Information from Configuration Files
# This script removes API keys and other sensitive information from configuration files

param(
    [string]$ConfigPath = ".\configs\openclaw"
)

Write-Host "🔒 Cleaning sensitive information from configuration files..." -ForegroundColor Cyan

if (-not (Test-Path $ConfigPath)) {
    Write-Host "❌ Configuration path not found: $ConfigPath" -ForegroundColor Red
    exit 1
}

# Backup original files
$backupDir = "$ConfigPath\backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
Copy-Item "$ConfigPath\*.json" -Destination $backupDir -Force
Write-Host "📁 Original files backed up to: $backupDir" -ForegroundColor Gray

# Process openclaw.json
$openclawFile = Join-Path $ConfigPath "openclaw.json"
if (Test-Path $openclawFile) {
    Write-Host "🔧 Cleaning openclaw.json..." -ForegroundColor Green
    $content = Get-Content $openclawFile -Raw | ConvertFrom-Json
    
    # Remove API keys from providers
    if ($content.models.providers) {
        foreach ($providerName in $content.models.providers.PSObject.Properties.Name) {
            $provider = $content.models.providers.$providerName
            if ($provider.apiKey) {
                $provider.apiKey = "<REMOVED_API_KEY>"
                Write-Host "  Removed API key from provider: $providerName" -ForegroundColor Gray
            }
        }
    }
    
    # Convert back to JSON and save
    $cleanedContent = $content | ConvertTo-Json -Depth 10
    $cleanedContent | Out-File $openclawFile -Encoding UTF8
    Write-Host "  ✅ openclaw.json cleaned" -ForegroundColor Green
}

# Create example configuration
$exampleFile = Join-Path $ConfigPath "openclaw.example.json"
@"
{
  "meta": {
    "lastTouchedVersion": "2026.3.24",
    "lastTouchedAt": "2026-03-27T03:32:56.872Z"
  },
  "auth": {
    "profiles": {
      "example-provider:default": {
        "provider": "example-provider",
        "mode": "api_key"
      }
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "deepseek": {
        "baseUrl": "https://api.deepseek.com",
        "apiKey": "<YOUR_DEEPSEEK_API_KEY_HERE>",
        "api": "openai-completions",
        "models": [
          {
            "id": "deepseek-chat",
            "name": "Deepseek Chat",
            "api": "openai-completions",
            "input": ["text", "image"],
            "contextWindow": 64000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-chat"
      }
    }
  }
}
"@ | Out-File $exampleFile -Encoding UTF8

Write-Host "📄 Example configuration created: openclaw.example.json" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Cleaning complete!" -ForegroundColor Cyan
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Review the cleaned configuration files" -ForegroundColor Gray
Write-Host "2. Compare with backup if needed: $backupDir" -ForegroundColor Gray
Write-Host "3. Update API keys with your own values when restoring" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  Important: Original files backed up to $backupDir" -ForegroundColor Red
Write-Host "   Make sure to delete this backup if it contains sensitive information!" -ForegroundColor Red