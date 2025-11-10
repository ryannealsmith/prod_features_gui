#!/bin/bash

# Product Features Management System Launcher

echo "=========================================="
echo "Product Features Management System"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if database exists
if [ ! -f "product_features.db" ]; then
    echo ""
    echo "Database not found. Importing data from Excel..."
    python import_data.py
    if [ $? -ne 0 ]; then
        echo "Error importing data. Please check that the Excel file exists."
        exit 1
    fi
fi

# Try to run the application
echo ""
echo "Launching application..."
python app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "=========================================="
    echo "Error: Tkinter not available"
    echo "=========================================="
    echo ""
    echo "To fix this on macOS, you can:"
    echo "1. Install Python with tkinter via Homebrew:"
    echo "   brew install python-tk@3.13"
    echo ""
    echo "2. Or use system Python directly:"
    echo "   /usr/bin/python3 app.py"
    echo ""
    echo "For more help, see README.md"
    echo "=========================================="
    exit 1
fi
