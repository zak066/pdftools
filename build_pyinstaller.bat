@echo off
setlocal enabledelayedexpansion
echo ========================================
echo PDF Tools - Build con PyInstaller
echo ========================================
echo.

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRORE: Impossibile attivare il virtual environment
    pause
    exit /b 1
)

echo [1/2] Verifica PyInstaller...
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

set OUTPUT_DIR=dist\pyinstaller
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
if exist "*.spec" del /q *.spec

echo [2/2] Build in corso... (2-5 minuti)
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --name=PDFTools ^
    --distpath=%OUTPUT_DIR% ^
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

if exist "%OUTPUT_DIR%\PDFTools.exe" (
    echo.
    echo ========================================
    echo Build completato con successo!
    echo Output: %OUTPUT_DIR%\PDFTools.exe
    for %%A in ("%OUTPUT_DIR%\PDFTools.exe") do (
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
