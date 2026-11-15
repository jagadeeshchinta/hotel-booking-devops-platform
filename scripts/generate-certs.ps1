# =============================================================================
# Cross-Platform TLS SAN Certificate Generator (Windows PowerShell)
# =============================================================================
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$certsDir = Join-Path (Split-Path -Parent $scriptDir) "certs"

if (-not (Test-Path $certsDir)) {
    New-Item -ItemType Directory -Path $certsDir -Force | Out-Null
}

$keyPath = Join-Path $certsDir "server.key"
$crtPath = Join-Path $certsDir "server.crt"
$cnfPath = Join-Path $certsDir "openssl-san.cnf"

Write-Host "[INFO] Locating OpenSSL executable..." -ForegroundColor Cyan

# Locate OpenSSL in PATH or standard Git installations
$opensslCmd = Get-Command "openssl" -ErrorAction SilentlyContinue
$opensslExe = $null

if ($opensslCmd) {
    $opensslExe = $opensslCmd.Source
} elseif (Test-Path "C:\Program Files\Git\usr\bin\openssl.exe") {
    $opensslExe = "C:\Program Files\Git\usr\bin\openssl.exe"
} elseif (Test-Path "C:\Program Files (x86)\Git\usr\bin\openssl.exe") {
    $opensslExe = "C:\Program Files (x86)\Git\usr\bin\openssl.exe"
}

if ($opensslExe) {
    Write-Host "[INFO] Using OpenSSL at: $opensslExe" -ForegroundColor Cyan

    $cnfContent = @"
[req]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
x509_extensions    = v3_req
prompt             = no

[req_distinguished_name]
C  = US
ST = DevOps
L  = Local
O  = HotelBooking
OU = API
CN = localhost

[req_ext]
subjectAltName = @alt_names

[v3_req]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[alt_names]
DNS.1 = localhost
IP.1  = 127.0.0.1
"@
    Set-Content -Path $cnfPath -Value $cnfContent -Encoding ASCII

    & $opensslExe req -x509 -nodes -days 365 -newkey rsa:2048 `
        -keyout $keyPath `
        -out $crtPath `
        -config $cnfPath

    if (Test-Path $cnfPath) {
        Remove-Item -Path $cnfPath -Force
    }

    Write-Host "[SUCCESS] TLS SAN Certificates successfully generated:" -ForegroundColor Green
    Write-Host "  Private Key: $keyPath" -ForegroundColor Green
    Write-Host "  Certificate: $crtPath" -ForegroundColor Green
} else {
    Write-Error "OpenSSL was not found. Please install OpenSSL or Git for Windows, or run scripts/generate-certs.sh in Git Bash."
}

