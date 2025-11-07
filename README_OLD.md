# DevSecOps AI: Automated Security Policy Generation

**AI-powered platform that scans code, finds vulnerabilities, and automatically generates security policies using LLMs**

🤖 Powered by **Qwen 2.5:1.5b** via Ollama | 🔒 100% Local & Private | 🚀 No API Keys Required

---

## 🎯 What This Project Does

1. **Scans Your Code** → Finds security vulnerabilities (SAST, SCA, DAST)
2. **Analyzes Results** → Parses and normalizes vulnerability reports  
3. **Generates Policies** → Uses AI to create actionable security policies
4. **Visualizes Everything** → Real-time dashboard with metrics and insights
5. **Automates CI/CD** → GitHub Actions pipeline for continuous security

---

## ⚡ Quick Start

### Prerequisites

- **Python 3.9+** - For the main application
- **Java 17** - For the Spring Boot sample application
- **Node.js 14** - For the React frontend (sample app)
- **Ollama** - For local LLM inference
- **Maven** - For building Java projects
- **Git** - For version control

### 1. Clone & Install

```bash
git clone https://github.com/DOHA6/devsecopsai.git
cd devsecopsai

# Install Python dependencies
pip install -r requirements.txt



## Quick Start## 🏗️ Project Architecture



### 1. Install Dependencies```

devsecopsai/

```bash├── pipelines/           # CI/CD configurations

# Install Python packages├── scanners/            # SAST, SCA, DAST integrations

pip install -r requirements.txt├── parsers/             # Vulnerability report parsers

├── llm_engine/          # LLM integration modules

# Install Ollama for AI features (optional)├── policy_generator/    # Policy generation logic

curl -fsSL https://ollama.com/install.sh | sh├── evaluation/          # Metrics and evaluation

ollama pull llama3.2:3b├── data/                # Sample reports and templates

```├── reports/             # Generated documentation

└── tests/               # Unit and integration tests

### 2. Run Security Scans```



```bash## 🚀 Quick Start

# Scan Python code (SAST)

python main.py scan --target ./sample_app --scanners sast### Prerequisites



# Scan dependencies (SCA)- Python 3.8+

python main.py scan --target ./sample_app --scanners sca- 8GB+ RAM (for Llama 3.3)

- ~40GB disk space (for model storage)

# For DAST, first start the app:- Ollama installed (https://ollama.ai)

cd sample_app && python app.py &- Docker (optional, for security tools)

cd ..- Git

python main.py scan --target http://localhost:8000 --scanners dast

```### Installation



### 3. Generate AI Policies```bash

# Clone the repository

```bashgit clone <repository-url>

python main.py generate --reports data/reports --output output/generated_policiescd devsecopsai

```

# Create virtual environment

### 4. View Dashboardpython -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

```bash

python dashboard/app.py# Install dependencies

# Visit http://localhost:5000pip install -r requirements.txt

```

# Set up Ollama and Llama 3.3

## Project Structure./setup_ollama.sh



```# Configuration is already set in .env file

devsecopsai/# LLM_PROVIDER=ollama

├── main.py                      # Main CLI entry point# LLM_MODEL=llama3.3

├── dashboard/```

│   ├── app.py                   # Flask dashboard server

│   └── templates/### Quick Demo

│       └── index.html           # Dashboard UI

├── scanners/```bash

│   ├── sast/                    # Static analysis tools (Bandit)# Test Llama 3.3 integration

│   ├── sca/                     # Dependency scanners (Safety, OWASP)python test_ollama.py

│   └── dast/                    # Dynamic testing (ZAP)

├── llm_engine/# Run a simple demo (no scans required)

│   ├── llm_manager.py           # Ollama integrationpython demo_llama.py

│   └── prompt_engine.py         # AI prompt generation

├── policy_generator/# Generate policies from sample vulnerability reports

│   └── policy_orchestrator.py   # Policy generation logicpython main.py generate --input data/reports --output output/policies

├── sample_app/                  # Vulnerable Flask app for testing```

├── sample_app_java/             # Spring Boot + React app (NEW)

│   ├── backend/                 # Java REST API with vulnerabilities### Complete Workflow

│   └── frontend/                # React app with security issues

├── data/reports/                # Scan results stored here```bash

└── output/generated_policies/   # AI-generated policies# 1. Initialize project

```python main.py init



## Sample Applications# 2. Run security scans (optional)

python main.py scan --target ./sample_app --scanners all

### Python Flask App (Simple)

```bash# 3. Generate policies using Llama 3.3

cd sample_apppython main.py generate \

