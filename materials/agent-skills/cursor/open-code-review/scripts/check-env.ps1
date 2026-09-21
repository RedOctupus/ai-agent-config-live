#Requires -Version 5.1
# OCR environment gate. stdout = JSON only. Never prints API keys.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check-env.ps1
#        powershell ... -File scripts/check-env.ps1 -TestLlm

param(
    [switch]$TestLlm
)

$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Test-TcpPort([int]$Port) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $iar = $client.BeginConnect('127.0.0.1', $Port, $null, $null)
        $ok = $iar.AsyncWaitHandle.WaitOne(400)
        if ($ok -and $client.Connected) { return $true }
        return $false
    } catch {
        return $false
    } finally {
        $client.Close()
    }
}

function Get-CommandPath([string]$Name) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return [string]$cmd.Source }
    return $null
}

function Get-GitInfo {
    $path = Get-CommandPath 'git'
    if (-not $path) {
        return @{ ok = $false; version = $null; path = $null }
    }
    $raw = (& git --version 2>$null | Out-String).Trim()
    $ok = $false
    $version = $raw
    if ($raw -match 'git version (\d+)\.(\d+)') {
        $maj = [int]$Matches[1]
        $min = [int]$Matches[2]
        $ok = ($maj -gt 2) -or (($maj -eq 2) -and ($min -ge 41))
        $version = "$maj.$min"
        if ($raw -match 'git version ([^\s]+)') { $version = $Matches[1] }
    }
    return @{ ok = $ok; version = $version; path = $path; raw = $raw }
}

function Get-OcrInfo {
    $path = Get-CommandPath 'ocr'
    if (-not $path) {
        return @{ ok = $false; version = $null; path = $null }
    }
    $raw = (& ocr version 2>$null | Out-String).Trim()
    $version = $null
    if ($raw -match 'v?(\d+\.\d+\.\d+)') { $version = $Matches[1] }
    return @{ ok = $true; version = $version; path = $path; raw = ($raw -split "`n")[0] }
}

function Get-NodeInfo {
    $path = Get-CommandPath 'node'
    if (-not $path) {
        return @{ ok = $false; version = $null }
    }
    $raw = (& node -v 2>$null | Out-String).Trim()
    $ok = $false
    if ($raw -match 'v(\d+)') { $ok = ([int]$Matches[1] -ge 18) }
    return @{ ok = $ok; version = $raw; path = $path }
}

$ProviderEnv = [ordered]@{
    deepseek            = 'DEEPSEEK_API_KEY'
    dashscope           = 'DASHSCOPE_API_KEY'
    kimi                = 'MOONSHOT_API_KEY'
    openai              = 'OPENAI_API_KEY'
    anthropic           = 'ANTHROPIC_API_KEY'
    volcengine          = 'ARK_API_KEY'
    'siliconflow-cn'    = 'SILICONFLOW_API_KEY'
    'z-ai'              = 'Z_AI_API_KEY'
    gemini              = 'GEMINI_API_KEY'
}

function Test-EnvSet([string]$Name) {
    $val = [Environment]::GetEnvironmentVariable($Name)
    return -not [string]::IsNullOrWhiteSpace($val)
}

