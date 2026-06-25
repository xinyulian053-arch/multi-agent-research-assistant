$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$FrontendDir = Join-Path $Root "frontend"
$LogDir = Join-Path $Root "runtime_logs"
$BackendPidPath = Join-Path $Root ".backend.pid"
$FrontendPidPath = Join-Path $Root ".frontend.pid"
$PythonDepsStamp = Join-Path $Root ".python-deps.ready"
$RequirementsPath = Join-Path $Root "requirements.txt"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Stop-ProcessTree {
    param([int]$ProcessId)
    if ($ProcessId -le 0) { return }

    $children = Get-CimInstance Win32_Process -Filter "ParentProcessId=$ProcessId" -ErrorAction SilentlyContinue
    foreach ($child in $children) {
        Stop-ProcessTree -ProcessId $child.ProcessId
    }

    Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
}

function Stop-FromPidFile {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        $pidValue = Get-Content -LiteralPath $Path -ErrorAction SilentlyContinue
        if ($pidValue) {
            Stop-ProcessTree -ProcessId ([int]$pidValue)
        }
        Remove-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    }
}

Set-Location $Root
Stop-FromPidFile $BackendPidPath
Stop-FromPidFile $FrontendPidPath

$Python = Join-Path $Root "venv\Scripts\python.exe"
if (!(Test-Path -LiteralPath $Python)) {
    Write-Host "Creating Python virtual environment..."
    python -m venv (Join-Path $Root "venv")
}

$ShouldInstallPythonDeps = !(Test-Path -LiteralPath $PythonDepsStamp)
if (!$ShouldInstallPythonDeps -and (Test-Path -LiteralPath $RequirementsPath)) {
    $ShouldInstallPythonDeps = (Get-Item $RequirementsPath).LastWriteTimeUtc -gt (Get-Item $PythonDepsStamp).LastWriteTimeUtc
}

if ($ShouldInstallPythonDeps) {
    Write-Host "Installing Python dependencies..."
    & $Python -m pip install -r $RequirementsPath
    "ok" | Set-Content -Encoding ASCII -Path $PythonDepsStamp
}

if (!(Test-Path -LiteralPath (Join-Path $FrontendDir "node_modules"))) {
    Write-Host "Installing frontend dependencies..."
    Push-Location $FrontendDir
    npm install
    Pop-Location
}

Write-Host "Starting backend on http://127.0.0.1:8000 ..."
$Backend = Start-Process `
    -FilePath $Python `
    -ArgumentList @("-m", "uvicorn", "api.app:app", "--host", "127.0.0.1", "--port", "8000") `
    -WorkingDirectory $Root `
    -RedirectStandardOutput (Join-Path $LogDir "backend.out.log") `
    -RedirectStandardError (Join-Path $LogDir "backend.err.log") `
    -PassThru `
    -WindowStyle Hidden
$Backend.Id | Set-Content -Encoding ASCII -Path $BackendPidPath

Write-Host "Starting frontend on http://127.0.0.1:5173 ..."
$Frontend = Start-Process `
    -FilePath "npm.cmd" `
    -ArgumentList @("run", "dev") `
    -WorkingDirectory $FrontendDir `
    -RedirectStandardOutput (Join-Path $LogDir "frontend.out.log") `
    -RedirectStandardError (Join-Path $LogDir "frontend.err.log") `
    -PassThru `
    -WindowStyle Hidden
$Frontend.Id | Set-Content -Encoding ASCII -Path $FrontendPidPath

$BackendReady = $false
for ($i = 0; $i -lt 40; $i++) {
    try {
        $health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/health" -Method Get -TimeoutSec 2
        if ($health.status -eq "ok") {
            $BackendReady = $true
            break
        }
    } catch {
        Start-Sleep -Milliseconds 500
    }
}

$FrontendReady = $false
for ($i = 0; $i -lt 40; $i++) {
    try {
        $response = Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:5173" -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            $FrontendReady = $true
            break
        }
    } catch {
        Start-Sleep -Milliseconds 500
    }
}

Write-Host ""
if ($BackendReady -and $FrontendReady) {
    Write-Host "Research Assistant is ready."
    Write-Host "Frontend: http://127.0.0.1:5173"
    Write-Host "Backend:  http://127.0.0.1:8000"
    Start-Process "http://127.0.0.1:5173"
} else {
    Write-Host "Startup finished, but one service did not pass readiness checks."
    Write-Host "Check logs in: $LogDir"
}
