# Contributing to DevSecOps AI

We welcome contributions to the DevSecOps AI project!

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs
- Include detailed steps to reproduce
- Provide sample data if applicable

### Submitting Changes
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions focused and small

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test
pytest tests/unit/test_parser.py
```

### Documentation
- Update README.md for new features
- Add docstrings to new modules
- Create examples for complex features

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/devsecopsai.git
cd devsecopsai

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest
```

## Areas for Contribution

- [ ] Additional security scanner integrations
- [ ] More LLM provider support
- [ ] Enhanced evaluation metrics
- [ ] Better prompt templates
- [ ] Documentation improvements
- [ ] Bug fixes
- [ ] Performance optimizations

Thank you for contributing!
