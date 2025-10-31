#!/bin/bash

# Quick setup script for the project

echo "🚀 DevSecOps AI - Quick Setup"
echo "=============================="

# Check Python version
echo "Checking Python version..."
python --version

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
echo "Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env with your API keys"
else
    echo "ℹ️  .env file already exists"
fi

# Initialize project
echo "Initializing project structure..."
python main.py init

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run: python main.py check-config"
echo "3. Try: python main.py scan --target ./sample_app"
echo ""
echo "For more information, see README.md"
