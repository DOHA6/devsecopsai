# Quick Start Guide

Get started with DevSecOps AI in 5 minutes!

## Step 1: Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI key
nano .env
```

Add:
```
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
```

## Step 3: Initialize Project

```bash
python main.py init
```

## Step 4: Try the Demo

### Scan Sample Reports
```bash
python main.py parse --input ./data/reports/sample_bandit_report.json
```

### Generate Security Policy
```bash
python main.py generate \
  --input ./data/reports \
  --output ./output/policies \
  --framework NIST_CSF
```

### Evaluate Policy
```bash
python main.py evaluate \
  --policies ./output/policies \
  --reference ./data/reference_policies
```

## Step 5: Scan Your Own Code

```bash
# Scan your application
python main.py scan --target /path/to/your/app

# Generate policies from scan results
python main.py generate \
  --input ./data/reports \
  --output ./output/policies

# Evaluate generated policies
python main.py evaluate \
  --policies ./output/policies \
  --reference ./data/reference_policies
```

## What's Next?

- **Integrate into CI/CD**: Copy pipeline configs from `pipelines/`
- **Try Different LLMs**: Configure Ollama, DeepSeek, or Hugging Face
- **Customize Frameworks**: Modify prompts for ISO 27001 or CIS Controls
- **Evaluate Metrics**: Compare LLM outputs with BLEU and ROUGE-L

## Need Help?

- Read full documentation in `docs/`
- Check examples in `data/reports/`
- Review test cases in `tests/`
