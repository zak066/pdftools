@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "VENV=%SCRIPT_DIR%venv"

if not exist "%VENV%\Scripts\python.exe" (
    echo Prima esegui: install.bat
    pause
    exit /b 1
)

call "%VENV%\Scripts\python.exe" "%SCRIPT_DIR%main.py"