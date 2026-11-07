$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "Toolkit not installed. Run install.ps1 first." -ForegroundColor Yellow
    exit 1
}

while ($true) {
    Write-Host ""
    Write-Host "========================================="
    Write-Host " Siemens OPC UA - READ ONLY TOOLKIT"
    Write-Host "========================================="
    Write-Host "1. Generate MES client certificate"
    Write-Host "2. Export PLC server certificate"
    Write-Host "3. Test secure OPC UA connection"
    Write-Host "4. Browse PLC nodes and save plc_nodes.txt"
    Write-Host "5. Open toolkit folder"
    Write-Host "0. Exit"
    $choice = Read-Host "Choose"

    switch ($choice) {
        "1" { & $python ".\generate_client_cert.py"; if ($LASTEXITCODE -ne 0) { Write-Warning "Certificate generation failed." } }
        "2" { & $python ".\export_plc_cert.py"; if ($LASTEXITCODE -ne 0) { Write-Warning "Certificate export failed." } }
        "3" { & $python -u ".\secure_test.py"; if ($LASTEXITCODE -ne 0) { Write-Warning "Secure connection test failed." } }
        "4" { & $python -u ".\browse_plc.py"; if ($LASTEXITCODE -ne 0) { Write-Warning "PLC browse failed." } }
        "5" { Start-Process explorer.exe $PSScriptRoot }
        "0" { break }
        default { Write-Host "Unknown choice." }
    }
    if ($choice -eq "0") { break }
}