function Get-LlmInfo {
    $homeCfg = Join-Path $env:USERPROFILE '.opencodereview\config.json'
    $configured = $false
    $provider = $null
    $model = $null
    $language = $null
    $fromEnv = @()
    foreach ($k in $ProviderEnv.Keys) {
        if (Test-EnvSet $ProviderEnv[$k]) { $fromEnv += $k }
    }
    if (Test-Path -LiteralPath $homeCfg) {
        try {
            $cfg = Get-Content -LiteralPath $homeCfg -Raw -Encoding UTF8 | ConvertFrom-Json
            $provider = [string]$cfg.provider
            $language = [string]$cfg.language
            if ($cfg.model) { $model = [string]$cfg.model }
            if ($provider -and $cfg.providers -and $cfg.providers.$provider) {
                $p = $cfg.providers.$provider
                if ($p.model) { $model = [string]$p.model }
                if ($p.api_key) { $configured = $true }
                if ($p.api_key_cmd) { $configured = $true }
            }
            if ($provider -and $cfg.custom_providers -and $cfg.custom_providers.$provider) {
                $p = $cfg.custom_providers.$provider
                if ($p.model) { $model = [string]$p.model }
                if ($p.api_key) { $configured = $true }
                if ($p.url) { $configured = $true }
            }
            if (-not $configured -and $provider -and $ProviderEnv.Contains($provider)) {
                if (Test-EnvSet $ProviderEnv[$provider]) { $configured = $true }
            }
            if (-not $configured -and $cfg.llm -and ($cfg.llm.auth_token -or $cfg.llm.url)) {
                $configured = $true
            }
        } catch {
            # keep defaults
        }
    }
    if (-not $configured -and $fromEnv.Count -gt 0) {
        $configured = $true
        if (-not $provider) { $provider = $fromEnv[0] }
    }
    $tested = $null
    if ($TestLlm -and (Get-CommandPath 'ocr')) {
        $out = & ocr llm test 2>&1 | Out-String
        $tested = $out -match 'successful'
    }
    return @{
        configured = [bool]$configured
        tested     = $tested
        provider   = $provider
        model      = $model
        language   = $language
        env_hints  = @($fromEnv)
    }
}

function Get-Recommend($node, $llm) {
    $install = 'npm'
    $installReason = 'npm wrapper auto-updates; needs Node.js 18+'
    $os = $env:OS
    if ($node.ok) {
        $install = 'npm'
        $installReason = "detected $($node.version); recommend npm"
    } elseif ($os -match 'Windows') {
        $install = 'windows-ps1'
        $installReason = 'Node.js 18+ not found; recommend install.ps1'
    }
    $provider = 'deepseek'
    $providerReason = 'no API key env var detected; DeepSeek is a common default'
    if ($llm.env_hints -and $llm.env_hints.Count -gt 0) {
        $provider = $llm.env_hints[0]
        $providerReason = "env $($ProviderEnv[$provider]) is set"
    } elseif ($llm.provider) {
        $provider = $llm.provider
        $providerReason = "config.json provider=$provider"
    }
    return @{
        install         = $install
        install_reason  = $installReason
        provider        = $provider
        provider_reason = $providerReason
    }
}

$git = Get-GitInfo
$ocr = Get-OcrInfo
$node = Get-NodeInfo
$llm = Get-LlmInfo
$viewerPort = 5483
$viewerRunning = Test-TcpPort $viewerPort
$recommend = Get-Recommend $node $llm

$missing = @()
if (-not $git.ok) { $missing += 'git>=2.41' }
if (-not $ocr.ok) { $missing += 'ocr' }

$readyFor = @()
if ($ocr.ok -and $git.ok) { $readyFor += 'delegate' }
if ($ocr.ok -and $git.ok -and $llm.configured) {
    $readyFor += 'review'
    $readyFor += 'scan'
}

$ok = ($git.ok -and $ocr.ok)
$next = 'start-viewer'
if (-not $git.ok) { $next = 'init-git' }
elseif (-not $ocr.ok) { $next = 'init-install' }
elseif (-not $llm.configured) { $next = 'init-llm' }
elseif ($TestLlm -and ($llm.tested -eq $false)) { $next = 'init-llm' }
elseif ($viewerRunning) { $next = 'dispatch' }

$result = [ordered]@{
    ok        = $ok
    next      = $next
    missing   = $missing
    ready_for = $readyFor
    git       = $git
    ocr       = $ocr
    node      = $node
    llm       = $llm
    viewer    = @{
        running = $viewerRunning
        url     = "http://localhost:$viewerPort"
        addr    = "localhost:$viewerPort"
    }
    recommend = $recommend
}

$json = $result | ConvertTo-Json -Depth 6 -Compress:$false
[Console]::Out.WriteLine($json)
exit 0
