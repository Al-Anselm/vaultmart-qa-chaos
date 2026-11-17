# ==============================================================================
# INFT 2700 — Browser Automation, UI Chaos & AI Red-Teaming Setup Script
# ==============================================================================
# Reminder: If PowerShell blocks script execution, run:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ⚡ INFT 2700: VaultMart Browser QA & Red-Team Lab Setup  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

function Find-RealPython {
    # 1. Check standard user and system install paths first (bypasses Windows Store stub!)
    $candidates = @()
    $candidates += Get-ChildItem -Path "$env:LOCALAPPDATA\Programs\Python\Python3*\python.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending
    $candidates += Get-ChildItem -Path "C:\Program Files\Python3*\python.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending
    $candidates += Get-ChildItem -Path "C:\Python3*\python.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending

    foreach ($c in $candidates) {
        if ($c.FullName -notlike "*WindowsApps*") {
            return $c.FullName
        }
    }

    # 2. Check if 'python' in PATH is real (not the Microsoft Store alias stub)
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd -and ($cmd.Source -notlike "*WindowsApps*")) {
        $ver = & $cmd.Source --version 2>&1
        if ($LASTEXITCODE -eq 0 -and ($ver -match "Python 3")) {
            return $cmd.Source
        }
    }

    return $null
}

# 1. Check for Real Python (ignoring the WindowsApps Microsoft Store stub)
$pythonExe = Find-RealPython

if (-not $pythonExe) {
    Write-Host "[1/5] Real Python not found (only Windows Store stub present). Installing Python 3.12 via winget..." -ForegroundColor Yellow
    winget install Python.Python.3.12 --scope user --accept-source-agreements --accept-package-agreements
    # Refresh PATH in current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")
    $pythonExe = Find-RealPython
}

if (-not $pythonExe) {
    Write-Host "[ERROR] Could not locate python.exe after winget install. Please close and reopen PowerShell, then run .\setup.ps1 again." -ForegroundColor Red
    exit 1
}

Write-Host "[1/5] Python detected: $(& $pythonExe --version) ($pythonExe)" -ForegroundColor Green

# 2. Create Virtual Environment (remove broken .venv if it was incomplete)
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    if (Test-Path ".venv") {
        Remove-Item -Recurse -Force ".venv"
    }
    Write-Host "[2/5] Creating local Python virtual environment (.venv)..." -ForegroundColor Yellow
    & $pythonExe -m venv .venv
} else {
    Write-Host "[2/5] Virtual environment (.venv) already exists." -ForegroundColor Green
}

# Activate .venv in current session
& .\.venv\Scripts\Activate.ps1

# 3. Install Python dependencies (Flask, Pytest, Playwright)
Write-Host "[3/5] Installing Flask, Pytest, and Playwright packages..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 4. Install Playwright's isolated Chromium browser (No Chrome installation needed!)
Write-Host "[4/5] Downloading Playwright Chromium browser binary..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe -m playwright install chromium

# 5. Start the Target Web Application (Docker Compose or Native Fallback)
Write-Host "[5/5] Starting VaultMart Target Web Application on port 8000..." -ForegroundColor Yellow
$dockerRunning = $false
if (Get-Command docker -ErrorAction SilentlyContinue) {
    docker info *> $null
    if ($LASTEXITCODE -eq 0) {
        $dockerRunning = $true
    }
}

if ($dockerRunning) {
    Write-Host "      -> Docker is running! Launching via 'docker compose up -d'..." -ForegroundColor Green
    docker compose up -d --build
} else {
    Write-Host "      -> Docker not running/installed. Launching native Python server in background window..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '.\.venv\Scripts\python.exe' app\server.py"
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " ✅ SETUP COMPLETE! VaultMart is live at:" -ForegroundColor Green
Write-Host "    http://localhost:8000" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Try these commands next:" -ForegroundColor Cyan
Write-Host "  0. Activate your venv in this window:  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "  1. Record a test interactively:        playwright codegen http://localhost:8000"
Write-Host "  2. Run tests (fast headless):          pytest -v"
Write-Host "  3. Watch browser live (headed):        pytest -v --headed"
Write-Host "  4. Watch in SLOW MOTION:               pytest -v --headed --slowmo 800"
Write-Host ""
