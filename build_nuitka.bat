@echo off
setlocal enabledelayedexpansion
echo ========================================
echo PDF Tools - Build con Nuitka (Fast)
echo ========================================
echo.

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRORE: Impossibile attivare il virtual environment
    pause
    exit /b 1
)

echo [1/2] Verifica dipendenze...
python -c "import nuitka; print('Nuitka versione:', nuitka.__version__)" 2>nul
if errorlevel 1 (
    pip install nuitka
    if errorlevel 1 ( pause & exit /b 1 )
)

REM Installa ordered-set per compilazione piu' veloce (consigliato da Nuitka)
python -c "import ordered_set" 2>nul
if errorlevel 1 (
    echo Installazione ordered-set ^(ottimizzazione Nuitka^)...
    pip install ordered-set -q
)
echo.

set OUTPUT_DIR=dist\nuitka
if exist "%OUTPUT_DIR%\main.dist" rmdir /s /q "%OUTPUT_DIR%\main.dist"
if exist "%OUTPUT_DIR%\main.build" rmdir /s /q "%OUTPUT_DIR%\main.build"

REM === CACHE: directory persistente tra le build ===
set NUITKA_CACHE_DIR=%LOCALAPPDATA%\Nuitka\pdf_tools_cache

REM === AUTO-DOWNLOAD: accetta automaticamente ccache, MinGW64, ecc. ===
set NUITKA_AUTOINSTALL=yes

echo [2/2] Build in corso...
echo Cache dir: %NUITKA_CACHE_DIR%
echo.

REM Core FISICI (non logici) per evitare thrashing da hyperthreading
for /f "tokens=2 delims==" %%A in ('wmic cpu get NumberOfCores /value 2^>nul') do set CORES=%%A
if not defined CORES set CORES=4
echo CPU cores fisici: %CORES%
echo.

python -m nuitka ^
    --assume-yes-for-downloads ^
    --standalone ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=icon.ico ^
    --output-dir=%OUTPUT_DIR% ^
    --windows-company-name="PDF Tools" ^
    --windows-product-name="PDF Tools" ^
    --windows-file-version="1.0.0" ^
    --windows-product-version="1.0.0" ^
    --windows-file-description="PDF Tools - Manipolazione PDF" ^
    --enable-plugin=pyside6 ^
    --jobs=%CORES% ^
    --include-package=converters ^
    --include-package=core ^
    --include-package=gui ^
    --include-package=utils ^
    --nofollow-import-to=fitz ^
    --nofollow-import-to=pymupdf ^
    --nofollow-import-to=numpy ^
    --nofollow-import-to=lxml ^
    --nofollow-import-to=PIL ^
    --nofollow-import-to=matplotlib ^
    --nofollow-import-to=scipy ^
    --nofollow-import-to=pandas ^
    --nofollow-import-to=test ^
    --nofollow-import-to=unittest ^
    --noinclude-setuptools-mode=nofollow ^
    --noinclude-pytest-mode=nofollow ^
    --noinclude-IPython-mode=nofollow ^
    --python-flag=no_docstrings ^
    --python-flag=no_asserts ^
    main.py

if exist "%OUTPUT_DIR%\main.dist\main.exe" (
    echo.
    echo ========================================
    echo Build completato con successo!
    echo Output: %OUTPUT_DIR%\main.dist\
    for %%A in ("%OUTPUT_DIR%\main.dist\main.exe") do (
        set size=%%~zA
        set /a sizeMB=!size!/1048576
        echo Dimensione exe: !sizeMB! MB
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