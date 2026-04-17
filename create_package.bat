@echo off
setlocal enabledelayedexpansion

echo ========================================
echo PDF Tools - Creazione Pacchetto
echo ========================================
echo.

set VERSION=1.0.1
set PACKAGE_NAME=pdftools_v%VERSION%
set TEMP_DIR=%PACKAGE_NAME%_temp

REM Pulisci vecchi pacchetti
if exist "%PACKAGE_NAME%.zip" (
    echo Rimozione vecchio pacchetto...
    del /q "%PACKAGE_NAME%.zip"
)
if exist "%TEMP_DIR%" (
    echo Pulizia cartella temporanea...
    rmdir /s /q "%TEMP_DIR%"
)

REM Crea struttura temporanea
echo Creazione struttura pacchetto...
mkdir "%TEMP_DIR%\%PACKAGE_NAME%"
mkdir "%TEMP_DIR%\%PACKAGE_NAME%\gui\dialogs"
mkdir "%TEMP_DIR%\%PACKAGE_NAME%\gui\widgets"
mkdir "%TEMP_DIR%\%PACKAGE_NAME%\core"
mkdir "%TEMP_DIR%\%PACKAGE_NAME%\converters"
mkdir "%TEMP_DIR%\%PACKAGE_NAME%\utils"

REM Copia file root
echo Copia file...
copy main.py "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy app.py "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy config.py "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy requirements.txt "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy install.bat "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy run.bat "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy install.sh "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy run.sh "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy icon.ico "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy README.md "%TEMP_DIR%\%PACKAGE_NAME%\" >nul
copy .gitignore "%TEMP_DIR%\%PACKAGE_NAME%\" >nul

REM Copia gui
copy gui\__init__.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\" >nul
copy gui\main_window.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\" >nul
copy gui\theme.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\" >nul
copy gui\dialogs\__init__.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\dialogs\" >nul
copy gui\dialogs\create_dialog.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\dialogs\" >nul
copy gui\dialogs\merge_dialog.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\dialogs\" >nul
copy gui\dialogs\extract_dialog.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\dialogs\" >nul
copy gui\widgets\__init__.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\widgets\" >nul
copy gui\widgets\pdf_sidebar.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\widgets\" >nul
copy gui\widgets\pdf_preview.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\widgets\" >nul
copy gui\widgets\drop_area.py "%TEMP_DIR%\%PACKAGE_NAME%\gui\widgets\" >nul

REM Copia core
copy core\__init__.py "%TEMP_DIR%\%PACKAGE_NAME%\core\" >nul
copy core\pdf_merge.py "%TEMP_DIR%\%PACKAGE_NAME%\core\" >nul
copy core\pdf_extract.py "%TEMP_DIR%\%PACKAGE_NAME%\core\" >nul
copy core\pdf_split.py "%TEMP_DIR%\%PACKAGE_NAME%\core\" >nul
copy core\pdf_edit.py "%TEMP_DIR%\%PACKAGE_NAME%\core\" >nul

REM Copia converters
copy converters\__init__.py "%TEMP_DIR%\%PACKAGE_NAME%\converters\" >nul
copy converters\txt_to_pdf.py "%TEMP_DIR%\%PACKAGE_NAME%\converters\" >nul
copy converters\docx_to_pdf.py "%TEMP_DIR%\%PACKAGE_NAME%\converters\" >nul
copy converters\odt_to_pdf.py "%TEMP_DIR%\%PACKAGE_NAME%\converters\" >nul
copy converters\xlsx_to_pdf.py "%TEMP_DIR%\%PACKAGE_NAME%\converters\" >nul
copy converters\csv_to_pdf.py "%TEMP_DIR%\%PACKAGE_NAME%\converters\" >nul

REM Copia utils
copy utils\__init__.py "%TEMP_DIR%\%PACKAGE_NAME%\utils\" >nul
copy utils\logger.py "%TEMP_DIR%\%PACKAGE_NAME%\utils\" >nul
copy utils\exceptions.py "%TEMP_DIR%\%PACKAGE_NAME%\utils\" >nul
copy utils\pdf_utils.py "%TEMP_DIR%\%PACKAGE_NAME%\utils\" >nul
copy utils\updater.py "%TEMP_DIR%\%PACKAGE_NAME%\utils\" >nul

REM Comprimi
echo.
echo Compressione in corso...
powershell -Command "Compress-Archive -Path '%TEMP_DIR%\%PACKAGE_NAME%\*' -DestinationPath '%PACKAGE_NAME%.zip' -CompressionLevel Optimal"

if exist "%PACKAGE_NAME%.zip" (
    for %%A in ("%PACKAGE_NAME%.zip") do (
        set size=%%~zA
        set /a sizeKB=!size!/1024
        echo.
        echo ========================================
        echo Pacchetto creato con successo!
        echo File: %PACKAGE_NAME%.zip
        echo Dimensione: !sizeKB! KB
        echo ========================================
    )
) else (
    echo.
    echo ========================================
    echo ERRORE: Creazione pacchetto fallita
    echo ========================================
)

REM Pulisci
if exist "%TEMP_DIR%" (
    rmdir /s /q "%TEMP_DIR%"
)

echo.
pause
