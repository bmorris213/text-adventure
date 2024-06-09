#!/bin/bash

echo "Cleaning previous builds..."
rm -rf build dist main.sepc

echo "Rebuilding executable..."
pyinstaller --onefile src/main.py

echo "Done."