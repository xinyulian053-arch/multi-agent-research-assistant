$ErrorActionPreference = "SilentlyContinue"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

function Stop-ProcessTree {
    param([int]$ProcessId)
    if ($ProcessId -le 0) { return }

    $children = Get-CimInstance Win32_Process -Filter "ParentProcessId=$ProcessId"
    foreach ($child in $children) {
        Stop-ProcessTree -ProcessId $child.ProcessId
    }

    Stop-Process -Id $ProcessId -Force
}

foreach ($pidFile in @(".backend.pid", ".frontend.pid")) {
    $path = Join-Path $Root $pidFile
    if (Test-Path -LiteralPath $path) {
        $pidValue = Get-Content -LiteralPath $path
        if ($pidValue) {
            Stop-ProcessTree -ProcessId ([int]$pidValue)
        }
        Remove-Item -LiteralPath $path -Force
    }
}

Write-Host "Research Assistant services stopped."
