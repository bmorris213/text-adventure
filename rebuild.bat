@echo off
echo Cleaning previous builds...
rd /s /q build
rd /s /q dist
del main.spec

echo Rebuilding executable...
pyinstaller --onefile src\main.py

echo Done.
pause