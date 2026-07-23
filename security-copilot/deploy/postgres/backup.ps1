param(
    [string]$DatabaseUrl = $env:DATABASE_URL,
    [string]$OutputDirectory = "./backups"
)

if ([string]::IsNullOrWhiteSpace($DatabaseUrl)) { throw "DATABASE_URL is required" }
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
pg_dump $DatabaseUrl --format=custom --file (Join-Path $OutputDirectory "security-copilot-$timestamp.dump")
if ($LASTEXITCODE -ne 0) { throw "pg_dump failed" }

