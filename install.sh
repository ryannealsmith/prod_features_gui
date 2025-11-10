#!/bin/bash

echo "=========================================="
echo "Product Features GUI - Installation"
echo "=========================================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Error: Homebrew is not installed."
    echo "Please install Homebrew first: https://brew.sh"
    exit 1
fi

echo "Installing Python with Tkinter support..."
brew install python-tk@3.13

if [ $? -ne 0 ]; then
    echo "Error: Failed to install python-tk"
    exit 1
fi

echo ""
echo "Creating virtual environment..."
/opt/homebrew/bin/python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install Python packages"
    exit 1
fi

echo ""
echo "Checking for Excel file..."
if [ ! -f "Product Engineering Canonical Product Features.xlsx" ]; then
    echo "Warning: Excel file not found!"
    echo "Please ensure 'Product Engineering Canonical Product Features.xlsx' is in this directory."
    echo ""
    read -p "Do you want to continue without importing data? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "Importing data from Excel..."
    python import_data.py
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to import data"
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source .venv/bin/activate"
echo "  python app.py"
echo ""
