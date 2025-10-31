# Setup Guide

## Prerequisites

Before setting up the DevSecOps AI project, ensure you have:

1. **Python 3.9 or higher**
   ```bash
   python --version
   ```

2. **Git**
   ```bash
   git --version
   ```

3. **Docker** (optional, for running security tools)
   ```bash
   docker --version
   ```

4. **API Keys** (for LLM providers)
   - OpenAI API key
   - Anthropic API key (optional)
   - Hugging Face token (optional)
   - DeepSeek API key (optional)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd devsecopsai
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```bash
# LLM Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
OPENAI_API_KEY=your_key_here

# Security Tools (optional)
SONARQUBE_URL=http://localhost:9000
SONARQUBE_TOKEN=your_token_here
```

### 5. Initialize Project Structure

```bash
python main.py init
```

This creates necessary directories and configuration files.

## Security Tools Setup

### SonarQube (SAST)

**Option 1: Docker**
```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
```

**Option 2: Manual Installation**
Download from https://www.sonarqube.org/downloads/

### OWASP Dependency-Check (SCA)

**Using Docker:**
```bash
docker pull owasp/dependency-check
```

**Manual Installation:**
Download from https://github.com/jeremylong/DependencyCheck/releases

### OWASP ZAP (DAST)

**Using Docker:**
```bash
docker pull owasp/zap2docker-stable
```

**Manual Installation:**
Download from https://www.zaproxy.org/download/

### Bandit (SAST for Python)

Already installed via requirements.txt:
```bash
bandit --version
```

### Safety (SCA for Python)

Already installed via requirements.txt:
```bash
safety --version
```

## LLM Setup

### OpenAI

1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-4
   ```

### Ollama (Local LLMs)

1. Install Ollama: https://ollama.ai/download
2. Pull model:
   ```bash
   ollama pull llama3.3
   ```
3. Configure:
   ```
   LLM_PROVIDER=ollama
   OLLAMA_HOST=http://localhost:11434
   ```

### Hugging Face

1. Get token from https://huggingface.co/settings/tokens
2. Configure:
   ```
   LLM_PROVIDER=huggingface
   HUGGINGFACE_TOKEN=hf_...
   LLM_MODEL=meta-llama/Llama-3.3-70B-Instruct
   ```

## Verification

Test your setup:

```bash
# Check configuration
python main.py check-config

# Run a test scan on sample data
python main.py scan --target ./sample_app --output ./data/reports

# Parse a sample report
python main.py parse --input ./data/reports/sample_bandit_report.json

# Generate a test policy
python main.py generate --input ./data/reports --output ./output/test

# Evaluate policies
python main.py evaluate --policies ./output/test --reference ./data/reference_policies
```

## Troubleshooting

### Issue: Module Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: LLM API Errors

- Verify API keys are correct
- Check API rate limits
- Ensure internet connectivity

### Issue: Security Tool Not Found

- Install tools via Docker
- Or install manually and add to PATH

## Next Steps

1. Read [Pipeline Configuration](pipeline_config.md)
2. Learn about [LLM Integration](llm_integration.md)
3. Review [Policy Templates](policy_templates.md)
4. Understand [Evaluation Methodology](evaluation.md)
