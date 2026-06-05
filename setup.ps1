# Employee Management System - PowerShell Setup Script

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Employee Management System - Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[1/6] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.x from https://www.python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host ""
Write-Host "[2/6] Activating virtual environment..." -ForegroundColor Cyan
& .\env\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Could not activate virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Virtual environment activated!" -ForegroundColor Green

# Install requirements
Write-Host ""
Write-Host "[3/6] Installing requirements..." -ForegroundColor Cyan
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install requirements" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Requirements installed!" -ForegroundColor Green

# Make migrations
Write-Host ""
Write-Host "[4/6] Making migrations..." -ForegroundColor Cyan
python manage.py makemigrations
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to make migrations" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Migrations created!" -ForegroundColor Green

# Migrate database
Write-Host ""
Write-Host "[5/6] Applying migrations..." -ForegroundColor Cyan
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to apply migrations" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Database migrated!" -ForegroundColor Green

# Collect static files
Write-Host ""
Write-Host "[6/6] Collecting static files..." -ForegroundColor Cyan
python manage.py collectstatic --noinput
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to collect static files" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Static files collected!" -ForegroundColor Green

# Success message
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create superuser: python manage.py createsuperuser" -ForegroundColor White
Write-Host "2. Run server: python manage.py runserver" -ForegroundColor White
Write-Host "3. Visit: http://localhost:8000" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"
