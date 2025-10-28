@echo off
title Building Ultron App Installer...
color 0D

echo ==========================================
echo      ULTRON APP INSTALLER - BUILDER
echo ==========================================
echo.

:: Navigate to the folder this BAT file is in
cd /d "%~dp0"

:: Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python and add it to PATH.
    pause
    exit /b
)

:: Ensure PyInstaller is installed
python -m pip show pyinstaller >nul 2>nul
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    python -m pip install pyinstaller
)

:: Build command
echo [INFO] Building executable...
python -m PyInstaller --onefile --console --icon=ultron_appinstaller.ico --name "Ultron App Installer" main.py

echo.
echo ==========================================
echo Build complete!
echo Output file: dist\Ultron App Installer.exe
echo ==========================================
pause
