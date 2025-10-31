# 🧪 Testing and Running Guide

## Quick Start (5 Minutes)

### Step 1: Initial Setup

```bash
# Navigate to project directory
cd /home/vboxuser/devsecopsai

# Run automated setup
./scripts/setup.sh
```

If you haven't run the setup script yet, it will:
- Create virtual environment
- Install all dependencies
- Create necessary directories
- Copy environment template

### Step 2: Manual Setup (if script didn't run)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize project structure
python main.py init
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your API key
nano .env
```

Add at minimum:
```bash
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
OPENAI_API_KEY=sk-your-actual-key-here
```

**Don't have an API key?** Use Ollama (free local option) - see Option 2 below.

### Step 4: Verify Setup

```bash
python main.py check-config
```

Expected output:
```
🔍 Checking configuration...

LLM Provider: openai
OpenAI API Key: ✅ Set

Security Tools:
SonarQube URL: ❌ Not set
ZAP Proxy: ❌ Not set

Directories:
data/reports: ✅ Exists
data/reference_policies: ✅ Exists
output: ✅ Exists
logs: ✅ Exists
```

---

## 🎯 Option 1: Test with Sample Data (Recommended First)

This uses pre-created sample vulnerability reports - no scanning needed!

### 1. Parse Sample Reports

```bash
# Parse a Bandit report
python main.py parse --input ./data/reports/sample_bandit_report.json
```

**Expected output:**
```
📄 Parsed Vulnerability Report:

Total Vulnerabilities: 3

By Severity:
  HIGH: 2
  LOW: 1
```

### 2. Generate Policy from Samples

```bash
# Generate NIST CSF policy
python main.py generate \
  --input ./data/reports \
  --output ./output/test_policies \
  --framework NIST_CSF
```

**Expected output:**
```
📄 Parsing vulnerability reports...
✅ Parsed 2 vulnerability reports
🤖 Generating policies using NIST_CSF...
✅ Generated 1 security policies
📁 Policies saved to: ./output/test_policies
  - ./output/test_policies/nist_csf_policy_20251031_143022.json
```

**This will:**
- Parse sample reports
- Send to LLM (OpenAI/etc.)
- Generate security policy
- Save as JSON and Markdown

### 3. Evaluate Generated Policy

```bash
# Evaluate against reference
python main.py evaluate \
  --policies ./output/test_policies \
  --reference ./data/reference_policies \
  --metrics BLEU,ROUGE-L,COMPLIANCE
```

**Expected output:**
```
📊 Evaluating generated policies...
✅ Evaluation completed!

📈 Results Summary:
  BLEU Score: 0.4523
  ROUGE-L Score: 0.5891
  Compliance Score: 0.8200

📁 Detailed results saved to: ./output/evaluation_results
```

### 4. View Generated Policy

```bash
# View the JSON policy
cat ./output/test_policies/nist_csf_policy_*.json | jq '.'

# View the Markdown version (more readable)
cat ./output/test_policies/nist_csf_policy_*.md
```

---

## 🔍 Option 2: Run Full Security Scan

This scans the sample vulnerable application.

### 1. Scan the Sample App

```bash
# Scan with all tools
python main.py scan --target ./sample_app --scanners all
```

**Expected output:**
```
Starting security scan on target: ./sample_app
Running SAST scans...
  - bandit
    ✓ Report: ./data/reports/bandit_report.json
  - sonarqube
    ✗ sonarqube failed: SonarQube token not set
Running SCA scans...
  - dependency_check
    ✓ Report: ./data/reports/dependency_check_report.json
  - safety
    ✓ Report: ./data/reports/safety_report.json

✅ Scans completed successfully!
📊 Results saved to: ./data/reports
```

**Note:** Some tools may fail if not installed (SonarQube, ZAP). That's OK for testing!

### 2. View Scan Results

```bash
# List all reports
ls -lh ./data/reports/

# View a report
cat ./data/reports/bandit_report.json | jq '.'
```

### 3. Generate Policy from Scan Results

```bash
python main.py generate \
  --input ./data/reports \
  --output ./output/generated_policies \
  --framework NIST_CSF
```

### 4. Try Different Frameworks

```bash
# ISO 27001
python main.py generate \
  --input ./data/reports \
  --output ./output/generated_policies \
  --framework ISO_27001

# CIS Controls
python main.py generate \
  --input ./data/reports \
  --output ./output/generated_policies \
  --framework CIS_CONTROLS
```

---

## 🆓 Option 3: Use Free Local LLM (Ollama)

No API costs! Runs locally on your machine.

### 1. Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve &

# Pull LLaMA model (3.2B - small and fast)
ollama pull llama3.2

# Or pull larger model for better quality
ollama pull llama3.3
```

### 2. Configure for Ollama

Edit `.env`:
```bash
LLM_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
# No API key needed!
```

### 3. Generate Policy

```bash
python main.py generate \
  --input ./data/reports \
  --output ./output/ollama_policies \
  --framework NIST_CSF
```

---

## 🧪 Run Unit Tests

### Run All Tests

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov --cov-report=html
```

**Expected output:**
```
========================= test session starts ==========================
collected 8 items

tests/unit/test_parser.py ......                                  [ 75%]
tests/unit/test_evaluator.py ..                                   [100%]

========================== 8 passed in 2.34s ===========================
```

### Run Specific Tests

```bash
# Test parser only
pytest tests/unit/test_parser.py

# Test evaluator only
pytest tests/unit/test_evaluator.py

# Test specific function
pytest tests/unit/test_parser.py::test_parse_bandit_report -v
```

### View Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov --cov-report=html

# Open in browser
xdg-open htmlcov/index.html  # Linux
# or
open htmlcov/index.html      # macOS
```

