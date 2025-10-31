# Sample Python Application for Security Scanning

This is a deliberately vulnerable sample application for testing security scanners.

## Files

- `app.py`: Main Flask application with security issues
- `utils.py`: Utility functions with vulnerabilities
- `requirements.txt`: Dependencies with known vulnerabilities

## Known Vulnerabilities

1. **Flask Debug Mode Enabled** (HIGH)
2. **Unsafe Subprocess Call** (HIGH)
3. **Hardcoded Credentials** (CRITICAL)
4. **SQL Injection Risk** (CRITICAL)
5. **Outdated Dependencies** (MEDIUM-HIGH)

## Usage

**DO NOT deploy this application!** It is intentionally insecure.

Use it for testing:
```bash
python main.py scan --target ./sample_app
```