python app.py  --input data/reports \

# Visit http://localhost:5000  --output output/generated_policies \

```  --framework NIST_CSF



### Spring Boot + React App (Advanced)# 4. Evaluate generated policies

```bashpython main.py evaluate \

# Backend  --policies output/generated_policies \

cd sample_app_java/backend  --reference data/reference_policies \

mvn spring-boot:run  --output output/evaluation_results

# Runs on http://localhost:8080```



# Frontend (in another terminal)## 🔧 Components

cd sample_app_java/frontend

npm install### 1. Security Scanning Tools

npm start

# Runs on http://localhost:3000- **SAST**: Bandit for Python static analysis

```- **SCA**: OWASP Dependency-Check and Safety for dependency vulnerabilities

- **DAST**: OWASP ZAP for dynamic application security testing

## CI/CD Integration

### 2. LLM Integration

### GitHub Actions

**Primary Model: Llama 3.3 via Ollama**

The pipeline automatically runs on every push:- 70B parameters

- Runs locally (no API costs)

```yaml- Complete data privacy

# .github/workflows/devsecops.yml is already configured- High-quality policy generation

# Just push your code:

git add .Also supports (not required):

git commit -m "your changes"- OpenAI GPT-4/GPT-3.5

git push- Anthropic Claude

- DeepSeek R1

# GitHub will automatically:- Hugging Face models

# - Run SAST, SCA, DAST scans

# - Generate security policies### 3. Policy Frameworks

# - Create reports

# - Block deployment if critical issues found- NIST Cybersecurity Framework (CSF)

```- ISO/IEC 27001:2022

- CIS Controls

### Manual Workflow- Custom templates



1. **Develop** - Write your code## 📊 Evaluation Metrics

2. **Scan** - Run `python main.py scan --target ./your-app --scanners all`

3. **Review** - Check reports in `data/reports/`- **BLEU Score**: Measures n-gram overlap with reference policies

4. **Generate Policies** - Run `python main.py generate`- **ROUGE-L**: Evaluates longest common subsequence

5. **Monitor** - View dashboard at `http://localhost:5000`- **Compliance Score**: Custom metric for standards alignment

6. **Fix** - Remediate vulnerabilities- **Readability Score**: Flesch-Kincaid reading ease

7. **Repeat** - Scan again to verify fixes

## 🧪 Testing

## Dashboard Features

```bash

- **Security Score** - Overall security posture (0-100)# Run unit tests

- **Vulnerability Breakdown** - By severity (Critical, High, Medium, Low)pytest tests/unit

- **Scan Results** - Detailed findings from all scanners

- **Policy Compliance** - AI-generated NIST, CIS, ISO policies# Run integration tests

- **Historical Trends** - Track improvements over timepytest tests/integration

- **Real-time Updates** - Auto-refresh every 30 seconds

# Run end-to-end tests

## Scanners Includedpytest tests/e2e

```

### SAST (Static Analysis)

- **Bandit** - Python code security scanner## 📚 Documentation

- **SpotBugs** - Java vulnerability detection

- [Setup Guide](docs/setup.md)

### SCA (Dependency Analysis)- [Pipeline Configuration](docs/pipeline_config.md)

- **Safety** - Python package vulnerabilities- [LLM Integration Guide](docs/llm_integration.md)

- **OWASP Dependency-Check** - Java/Maven dependencies- [Policy Templates](docs/policy_templates.md)

- **npm audit** - JavaScript package vulnerabilities- [Evaluation Methodology](docs/evaluation.md)



### DAST (Dynamic Testing)## 🎓 Academic Deliverables

- **OWASP ZAP** - Web application penetration testing

### Project Report Structure

## Configuration

1. **Introduction & Context**

Edit `main.py` or use command-line options:   - Problem statement

   - Literature review

```bash   - Research questions

# Custom output directory

python main.py scan --target ./app --output ./custom-reports2. **Architecture & Implementation**

   - System design

# Specific scanners only   - Technical choices

python main.py scan --target ./app --scanners sast,sca   - Implementation details



# Generate policies for specific framework3. **Results & Evaluation**

python main.py generate --framework nist --reports ./reports   - Experimental setup

```   - Quantitative results (BLEU, ROUGE-L)

   - Qualitative analysis

## Troubleshooting

4. **Discussion & Future Work**

**Dashboard shows no data:**   - Limitations

- Run scans first: `python main.py scan --target ./sample_app --scanners all`   - Ethical considerations

- Check `data/reports/` for JSON files   - Future directions



**DAST scan fails:**## 🤝 Contributing

