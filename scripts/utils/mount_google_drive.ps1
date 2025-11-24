# Script to mount Google Drive as G: drive on Windows
# Using rclone

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Mount Google Drive as G: Drive" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if rclone is installed
$rcloneInstalled = Get-Command rclone -ErrorAction SilentlyContinue

if (-not $rcloneInstalled) {
    Write-Host "`nrclone is not installed. Installing rclone..." -ForegroundColor Yellow
    
    # Download and install rclone
    $rcloneUrl = "https://downloads.rclone.org/rclone-current-windows-amd64.zip"
    $downloadPath = "$env:TEMP\rclone.zip"
    $extractPath = "$env:TEMP\rclone"
    
    Write-Host "Downloading rclone..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $rcloneUrl -OutFile $downloadPath
    
    Write-Host "Extracting rclone..." -ForegroundColor Yellow
    Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force
    
    # Move rclone.exe to a permanent location
    $rclonePath = "C:\Program Files\rclone"
    if (-not (Test-Path $rclonePath)) {
        New-Item -Path $rclonePath -ItemType Directory -Force | Out-Null
    }
    
    Copy-Item "$extractPath\rclone-*\rclone.exe" "$rclonePath\rclone.exe" -Force
    
    # Add to PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($currentPath -notlike "*$rclonePath*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$rclonePath", "Machine")
    }
    
    # Update current session PATH
    $env:Path += ";$rclonePath"
    
    Write-Host "rclone installed successfully!" -ForegroundColor Green
    
    # Clean up
    Remove-Item $downloadPath -Force
    Remove-Item $extractPath -Recurse -Force
}

Write-Host "`nChecking rclone configuration..." -ForegroundColor Yellow

# Check if Google Drive remote is configured
$remoteExists = rclone listremotes | Select-String -Pattern "^gdrive:"

if (-not $remoteExists) {
    Write-Host "`nGoogle Drive remote not configured." -ForegroundColor Yellow
    Write-Host "Please run the following command to configure:" -ForegroundColor Yellow
    Write-Host "  rclone config" -ForegroundColor Cyan
    Write-Host "`nFollow these steps:" -ForegroundColor Yellow
    Write-Host "  1. Choose 'n' for new remote" -ForegroundColor White
    Write-Host "  2. Name it: gdrive" -ForegroundColor White
    Write-Host "  3. Choose Google Drive (number 15 or similar)" -ForegroundColor White
    Write-Host "  4. Leave client_id and client_secret blank (press Enter)" -ForegroundColor White
    Write-Host "  5. Choose scope: 1 (Full access)" -ForegroundColor White
    Write-Host "  6. Leave root_folder_id blank" -ForegroundColor White
    Write-Host "  7. Leave service_account_file blank" -ForegroundColor White
    Write-Host "  8. Choose 'n' for advanced config" -ForegroundColor White
    Write-Host "  9. Choose 'y' to auto config (opens browser)" -ForegroundColor White
    Write-Host "  10. Authorize in browser" -ForegroundColor White
    Write-Host "  11. Choose 'y' to confirm" -ForegroundColor White
    Write-Host "  12. Choose 'q' to quit config" -ForegroundColor White
    Write-Host "`nAfter configuration, run this script again." -ForegroundColor Yellow
    
    # Ask if user wants to configure now
    $configure = Read-Host "`nDo you want to configure now? (y/n)"
    if ($configure -eq "y") {
        rclone config
    }
    exit
}

Write-Host "Google Drive remote found!" -ForegroundColor Green

# Check if G: drive is already mounted
if (Test-Path "G:\") {
    Write-Host "`nG: drive is already in use." -ForegroundColor Yellow
    $unmount = Read-Host "Do you want to unmount it first? (y/n)"
    if ($unmount -eq "y") {
        Write-Host "Unmounting G: drive..." -ForegroundColor Yellow
        Stop-Process -Name rclone -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    } else {
        Write-Host "Exiting..." -ForegroundColor Red
        exit
    }
}

# Mount Google Drive as G:
Write-Host "`nMounting Google Drive as G: drive..." -ForegroundColor Yellow
Write-Host "This will run in the background. Close PowerShell to unmount." -ForegroundColor Yellow

# Create mount point
if (-not (Test-Path "G:\")) {
    Write-Host "Creating G: drive..." -ForegroundColor Yellow
}

# Mount with rclone
$mountCommand = "rclone mount gdrive: G: --vfs-cache-mode writes --vfs-cache-max-age 100h --no-console"

Write-Host "`nExecuting: $mountCommand" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop mounting" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Start rclone mount in background
Start-Process -FilePath "rclone" -ArgumentList "mount", "gdrive:", "G:", "--vfs-cache-mode", "writes", "--vfs-cache-max-age", "100h" -WindowStyle Hidden

Start-Sleep -Seconds 5

# Verify mount
if (Test-Path "G:\") {
    Write-Host "SUCCESS! Google Drive is now mounted as G: drive" -ForegroundColor Green
    Write-Host "`nYou can now access your Google Drive files at G:\" -ForegroundColor Green
    Write-Host "`nTo unmount, close this PowerShell window or run:" -ForegroundColor Yellow
    Write-Host "  Stop-Process -Name rclone -Force" -ForegroundColor Cyan
    
    # Keep the window open
    Write-Host "`nPress any key to open G: drive in Explorer..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    Start-Process "explorer.exe" "G:\"
} else {
    Write-Host "ERROR: Failed to mount G: drive" -ForegroundColor Red
    Write-Host "Please check rclone logs for details" -ForegroundColor Red
}
