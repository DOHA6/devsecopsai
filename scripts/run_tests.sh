#!/bin/bash

# Run all tests with coverage
echo "Running tests..."
pytest tests/ --cov=. --cov-report=html --cov-report=term

# Check code quality
echo "Checking code quality..."
flake8 .

# Check for security issues
echo "Running security checks..."
bandit -r . -ll

echo "All checks completed!"
