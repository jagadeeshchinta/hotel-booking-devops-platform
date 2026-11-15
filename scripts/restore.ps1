# =============================================================================
# Automated Database Restore Script (Windows PowerShell)
# Restores a PostgreSQL .sql dump into running container and verifies row counts
# =============================================================================
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$BackupFile,
    [string]$ContainerName = "hotel-booking-db"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $BackupFile)) {
    Write-Error "Backup file not found: $BackupFile"
    exit 1
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir

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

Write-Host "[INFO] Restoring '$BackupFile' into container '$ContainerName' ($pgDb)..." -ForegroundColor Cyan
Get-Content $BackupFile -Raw | docker exec -i -e PGPASSWORD="$pgPass" $ContainerName psql -U $pgUser -d $pgDb -v ON_ERROR_STOP=1

Write-Host "[INFO] Running recovery verification query..." -ForegroundColor Cyan
$verifySql = "SELECT 'rooms' AS table_name, COUNT(*) AS count FROM rooms UNION ALL SELECT 'reservations' AS table_name, COUNT(*) AS count FROM reservations;"
docker exec -e PGPASSWORD="$pgPass" $ContainerName psql -U $pgUser -d $pgDb -c "$verifySql"

Write-Host "[SUCCESS] Database restoration and verification completed successfully!" -ForegroundColor Green

