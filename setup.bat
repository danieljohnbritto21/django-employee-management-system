@echo off
REM Employee Management System - Setup Script
REM This script automates the setup process

setlocal enabledelayedexpansion

echo.
echo ============================================
echo Employee Management System - Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.x from https://www.python.org
    pause
    exit /b 1
)

echo [1/6] Python found: 
python --version

REM Activate virtual environment
echo.
echo [2/6] Activating virtual environment...
call .\env\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Could not activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!

REM Install requirements
echo.
echo [3/6] Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)
echo Requirements installed!

REM Make migrations
echo.
echo [4/6] Making migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo Error: Failed to make migrations
    pause
    exit /b 1
)
echo Migrations created!

REM Migrate database
echo.
echo [5/6] Applying migrations...
python manage.py migrate
if errorlevel 1 (
    echo Error: Failed to apply migrations
    pause
    exit /b 1
)
echo Database migrated!

REM Collect static files
echo.
echo [6/6] Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo Error: Failed to collect static files
    pause
    exit /b 1
)
echo Static files collected!

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Create superuser: python manage.py createsuperuser
echo 2. Run server: python manage.py runserver
echo 3. Visit: http://localhost:8000
echo.
pause
