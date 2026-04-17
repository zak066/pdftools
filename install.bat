@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "VENV=%SCRIPT_DIR%venv"
set "RUN_BAT=%SCRIPT_DIR%run.bat"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\PDF Tools.lnk"

echo ========================================
echo PDF Tools - Installazione
echo ========================================

if not exist "%VENV%\Scripts\python.exe" (
    echo [1/2] Creazione virtual environment...
    python -m venv "%VENV%"
    call "%VENV%\Scripts\pip.exe" install -r requirements.txt --quiet
    echo        Fatto
) else (
    echo [1/2] Virtual environment gia esistente, skip
)

if not exist "%START_MENU%" (
    echo [2/2] Creazione collegamento Start Menu...

    powershell -Command ^
    "$ws = New-Object -ComObject WScript.Shell; " ^
    "$s = $ws.CreateShortcut('%START_MENU%'); " ^
    "$s.TargetPath = '%RUN_BAT%'; " ^
    "$s.WorkingDirectory = '%SCRIPT_DIR%'; " ^
    "$s.Description = 'PDF Tools'; " ^
    "$s.Save()"

    echo        Desktop entry creato
) else (
    echo [2/2] Collegamento gia esistente, skip
)

echo ========================================
echo Installazione completata!
echo Esegui: run.bat
echo ========================================

pause