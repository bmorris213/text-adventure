@echo off
REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Run the Python script
python path\to\your\script\main.py
pause