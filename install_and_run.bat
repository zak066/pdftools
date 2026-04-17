@echo off
setlocal enabledelayedexpansion

echo ========================================
echo PDF Tools - Installazione e Avvio
echo ========================================
echo.

REM 1. Verifica Python
echo [1/4] Verifica Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERRORE: Python non trovato.
    echo Installa Python 3.10+ da: https://www.python.org/downloads/
    echo.
    echo Premi un tasto per aprire il download...
    pause >nul
    start https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo Python trovato: %PYVER%

REM 2. Verifica versione minima (3.10)
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set MAJOR=%%a
    set MINOR=%%b
)
if !MAJOR! LSS 3 (
    echo.
    echo ERRORE: Richiesto Python 3.10+, trovato %PYVER%
    echo Scarica l'ultima versione da: https://www.python.org/downloads/
    pause >nul
    exit /b 1
)
if !MAJOR! EQU 3 (
    if !MINOR! LSS 10 (
        echo.
        echo ERRORE: Richiesto Python 3.10+, trovato %PYVER%
        echo Scarica l'ultima versione da: https://www.python.org/downloads/
        pause >nul
        exit /b 1
    )
)

REM 3. Crea virtual environment
echo.
echo [2/4] Virtual environment...
if not exist "venv" (
    echo Creazione virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ERRORE: Impossibile creare il virtual environment.
        echo Assicurati di avere i permessi di scrittura.
        pause >nul
        exit /b 1
    )
    echo Virtual environment creato.
) else (
    echo Virtual environment gia esistente.
)

REM 4. Installa dipendenze
echo.
echo [3/4] Installazione dipendenze...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo ERRORE: Installazione dipendenze fallita.
    echo Verifica la connessione internet e riprova.
    pause >nul
    exit /b 1
)
echo Dipendenze installate.

REM 5. Avvia l'app
echo.
echo [4/4] Avvio PDF Tools...
echo.
python main.py
