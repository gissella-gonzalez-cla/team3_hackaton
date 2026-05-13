# Windows Setup Script for ML Doc Intelligence Promotion Tool
# PowerShell equivalent of setup.sh

$ErrorActionPreference = "Stop"

# Set the Python version
$PYTHON_VERSION = "3.12.3"

Write-Host "Setting up ML Doc Intelligence Promotion Tool on Windows..." -ForegroundColor Green

# Check if Python is installed
Write-Host "`nChecking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install Python $PYTHON_VERSION from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check if Azure CLI is installed
Write-Host "`nChecking Azure CLI installation..." -ForegroundColor Yellow
try {
    $azVersion = az --version 2>&1 | Select-Object -First 1
    Write-Host "Azure CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "Azure CLI not found. Installing..." -ForegroundColor Yellow
    # Install Azure CLI using MSI
    $azCliUrl = "https://aka.ms/installazurecliwindowsx64"
    $msiPath = "$env:TEMP\AzureCLI.msi"
    Invoke-WebRequest -Uri $azCliUrl -OutFile $msiPath -UseBasicParsing
    Start-Process msiexec.exe -Wait -ArgumentList "/i $msiPath /quiet /norestart"
    Remove-Item $msiPath
    Write-Host "Azure CLI installed successfully" -ForegroundColor Green
}

# Install AzCopy for training data migration
Write-Host "`nInstalling AzCopy..." -ForegroundColor Yellow

# Check if AzCopy is already installed
if (Get-Command azcopy -ErrorAction SilentlyContinue) {
    $azCopyVersion = azcopy --version 2>&1
    Write-Host "AzCopy is already installed: $azCopyVersion" -ForegroundColor Green
} else {
    # Download AzCopy
    $downloadUrl = "https://aka.ms/downloadazcopy-v10-windows"
    $zipPath = "$env:TEMP\azcopy.zip"
    $extractPath = "$env:USERPROFILE\azcopy"
    
    Write-Host "Downloading AzCopy..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath -UseBasicParsing
    
    Write-Host "Extracting AzCopy..." -ForegroundColor Yellow
    # Remove existing directory if it exists
    if (Test-Path $extractPath) {
        Remove-Item $extractPath -Recurse -Force
    }
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
    
    # Find azcopy.exe
    $azCopyExe = Get-ChildItem $extractPath -Recurse -Filter "azcopy.exe" | Select-Object -First 1
    if (-not $azCopyExe) {
        Write-Host "Failed to find azcopy.exe after extraction" -ForegroundColor Red
        exit 1
    }
    
    $azCopyDir = $azCopyExe.Directory.FullName
    
    # Add to current session PATH
    $env:Path += ";$azCopyDir"
    
    # Add to permanent PATH (User level)
    $currentUserPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    if ($currentUserPath -notlike "*$azCopyDir*") {
        [Environment]::SetEnvironmentVariable('Path', "$currentUserPath;$azCopyDir", 'User')
        Write-Host "AzCopy added to PATH" -ForegroundColor Green
    }
    
    # Clean up
    Remove-Item $zipPath -Force
    
    # Verify AzCopy installation
    $azCopyVersion = & "$azCopyDir\azcopy.exe" --version 2>&1
    Write-Host "AzCopy installed successfully: $azCopyVersion" -ForegroundColor Green
    Write-Host "AzCopy location: $azCopyDir" -ForegroundColor Cyan
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nIMPORTANT: Please restart your PowerShell session for PATH changes to take effect." -ForegroundColor Yellow
Write-Host "`nTo verify installations, run:" -ForegroundColor Cyan
Write-Host "  python --version" -ForegroundColor White
Write-Host "  az --version" -ForegroundColor White
Write-Host "  azcopy --version" -ForegroundColor White
