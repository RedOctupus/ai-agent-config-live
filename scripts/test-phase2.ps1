# Test Phase 2 Collection Script
# This script tests the Phase 2 collection functionality

param(
    [string]$TestDir = ".\test-phase2-validation"
)

Write-Host "🧪 Testing Phase 2 Collection" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Clean up previous test if exists
if (Test-Path $TestDir) {
    Remove-Item -Path $TestDir -Recurse -Force
    Write-Host "Cleaned up previous test directory" -ForegroundColor Gray
}

# Run collection with Phase 2 enabled
Write-Host "Running collection script..." -ForegroundColor Green
.\scripts\collect.ps1 -OutputPath $TestDir

Write-Host ""
Write-Host "📊 Test Results" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan

# Verify all expected files exist
$expectedFiles = @(
    "configs\openclaw\openclaw.json",
    "configs\openclaw\exec-approvals.json",
    "configs\openclaw\update-check.json",
    "skills\builtin-skills.txt",
    "skills\clawhub-skills.txt",
    "skills\custom-skills.txt",
    "environment\system-info.txt",
    "cli-tools\installed-cli.txt",
    "environments\python-info.txt",
    "environments\nodejs-info.txt"
)

$allPassed = $true
foreach ($file in $expectedFiles) {
    $fullPath = Join-Path $TestDir $file
    if (Test-Path $fullPath) {
        $size = (Get-Item $fullPath).Length
        Write-Host "✅ $file ($size bytes)" -ForegroundColor Green
    } else {
        Write-Host "❌ $file (MISSING)" -ForegroundColor Red
        $allPassed = $false
    }
}

# Check file contents
Write-Host ""
Write-Host "📝 Sample File Contents" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

if (Test-Path "$TestDir\cli-tools\installed-cli.txt") {
    Write-Host "CLI Tools Found:" -ForegroundColor Green
    Get-Content "$TestDir\cli-tools\installed-cli.txt" | ForEach-Object {
        Write-Host "  $_" -ForegroundColor Gray
    }
}

if (Test-Path "$TestDir\environments\python-requirements.txt") {
    $packageCount = (Get-Content "$TestDir\environments\python-requirements.txt" | Measure-Object).Count
    Write-Host "Python Packages: $packageCount" -ForegroundColor Green
}

Write-Host ""
if ($allPassed) {
    Write-Host "🎉 All tests passed!" -ForegroundColor Green
    Write-Host "Phase 2 collection is working correctly." -ForegroundColor Gray
} else {
    Write-Host "⚠️  Some tests failed. Check the missing files." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📁 Test directory: $TestDir" -ForegroundColor Cyan
Write-Host "📋 To clean up: Remove-Item -Path $TestDir -Recurse -Force" -ForegroundColor Gray