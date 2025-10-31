# DevSecOps AI: Automated Security Policy Generation

## 🎯 Project Overview

This project explores how Large Language Models (LLMs) can automate the translation of technical vulnerability reports (SAST, SCA, DAST) into human-readable security policies aligned with international standards (NIST CSF, ISO/IEC 27001).

## 📋 Project Objectives

1. Understand the role of DevSecOps in modern secure software development
2. Apply AI-assisted automation to enhance the security lifecycle
3. Use SAST, SCA, and DAST tools to identify vulnerabilities
4. Develop parsing mechanisms to preprocess security reports
5. Employ LLMs for automatic security policy generation
6. **Bonus**: Conduct research-level evaluation using BLEU and ROUGE-L metrics
7. **Bonus**: Analyze ethical, privacy, and reliability concerns

## 🏗️ Project Architecture

```
devsecopsai/
├── pipelines/           # CI/CD configurations
├── scanners/            # SAST, SCA, DAST integrations
├── parsers/             # Vulnerability report parsers
├── llm_engine/          # LLM integration modules
├── policy_generator/    # Policy generation logic
├── evaluation/          # Metrics and evaluation
├── data/                # Sample reports and templates
├── reports/             # Generated documentation
└── tests/               # Unit and integration tests
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker (for security tools)
- Git
- Cloud provider account (AWS/GitLab/GitHub)
- API access to LLMs (OpenAI, Hugging Face, or local models)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd devsecopsai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Running the Pipeline

```bash
# Run security scans
python main.py scan --target ./sample_app

# Generate policies from reports
python main.py generate --input data/reports/vulnerability_report.json

# Evaluate generated policies
python main.py evaluate --policy output/generated_policy.json --reference data/reference_policies/
```

## 🔧 Components

### 1. Security Scanning Tools

- **SAST**: SonarQube for static analysis
- **SCA**: OWASP Dependency-Check for dependency vulnerabilities
- **DAST**: OWASP ZAP for dynamic application security testing

### 2. LLM Integration

Supports multiple LLM providers:
- LLaMA 3.3 (via Ollama or Hugging Face)
- DeepSeek R1
- OpenAI GPT-4/GPT-3.5
- Custom fine-tuned models

### 3. Policy Frameworks

- NIST Cybersecurity Framework (CSF)
- ISO/IEC 27001:2022
- CIS Controls
- Custom templates

## 📊 Evaluation Metrics

- **BLEU Score**: Measures n-gram overlap with reference policies
- **ROUGE-L**: Evaluates longest common subsequence
- **Compliance Score**: Custom metric for standards alignment
- **Readability Score**: Flesch-Kincaid reading ease

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run end-to-end tests
pytest tests/e2e
```

## 📚 Documentation

- [Setup Guide](docs/setup.md)
- [Pipeline Configuration](docs/pipeline_config.md)
- [LLM Integration Guide](docs/llm_integration.md)
- [Policy Templates](docs/policy_templates.md)
- [Evaluation Methodology](docs/evaluation.md)

## 🎓 Academic Deliverables

### Project Report Structure

1. **Introduction & Context**
   - Problem statement
   - Literature review
   - Research questions

2. **Architecture & Implementation**
   - System design
   - Technical choices
   - Implementation details

3. **Results & Evaluation**
   - Experimental setup
   - Quantitative results (BLEU, ROUGE-L)
   - Qualitative analysis

4. **Discussion & Future Work**
   - Limitations
   - Ethical considerations
   - Future directions

## 🤝 Contributing

This is an academic project. Contributions should follow the project objectives and maintain research integrity.

## 📄 License

[Specify your license]

## 👥 Team

[Add team members]

## 📧 Contact

[Add contact information]

## 🙏 Acknowledgments

- NIST for Cybersecurity Framework
- ISO for 27001 standards
- OWASP for security tools
- Open-source LLM communities
