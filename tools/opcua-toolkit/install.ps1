$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

Write-Host ""
Write-Host "==============================================="
Write-Host " Siemens OPC UA - Read-only Toolkit Installer"
Write-Host "==============================================="
Write-Host ""

$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) {
    throw "Python launcher 'py' was not found. Install Python 3.10+ from python.org and enable the Python Launcher, then run this installer again."
}

$pythonVersion = & py -3 --version 2>&1
Write-Host "Python detected: $pythonVersion"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Creating isolated virtual environment..."
    & py -3 -m venv .venv
}

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
Write-Host "Updating pip in the virtual environment..."
& $venvPython -m pip install --upgrade pip
Write-Host "Installing toolkit dependencies..."
& $venvPython -m pip install -r requirements.txt

if (-not (Test-Path ".\config.json")) {
    Copy-Item ".\config.example.json" ".\config.json"
    Write-Host "Created config.json from defaults."
}

New-Item -ItemType Directory -Force -Path ".\certificates" | Out-Null
Write-Host ""
Write-Host "Installation complete."
Write-Host "Start the toolkit with: .\run-toolkit.ps1"
Write-Host "No PLC settings or PLC values were changed."
