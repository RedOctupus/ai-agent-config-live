#Requires -Version 5.1
# Start ocr viewer if port 5483 is free. stdout = JSON only.
param(
    [string]$Addr = 'localhost:5483'
)

$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Test-TcpPort([int]$Port) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $iar = $client.BeginConnect('127.0.0.1', $Port, $null, $null)
        $ok = $iar.AsyncWaitHandle.WaitOne(400)
        return [bool]($ok -and $client.Connected)
    } catch {
        return $false
    } finally {
        $client.Close()
    }
}

$port = 5483
if ($Addr -match ':(\d+)$') { $port = [int]$Matches[1] }
$url = "http://$Addr"
if ($Addr -match '^:') { $url = "http://localhost$port" }

$ocrCmd = Get-Command ocr.cmd -ErrorAction SilentlyContinue
$ocrExe = Get-Command ocr.exe -ErrorAction SilentlyContinue
$ocrAny = Get-Command ocr -ErrorAction SilentlyContinue
$launchFile = $null
$launchPrefix = @()
if ($ocrCmd -and $ocrCmd.Source) {
    $launchFile = $ocrCmd.Source
} elseif ($ocrExe -and $ocrExe.Source) {
    $launchFile = $ocrExe.Source
} elseif ($ocrAny -and $ocrAny.Source -match '\.exe$') {
    $launchFile = $ocrAny.Source
} elseif ($ocrAny -and $ocrAny.Source) {
    $sibling = [IO.Path]::ChangeExtension($ocrAny.Source, '.cmd')
    if (Test-Path -LiteralPath $sibling) {
        $launchFile = $sibling
    } elseif ($ocrAny.Source -match '\.ps1$') {
        $launchFile = (Get-Command powershell).Source
        $launchPrefix = @('-NoProfile', '-File', $ocrAny.Source)
    }
}

if (-not $launchFile) {
    '{"ok":false,"error":"ocr not on PATH","started":false,"already_running":false}' | Write-Output
    exit 2
}

if (Test-TcpPort $port) {
    $o = [ordered]@{
        ok              = $true
        started         = $false
        already_running = $true
        url             = "http://localhost:$port"
        addr            = $Addr
    }
    $o | ConvertTo-Json -Compress | Write-Output
    exit 0
}

$logDir = Join-Path $env:TEMP 'ocr-viewer'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$outLog = Join-Path $logDir 'stdout.log'
$errLog = Join-Path $logDir 'stderr.log'
$proc = Start-Process -FilePath $launchFile -ArgumentList ($launchPrefix + @('viewer', '--open=never', '--addr', $Addr)) `
    -WindowStyle Hidden -PassThru -RedirectStandardOutput $outLog -RedirectStandardError $errLog

$up = $false
for ($i = 0; $i -lt 50; $i++) {
    Start-Sleep -Milliseconds 200
    if (Test-TcpPort $port) { $up = $true; break }
}

$o = [ordered]@{
    ok              = $up
    started         = $true
    already_running = $false
    url             = "http://localhost:$port"
    addr            = $Addr
    pid             = $proc.Id
    log             = $outLog
}
$o | ConvertTo-Json -Compress | Write-Output
if ($up) { exit 0 } else { exit 3 }