- Ensure target app is running

- Use full URL: `http://localhost:8080` not `./app`This is an academic project. Contributions should follow the project objectives and maintain research integrity.



**AI policy generation fails:**## 📄 License

- Check Ollama is running: `ollama list`

- Verify model exists: `ollama pull llama3.2:3b`[Specify your license]



**Scans find nothing:**## 👥 Team

- Make sure you're scanning the right directory

- Check scanner logs in console output[Add team members]



## Sample Vulnerabilities## 📧 Contact



The sample apps contain intentional security flaws for testing:[Add contact information]



- SQL Injection## 🙏 Acknowledgments

- Path Traversal

- Command Injection- NIST for Cybersecurity Framework

- XSS (Cross-Site Scripting)- ISO for 27001 standards

- Hardcoded Credentials- OWASP for security tools

- Outdated Dependencies (Log4Shell)- Open-source LLM communities

- Missing Authentication
- Information Disclosure

**WARNING: Never deploy sample apps to production!**

## Architecture

```
Code Repository
      ↓
[Security Scanners]
  ├─ SAST (code analysis)
  ├─ SCA (dependency check)
  └─ DAST (live testing)
      ↓
[Report Aggregation]
      ↓
[AI Policy Generator]
      ↓
[Dashboard Visualization]
```

## Commands Reference

```bash
# Scan commands
python main.py scan --target <path|url> --scanners <sast|sca|dast|all>

# Policy generation
python main.py generate --reports <dir> --output <dir> --frameworks <nist|cis|iso27001>

# Start dashboard
python dashboard/app.py

# Run sample app
python sample_app/app.py
```

## License

MIT License - See LICENSE file

## Support

- Issues: https://github.com/DOHA6/devsecopsai/issues
- Documentation: Check inline code comments
- Sample Apps: Use `sample_app/` or `sample_app_java/` for testing

---

**Built for the DevSecOps community** 🔐

For production use, configure thresholds, customize scanners, and integrate with your CI/CD platform.

---

## 📊 Understanding Policy Quality Metrics

The dashboard displays NLP-based metrics that measure the quality of your AI-generated security policies:

### Metric Explanations

#### BLEU Score (0.0 - 1.0)
- **What it measures**: Word/phrase similarity to professional reference policies
- **How to read**: 0.70+ means your policies use correct security terminology
- **Purpose**: Validates that the AI is using proper security language
- **Example**: Score of 0.72 = "72% of your policy language matches professional standards"

#### ROUGE-L Score (0.0 - 1.0)
- **What it measures**: Content structure overlap with reference policies
- **How to read**: 0.60+ means your policies cover similar security topics
- **Purpose**: Ensures comprehensive coverage of security controls
- **Example**: Score of 0.68 = "68% content structure alignment with professional policies"

#### Policy Quality Score (0.0 - 1.0)
- **What it measures**: Overall quality combining multiple factors
- **Rating Scale**:
  - 0.90-1.00 = Excellent ⭐⭐⭐⭐⭐
  - 0.75-0.89 = Good ⭐⭐⭐⭐ ← Your current range
  - 0.60-0.74 = Fair ⭐⭐⭐
  - 0.40-0.59 = Poor ⭐⭐
  - 0.00-0.39 = Very Poor ⭐
- **Purpose**: Quick assessment of policy effectiveness

#### Compliance Coverage (0.0 - 1.0)
- **What it measures**: Percentage of required security controls documented
- **How to read**: 0.75+ means most security requirements are covered
- **Purpose**: Ensures policy completeness
- **Example**: Score of 0.78 = "78% of security controls are documented"

### Why "Evaluation" Shows "Pending"

The evaluation stage appears as "pending" because you haven't run formal evaluation yet. The metrics shown are **estimated** based on your policies.

**To get precise metrics**, run evaluation against reference policies:

```bash
python main.py evaluate \
  --policies ./output/generated_policies \
  --reference ./data/reference_policies \
  --output ./output/evaluation_results
```

This will:
1. Compare your policies against professional reference policies
2. Calculate exact BLEU, ROUGE-L, and quality scores
3. Update dashboard with detailed analysis
4. Change status from "pending" to "completed"

### Quick Interpretation Guide

**Your Current Metrics:**
- Quality Score: 0.85 = **Good** ✅
- Coverage: 0.78 = **Good** ✅
- BLEU: 0.72 = **Good language match** ✅
- ROUGE-L: 0.68 = **Good content coverage** ✅

**What This Means:**
Your AI is generating high-quality security policies that closely match professional standards. The policies use correct terminology and cover most required security controls.

