@echo off
setlocal enabledelayedexpansion
echo ========================================
echo PDF Tools - Build con PyInstaller
echo ========================================
echo.

REM Attiva il virtual environment
echo [1/3] Attivazione virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRORE: Impossibile attivare il virtual environment
    pause
    exit /b 1
)

REM Verifica PyInstaller
echo [2/3] Verifica PyInstaller...
python -c "import PyInstaller; print('PyInstaller versione:', PyInstaller.__version__)" 2>nul
if errorlevel 1 (
    echo Installazione PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERRORE: Impossibile installare PyInstaller
        pause
        exit /b 1
    )
)
echo.

REM Pulisci build precedenti
if exist "build" (
    echo Pulizia build precedenti...
    rmdir /s /q build
)
if exist "dist" (
    rmdir /s /q dist
)
if exist "*.spec" (
    del /q *.spec
)

REM Build
echo [3/3] Build in corso... (2-5 minuti)
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --name=PDFTools ^
    --add-data "converters;converters" ^
    --add-data "core;core" ^
    --add-data "gui;gui" ^
    --add-data "utils;utils" ^
    --hidden-import=converters ^
    --hidden-import=converters.txt_to_pdf ^
    --hidden-import=converters.docx_to_pdf ^
    --hidden-import=converters.odt_to_pdf ^
    --hidden-import=converters.xlsx_to_pdf ^
    --hidden-import=converters.csv_to_pdf ^
    --hidden-import=core ^
    --hidden-import=core.pdf_merge ^
    --hidden-import=core.pdf_extract ^
    --hidden-import=core.pdf_split ^
    --hidden-import=core.pdf_edit ^
    --hidden-import=gui ^
    --hidden-import=gui.main_window ^
    --hidden-import=gui.dialogs.create_dialog ^
    --hidden-import=gui.dialogs.merge_dialog ^
    --hidden-import=gui.dialogs.extract_dialog ^
    --hidden-import=gui.widgets.pdf_sidebar ^
    --hidden-import=gui.widgets.pdf_preview ^
    --hidden-import=gui.widgets.drop_area ^
    --hidden-import=utils ^
    --hidden-import=utils.logger ^
    --hidden-import=utils.exceptions ^
    --hidden-import=utils.pdf_utils ^
    --hidden-import=utils.updater ^
    --hidden-import=fitz ^
    --hidden-import=pypdf ^
    --hidden-import=reportlab ^
    --hidden-import=loguru ^
    --hidden-import=PIL ^
    main.py

if exist "dist\PDFTools.exe" (
    echo.
    echo ========================================
    echo Build completato con successo!
    echo Output: dist\PDFTools.exe
    for %%A in ("dist\PDFTools.exe") do (
        set size=%%~zA
        set /a sizeMB=!size!/1048576
        echo Dimensione: !sizeMB! MB
    )
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ERRORE: Build fallito
    echo ========================================
)

echo.
pause
