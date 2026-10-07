param([Parameter(Mandatory=$true)][string]$EnvelopePath)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$envelope = Get-Content -LiteralPath $EnvelopePath -Raw -Encoding UTF8 | ConvertFrom-Json
$agentExecutable = [string]$envelope.agent_path
$agentArguments = @($envelope.arguments | ForEach-Object { [string]$_ })
& $agentExecutable @agentArguments
if ($null -ne $LASTEXITCODE) { exit $LASTEXITCODE }
if (-not $?) { exit 1 }
exit 0
