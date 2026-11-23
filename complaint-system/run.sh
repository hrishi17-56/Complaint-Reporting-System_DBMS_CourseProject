#!/bin/bash

echo ""
echo "========================================"
echo "  ComplaintDesk - Setup & Run"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "[1/3] Installing dependencies..."
cd backend
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "[2/3] Dependencies installed successfully!"
echo ""
echo "[3/3] Starting server..."
echo ""
echo "========================================"
echo "Server is starting on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python3 app.py
