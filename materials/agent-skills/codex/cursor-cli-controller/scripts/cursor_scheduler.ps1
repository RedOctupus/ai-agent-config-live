param(
    [Parameter(Mandatory=$true)][string]$EnvelopePath,
    [Parameter(Mandatory=$true)][ValidateSet('launch', 'cleanup')][string]$Operation
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$envelopeFullPath = [System.IO.Path]::GetFullPath($EnvelopePath)
$workerWorkingDirectory = [System.IO.Path]::GetFullPath($PSScriptRoot)
$launch = Get-Content -LiteralPath $envelopeFullPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($launch.token -cnotmatch '^[a-f0-9]{32}$' -or $launch.task_name -cne ('CursorController-Worker-' + $launch.token)) {
    throw 'Invalid controller-owned task identity'
}
if (-not [System.IO.Path]::IsPathRooted($launch.executable) -or -not (Test-Path -LiteralPath $launch.executable -PathType Leaf)) {
    throw 'Worker executable must be an existing absolute path'
}
$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$sid = $identity.User.Value
$description = 'CursorController transient worker; token=' + $launch.token + '; envelope=' + $envelopeFullPath
$service = New-Object -ComObject 'Schedule.Service'
$service.Connect()
$folder = $service.GetFolder('\')

function Assert-OwnedTask($task) {
    $definition = $task.Definition
    $principal = $definition.Principal.UserId
    if ($principal -match '^S-1-') {
        $principalSid = $principal
    } else {
        $principalSid = ([System.Security.Principal.NTAccount]::new($principal)).Translate([System.Security.Principal.SecurityIdentifier]).Value
    }
    if ($task.Name -cne $launch.task_name -or $definition.RegistrationInfo.Description -cne $description -or
        $principalSid -ine $sid -or $definition.Principal.RunLevel -ne 0 -or
        $definition.Actions.Count -ne 1 -or $definition.Actions.Item(1).Path -ine $launch.executable -or
        $definition.Actions.Item(1).Arguments -cne $launch.arguments -or
        $definition.Actions.Item(1).WorkingDirectory -ine $workerWorkingDirectory) {
        throw 'Task identity mismatch; refusing to modify an unowned entry'
    }
}

if ($Operation -eq 'cleanup') {
    $task = $folder.GetTask($launch.task_name)
    Assert-OwnedTask $task
    $folder.DeleteTask($launch.task_name, 0)
    @{deleted=$true; task_name=$launch.task_name; sid=$sid} | ConvertTo-Json -Compress
    exit 0
}

$definition = $service.NewTask(0)
$definition.RegistrationInfo.Description = $description
$definition.RegistrationInfo.Author = $sid
$definition.Principal.UserId = $sid
$definition.Principal.LogonType = 3 # TASK_LOGON_INTERACTIVE_TOKEN; current user, no password/elevation
$definition.Principal.RunLevel = 0
$definition.Settings.Hidden = $true
$definition.Settings.Enabled = $true
$definition.Settings.AllowDemandStart = $true
$definition.Settings.DisallowStartIfOnBatteries = $false
$definition.Settings.StopIfGoingOnBatteries = $false
$definition.Settings.ExecutionTimeLimit = 'PT0S'
$definition.Settings.MultipleInstances = 2 # Ignore duplicate starts; worker also claims its run transactionally.
$action = $definition.Actions.Create(0)
$action.Path = $launch.executable
$action.Arguments = $launch.arguments
# The venv pythonw redirector can outlive the final worker PID briefly. Keep its
# cwd outside disposable run storage; executor workspace cwd remains explicit.
$action.WorkingDirectory = $workerWorkingDirectory
# CREATE only: never replace any existing task, even one with the same name.
$task = $folder.RegisterTaskDefinition($launch.task_name, $definition, 2, $sid, $null, 3, $null)
Assert-OwnedTask $task
$instance = $task.Run($null)
@{scheduled=$true; task_name=$launch.task_name; sid=$sid; instance_id=$instance.InstanceGuid} | ConvertTo-Json -Compress
