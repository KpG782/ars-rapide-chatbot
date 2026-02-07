@echo off
REM ARS Rapide Setup Script for Windows

echo.
echo ========================================
echo ARS Rapide Chatbot - Phase 1 Setup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo Step 1: Checking Python version...
python --version
echo.

REM Check if .env exists
if not exist .env (
    echo Step 2: Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your GOOGLE_API_KEY
    echo Get your key at: https://makersuite.google.com/app/apikey
    echo.
    pause
) else (
    echo Step 2: .env file already exists
    echo.
)

echo Step 3: Installing dependencies...
echo This may take a few minutes...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit .env and add your GOOGLE_API_KEY
echo   2. Run: python app/main.py
echo.
pause
