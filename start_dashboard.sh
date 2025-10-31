#!/bin/bash

# Dashboard Launch Script
# Starts the DevSecOps AI Dashboard web interface

set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║           DevSecOps AI Dashboard - Starting...                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "✓ Activating virtual environment..."
    source venv/bin/activate
fi

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask not found. Installing..."
    pip install Flask==3.0.0
fi

# Create directories if they don't exist
mkdir -p data/reports
mkdir -p output/generated_policies
mkdir -p output/evaluation_results
mkdir -p logs

echo ""
echo "✓ All dependencies ready"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Dashboard Starting on http://localhost:5000"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📊 View your CI/CD pipeline results in real-time"
echo "  🔍 Monitor security vulnerabilities"
echo "  📄 Track generated policies"
echo "  📈 Analyze quality metrics"
echo ""
echo "  Press Ctrl+C to stop the server"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the dashboard
cd dashboard
python app.py
