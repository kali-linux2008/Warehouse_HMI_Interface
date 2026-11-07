$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$cert = Join-Path $PSScriptRoot "certificates\mes-client.der"
$key = Join-Path $PSScriptRoot "certificates\mes-client-key.pem"
$serverCert = Join-Path $PSScriptRoot "certificates\plc-server.der"
$log = Join-Path $PSScriptRoot "setup-log.txt"

Start-Transcript -Path $log -Append | Out-Null
try {
    Write-Host ""
    Write-Host "STEP 1/4 - Client certificate" -ForegroundColor Cyan
    if (-not (Test-Path $cert) -or -not (Test-Path $key)) {
        & $python ".\generate_client_cert.py"
        if ($LASTEXITCODE -ne 0) { throw "Client certificate generation failed." }
    } else {
        Write-Host "Existing client certificate found; keeping it."
    }

    Write-Host ""
    Write-Host "STEP 2/4 - PLC server certificate" -ForegroundColor Cyan
    & $python ".\export_plc_cert.py"
    if ($LASTEXITCODE -ne 0) { throw "PLC certificate export failed." }

    Write-Host ""
    Write-Host "STEP 3/4 - TIA Portal trust configuration" -ForegroundColor Cyan
    Write-Host "Only the public certificate may be imported:"
    Write-Host $cert -ForegroundColor Yellow
    Write-Host ""
    Write-Host "In TIA Portal, import this .der into the global Certificate Manager"
    Write-Host "and add it to the CPU's OPC UA Trusted clients list."
    Write-Host "Then compile and load the project to PLCSIM if the configuration changed."
    Write-Host "The private key is NOT imported. Never share this file:"
    Write-Host $key -ForegroundColor Red
    Write-Host ""
    Start-Process explorer.exe -ArgumentList ('/select,"' + $cert + '"')
    Read-Host "Press ENTER only after the client certificate is trusted by the simulated CPU"

    Write-Host ""
    Write-Host "STEP 4/4 - Secure connection test and PLC browse" -ForegroundColor Cyan
    if (-not (Test-Path $serverCert)) { throw "PLC server certificate missing." }
    & $python -u ".\secure_test.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Secure connection failed. Check TIA trust, endpoint, CPU configuration and setup-log.txt."
    }
    & $python -u ".\browse_plc.py"
    if ($LASTEXITCODE -ne 0) { throw "PLC browse failed." }

    Write-Host ""
    Write-Host "SUCCESS - plc_nodes.txt has been generated." -ForegroundColor Green
    Write-Host "Log: $log"
    Write-Host "All OPC UA operations in this toolkit are read-only."
}
finally {
    Stop-Transcript | Out-Null
}
