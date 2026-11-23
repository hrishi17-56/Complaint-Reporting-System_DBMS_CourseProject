@echo off
echo.
echo ========================================
echo   ComplaintDesk - Setup & Run
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
cd backend
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/3] Dependencies installed successfully!
echo.
echo [3/3] Starting server...
echo.
echo ========================================
echo Server is starting on http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
