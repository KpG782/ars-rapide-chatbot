#!/bin/bash
# ARS Rapide Setup Script for Linux/Mac

echo ""
echo "========================================"
echo "ARS Rapide Chatbot - Phase 1 Setup"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10+ from python.org"
    exit 1
fi

echo "Step 1: Checking Python version..."
python3 --version
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Step 2: Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env and add your GOOGLE_API_KEY"
    echo "Get your key at: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter to continue..."
else
    echo "Step 2: .env file already exists"
    echo ""
fi

echo "Step 3: Installing dependencies..."
echo "This may take a few minutes..."
echo ""
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your GOOGLE_API_KEY"
echo "  2. Run: python3 app/main.py"
echo ""