---

## 🔬 Research Workflow: Compare LLMs

This is for your academic comparative study!

### 1. Test with OpenAI GPT-4

```bash
# Edit .env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
OPENAI_API_KEY=sk-your-key

# Generate
python main.py generate \
  --input ./data/reports \
  --output ./output/gpt4_policies \
  --framework NIST_CSF
```

### 2. Test with OpenAI GPT-3.5

```bash
# Edit .env
LLM_MODEL=gpt-3.5-turbo

# Generate
python main.py generate \
  --input ./data/reports \
  --output ./output/gpt35_policies \
  --framework NIST_CSF
```

### 3. Test with Ollama (Free)

```bash
# Edit .env
LLM_PROVIDER=ollama

# Generate
python main.py generate \
  --input ./data/reports \
  --output ./output/ollama_policies \
  --framework NIST_CSF
```

### 4. Compare Results

```bash
# Evaluate GPT-4 policies
python main.py evaluate \
  --policies ./output/gpt4_policies \
  --reference ./data/reference_policies \
  --output ./output/eval_gpt4

# Evaluate GPT-3.5 policies
python main.py evaluate \
  --policies ./output/gpt35_policies \
  --reference ./data/reference_policies \
  --output ./output/eval_gpt35

# Evaluate Ollama policies
python main.py evaluate \
  --policies ./output/ollama_policies \
  --reference ./data/reference_policies \
  --output ./output/eval_ollama
```

### 5. Compare Metrics

```bash
# View all results
cat ./output/eval_gpt4/summary.json | jq '.metrics'
cat ./output/eval_gpt35/summary.json | jq '.metrics'
cat ./output/eval_ollama/summary.json | jq '.metrics'
```

---

## 📊 Generate Final Report

```bash
python scripts/generate_final_report.py \
  --evaluation ./output/evaluation_results \
  --policies ./output/generated_policies \
  --output ./reports/final_report.md
```

View report:
```bash
cat ./reports/final_report.md
# or
nano ./reports/final_report.md
```

---

## 🐛 Troubleshooting

### Issue: "Module not found"

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "OpenAI API error"

```bash
# Check your API key
cat .env | grep OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Solution:** Use Ollama instead (free, no API key needed)

### Issue: "Bandit command not found"

```bash
# Install Bandit
pip install bandit
```

### Issue: "No vulnerabilities found"

**Solution:** Use the sample_app which has intentional vulnerabilities:
```bash
python main.py scan --target ./sample_app
```

### Issue: "Permission denied" on scripts

```bash
# Make scripts executable
chmod +x ./scripts/*.sh
```

---

## 📝 Complete Test Workflow

Here's a complete end-to-end test:

```bash
# 1. Setup
cd /home/vboxuser/devsecopsai
source venv/bin/activate

# 2. Verify configuration
python main.py check-config

# 3. Parse sample data
python main.py parse --input ./data/reports/sample_bandit_report.json

# 4. Generate policy
python main.py generate \
  --input ./data/reports \
  --output ./output/test_run \
  --framework NIST_CSF

# 5. Evaluate policy
python main.py evaluate \
  --policies ./output/test_run \
  --reference ./data/reference_policies

# 6. View results
cat ./output/evaluation_results/summary.json | jq '.'
cat ./output/test_run/*.md

# 7. Run tests
pytest tests/ -v
```

---

## 🎯 What to Test for Your Project

### 1. Basic Functionality ✅
- [x] Parse sample reports
- [x] Generate policies
- [x] Evaluate policies
- [x] Run unit tests

### 2. LLM Comparison ✅
- [ ] Test with GPT-4
- [ ] Test with GPT-3.5
- [ ] Test with Ollama
- [ ] Compare metrics

### 3. Framework Comparison ✅
- [ ] Generate NIST CSF policies
- [ ] Generate ISO 27001 policies
- [ ] Generate CIS Controls policies
- [ ] Compare compliance scores

### 4. Real Application Testing ✅
- [ ] Scan sample_app
- [ ] Scan your own project
- [ ] Generate policies from real scans
- [ ] Evaluate quality

---

## 💰 Cost Considerations

### OpenAI Costs
- **GPT-3.5-turbo**: ~$0.002 per policy
- **GPT-4**: ~$0.03 per policy

### Free Alternatives
1. **Ollama**: Completely free, runs locally
2. **Sample Data**: Test without scanning

---

## 📈 Expected Results

### Sample Report → Policy Generation
- **Time**: 10-30 seconds
- **Output**: JSON + Markdown policy
- **Size**: 2-5 KB

### Evaluation Metrics
- **BLEU**: 0.3-0.6 (typical)
- **ROUGE-L**: 0.4-0.7 (typical)
- **Compliance**: 0.6-0.9 (typical)

### Full Scan → Policy → Evaluation
- **Time**: 2-5 minutes
- **Vulnerabilities**: 5-20 (sample_app)
- **Policy Pages**: 2-4

---

## 🚀 Next Steps

1. **Start Simple**: Use sample data first
2. **Test Ollama**: Free and easy
3. **Try OpenAI**: When ready to spend
4. **Run Full Workflow**: Scan → Generate → Evaluate
5. **Compare LLMs**: For research
6. **Document Results**: For report

---

## ✅ Success Checklist

After testing, you should have:
- [ ] Successfully parsed reports
- [ ] Generated at least one policy
- [ ] Evaluated policy with metrics
- [ ] Run unit tests (all passing)
- [ ] Compared at least 2 LLMs
- [ ] Generated final report
- [ ] Documented your findings

---

**Ready to start?** Run: `python main.py check-config`

**Need help?** Check: `python main.py --help`
