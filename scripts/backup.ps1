# =============================================================================
# Automated Database Backup Script (Windows PowerShell)
# Dumps PostgreSQL database from running container into backups/
# =============================================================================
[CmdletBinding()]
param(
    [string]$ContainerName = "hotel-booking-db"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir
$backupDir = Join-Path $rootDir "backups"

if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}

$pgUser = "postgres"
$pgPass = "postgres"
$pgDb = "hotel_booking"

# Load credentials from .env if present
$envFile = Join-Path $rootDir ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
            $parts = $line.Split("=", 2)
            $name = $parts[0].Trim()
            $val = $parts[1].Trim()
            if ($name -eq "POSTGRES_USER") { $pgUser = $val }
            if ($name -eq "POSTGRES_PASSWORD") { $pgPass = $val }
            if ($name -eq "POSTGRES_DB") { $pgDb = $val }
        }
    }
}

Write-Host "[INFO] Checking if container '$ContainerName' is active..." -ForegroundColor Cyan
$running = docker ps --format '{{.Names}}' | Select-String -Pattern "^$ContainerName$"
if (-not $running) {
    Write-Error "Database container '$ContainerName' is not running."
    exit 1
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = Join-Path $backupDir "hotel_booking_$timestamp.sql"

Write-Host "[INFO] Creating database backup for '$pgDb'..." -ForegroundColor Cyan
docker exec -e PGPASSWORD="$pgPass" $ContainerName pg_dump -U $pgUser -d $pgDb --clean --if-exists | Out-File -FilePath $backupFile -Encoding utf8

if (-not (Test-Path $backupFile) -or (Get-Item $backupFile).Length -eq 0) {
    Write-Error "Backup failed or generated an empty file: $backupFile"
    if (Test-Path $backupFile) { Remove-Item $backupFile -Force }
    exit 1
}

$fileItem = Get-Item $backupFile
$sizeKb = [math]::Round($fileItem.Length / 1KB, 2)
Write-Host "[SUCCESS] Database backup created successfully!" -ForegroundColor Green
Write-Host "  File Path: $backupFile" -ForegroundColor Green
Write-Host "  File Size: $sizeKb KB ($($fileItem.Length) bytes)" -ForegroundColor Green

