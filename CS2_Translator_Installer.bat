@echo off
title CS2 Translator - Auto Installer by Sl0w
echo ================================================
echo    CS2 TRANSLATOR - AUTO INSTALLER by Sl0w
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python from: https://python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install Dependencies
echo [INFO] Installing required packages...
python -m pip install --upgrade pip
python -m pip install mss pillow pytesseract psutil deep-translator keyboard numpy

if %errorlevel% neq 0 (
    echo [ERROR] Package installation failed!
    pause
    exit /b 1
)

echo [OK] All packages installed
echo.

REM Check Tesseract
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [OK] Tesseract OCR found
) else (
    echo [WARNING] Tesseract OCR not found!
    echo Please install Tesseract from:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
)

echo ================================================
echo Installation complete!
echo.
echo USAGE:
echo 1. Start CS2
echo 2. Run CS2_Translator_by_Sl0w.exe
echo 3. Press F7 for Auto-Region
echo 4. Press F10 to Start
echo.
echo HOTKEYS:
echo F7/Num2 = Auto-Region
echo F9/Num1 = Manual Region
echo F10/Num0 = Start/Stop
echo F11 = Hide/Show
echo F12 = Quit
echo ================================================
pause
