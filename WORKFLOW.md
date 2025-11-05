# DevSecOps AI - Complete Project Workflow

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Local Development Workflow](#local-development-workflow)
4. [CI/CD Pipeline Workflow](#cicd-pipeline-workflow)
5. [Component Details](#component-details)
6. [Dashboard Usage](#dashboard-usage)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**DevSecOps AI** is an automated security policy generation system that:
- Scans applications for vulnerabilities (SAST, SCA, DAST)
- Uses AI (Ollama with qwen2.5:1.5b) to generate security policies
- Provides a web dashboard to visualize results
- Integrates with GitHub Actions for CI/CD

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    DevSecOps AI Pipeline                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: SECURITY SCANNING                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐               │
│  │   SAST   │     │   SCA    │     │   DAST   │               │
│  │ (Bandit) │     │ (Safety) │     │ (ZAP)    │               │
│  │SpotBugs  │     │  OWASP   │     │          │               │
│  └────┬─────┘     └────┬─────┘     └────┬─────┘               │
│       │                │                 │                      │
│       └────────────────┼─────────────────┘                      │
│                        ▼                                        │
│            data/reports/*.json                                  │
│         (bandit, dependency-check,                              │
│          safety, npm_audit, zap)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: REPORT PARSING                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ReportParser (parsers/report_parser.py)                      │
│    ├─ Reads JSON/XML reports                                    │
│    ├─ Normalizes vulnerability data                             │
│    └─ Aggregates findings                                       │
│                        │                                        │
│                        ▼                                        │
│            Parsed Vulnerability Data                            │
│         {severity, description, location,                       │
│          cwe, recommendation}                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: AI POLICY GENERATION                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    LLM Engine (llm_engine/llm_manager.py)                       │
│    ├─ Ollama Server (localhost:11434)                           │
│    ├─ Model: qwen2.5:1.5b                                       │
│    └─ Cached responses (cache/llm/)                             │
│                        │                                        │
│                        ▼                                        │
│    Policy Orchestrator (policy_generator/)                      │
│    ├─ Framework: NIST_CSF / CIS_CONTROLS                        │
│    ├─ Generates controls & recommendations                      │
│    └─ Assigns severity & priorities                             │
│                        │                                        │
│                        ▼                                        │
│        output/generated_policies/*.json                         │
│         (NIST_CSF, CIS_CONTROLS policies)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: POLICY EVALUATION                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    Evaluator (evaluation/evaluator.py)                          │
│    ├─ BLEU Score (precision metrics)                            │
│    ├─ ROUGE-L Score (recall metrics)                            │
│    ├─ Quality Score (0-1 scale)                                 │
│    └─ Coverage Score                                            │
│                        │                                        │
│                        ▼                                        │
│    output/evaluation_results/*.json                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: DASHBOARD VISUALIZATION                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    Flask Dashboard (dashboard/app.py)                           │
│    ├─ Port: 5000                                                │
│    ├─ Endpoints:                                                │
│    │   GET  /                    - Main dashboard               │
│    │   GET  /api/status          - Pipeline status              │
│    │   GET  /api/metrics         - Quality metrics              │
│    │   GET  /api/vulnerabilities - Vuln summary                 │
│    │   GET  /api/policies        - Generated policies           │
│    └─ Real-time data from JSON files                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Local Development Workflow

### **Prerequisites**
```bash
# System requirements
- Python 3.9+
- Node.js 14+ (for sample app)
- Java 17+ (for sample app)
- Ollama installed and running
- Git

# Check installations
python --version
node --version
java --version
ollama --version
```

### **Step 1: Initial Setup**

```bash
# 1. Clone the repository
git clone git@github.com:DOHA6/devsecopsai.git
cd devsecopsai

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env  # If exists, or create manually
nano .env

# Add to .env:
LLM_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
LLM_MODEL=qwen2.5:1.5b
LOG_LEVEL=INFO
```

### **Step 2: Start Ollama**

```bash
# Start Ollama service
ollama serve &

# Pull the model (first time only)
ollama pull qwen2.5:1.5b

# Verify it's running
curl http://localhost:11434/api/tags
```

### **Step 3: Run Security Scans**

```bash
# Scan the Python sample app
python main.py scan --target ./sample_app --scanners all

# Or scan the Java/React app
python main.py scan --target ./sample_app_java --scanners all

# Check generated reports
ls -lh data/reports/
# Should see:
# - bandit_report.json
# - dependency-check-report.json
# - safety_report.json
# - zap_report.json (if DAST ran)
```

### **Step 4: Generate Policies**

```bash
# Generate policies from scan reports
python main.py generate \
  --input data/reports \
  --output output/generated_policies \
  --framework NIST_CSF

# Optional: Generate with different framework
python main.py generate \
  --input data/reports \
  --output output/generated_policies \
  --framework CIS_CONTROLS

# Check generated policies
ls -lh output/generated_policies/
# Should see JSON files with timestamps
```

### **Step 5: Evaluate Policies (Optional)**

```bash
# Evaluate generated policies against reference
python main.py evaluate \
  --policies output/generated_policies \
  --reference data/reference_policies \
  --output output/evaluation_results

# View evaluation metrics
cat output/evaluation_results/evaluation_report_*.json | jq
```

### **Step 6: Start Dashboard**

```bash
# Start the Flask dashboard
python dashboard/app.py

# Or use the script
./start_dashboard.sh

# Access dashboard
# Open browser: http://localhost:5000
```

### **Step 7: View Results**

```
Dashboard shows:
┌─────────────────────────────────────────────┐
│          DevSecOps AI Dashboard             │
├─────────────────────────────────────────────┤
│ Pipeline Status:        ✓ Completed         │
│ Total Vulnerabilities:  20                  │
│   - HIGH:               2                   │
│   - MEDIUM:             4                   │
│   - LOW:                11                  │
│   - INFO:               3                   │
├─────────────────────────────────────────────┤
│ Generated Policies:     11                  │
│ Frameworks:             NIST_CSF, CIS       │
├─────────────────────────────────────────────┤
│ Quality Metrics:                            │
│   - BLEU Score:         0.72                │
│   - ROUGE-L:            0.68                │
│   - Quality Score:      0.85                │
│   - Coverage:           0.78                │
├─────────────────────────────────────────────┤
│ [View Details] [Download Policies]          │
└─────────────────────────────────────────────┘
```

---

## 🔄 CI/CD Pipeline Workflow

### **GitHub Actions Pipeline Overview**

The `.github/workflows/devsecops.yml` file defines 6 jobs:

```
Trigger: Push to main/develop, PR to main, or weekly schedule
                              │
                              ▼
        ┌───────────────────────────────────────┐
        │  Job 1: SAST Scan (Python & Java)     │
        │  - Bandit for Python                   │
        │  - SpotBugs for Java                   │
        │  - Upload: sast-reports                │
        └────────────────┬──────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  Job 2: SCA Scan (Dependencies)       │
        │  - Safety (Python)                     │
        │  - OWASP Dependency-Check (Java)       │
        │  - npm audit (Node.js)                 │
        │  - Upload: sca-reports                 │
        └────────────────┬──────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  Job 3: Build Application              │
        │  - Maven build (Spring Boot)           │
        │  - npm install + build (React)         │
        │  - Upload: build-artifacts             │
        └────────────────┬──────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  Job 4: DAST Scan (Running App)       │
        │  - Start Spring Boot app               │
        │  - OWASP ZAP baseline scan             │
        │  - Upload: dast-reports                │
        └────────────────┬──────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  Job 5: Generate Policies (AI)        │
        │  - Download all reports                │
        │  - Run: python main.py generate        │
        │  - Upload: security-policies           │
        │  - Upload: dashboard report            │
        └────────────────┬──────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  Job 6: Security Gate                  │
        │  - Download all artifacts              │
        │  - Check thresholds:                   │
        │    * Max 0 CRITICAL                    │
        │    * Max 5 HIGH                        │
        │  - Fail build if exceeded              │
        └────────────────────────────────────────┘
```

### **Pipeline Configuration**

```yaml
# Environment Variables
JAVA_VERSION: '17'
NODE_VERSION: '14'      # Compatible with react-scripts 4.0.3
PYTHON_VERSION: '3.9'

# Key Features
- continue-on-error: true   # Scans won't fail the build
- Artifact retention: 90 days
- Runs on: ubuntu-latest
```

### **How to Trigger Pipeline**

```bash
# Method 1: Push to main/develop
git add .
git commit -m "Your changes"
git push origin main

# Method 2: Create Pull Request
git checkout -b feature-branch
# Make changes
git push origin feature-branch
# Create PR on GitHub

# Method 3: Manual trigger (if enabled)
# Go to Actions tab -> Select workflow -> Run workflow

# Method 4: Automatic weekly scan
# Runs every Sunday at midnight (UTC)
```

### **Monitoring Pipeline**

```bash
# View pipeline status
# Go to: https://github.com/DOHA6/devsecopsai/actions

# Check specific run
# Click on run -> View job logs

# Download artifacts
# Go to run -> Scroll to "Artifacts" -> Download ZIP
```

---

## 🔧 Component Details

### **1. Scanner Orchestrator** (`scanners/scanner_orchestrator.py`)

```python
# Purpose: Coordinate all security scanners

Supported Scanners:
├─ SAST (Static Analysis)
│  ├─ Bandit: Python code analysis
│  └─ SpotBugs: Java bytecode analysis
│
├─ SCA (Software Composition Analysis)
│  ├─ Safety: Python package vulnerabilities
│  ├─ OWASP Dependency-Check: Java dependencies
│  └─ npm audit: Node.js packages
│
└─ DAST (Dynamic Analysis)
   └─ OWASP ZAP: Runtime vulnerability scanning

# Usage
orchestrator = ScannerOrchestrator(output_dir='data/reports')
results = orchestrator.run_scans(target_path, ['sast', 'sca', 'dast'])
```

### **2. Report Parser** (`parsers/report_parser.py`)

```python
# Purpose: Parse and normalize vulnerability reports

Supported Formats:
├─ JSON (Bandit, Safety, npm)
├─ XML (OWASP Dependency-Check, ZAP)
└─ HTML (ZAP reports)

# Normalized Output Structure
{
  "severity": "HIGH|MEDIUM|LOW|INFO",
  "description": "Vulnerability details",
  "location": "file:line or component",
  "cwe": "CWE-89",
  "cvss": 7.5,
  "recommendation": "Fix suggestion"
}

# Usage
parser = ReportParser()
vulns = parser.parse_directory('data/reports')
```

### **3. LLM Manager** (`llm_engine/llm_manager.py`)

```python
# Purpose: Interface with Ollama for AI generation

Features:
├─ Connection pooling
├─ Response caching (cache/llm/)
├─ Retry logic with exponential backoff
├─ Token counting and limits
└─ Temperature control

# Configuration
OLLAMA_HOST: http://localhost:11434
MODEL: qwen2.5:1.5b
TEMPERATURE: 0.7
MAX_TOKENS: 2048
TIMEOUT: 120 seconds

# Caching Strategy
Cache Key: SHA256(model + prompt + options)
Cache Hit: Return immediately
Cache Miss: Call Ollama + save response
```

### **4. Policy Orchestrator** (`policy_generator/policy_orchestrator.py`)

```python
# Purpose: Generate security policies using AI

Frameworks:
├─ NIST_CSF: 5 functions, 23 categories
│  (Identify, Protect, Detect, Respond, Recover)
│
├─ ISO_27001: 14 domains, 114 controls
│  (Information security management)
│
└─ CIS_CONTROLS: 18 controls
   (Critical Security Controls)

# Policy Structure
{
  "framework": "NIST_CSF",
  "control_id": "PR.AC-1",
  "title": "Identity and Access Management",
  "description": "...",
  "recommendations": [...],
  "severity": "HIGH",
  "priority": 1
}

# Generation Process
1. Group vulnerabilities by type
2. Map to framework controls
3. Generate policy with LLM
4. Validate and format output
5. Save to JSON file
```

### **5. Policy Evaluator** (`evaluation/evaluator.py`)

```python
# Purpose: Evaluate policy quality

Metrics:
├─ BLEU Score (0-1)
│  - Precision-based metric
│  - Compares n-grams with reference
│  - Higher = better match
│
├─ ROUGE-L Score (0-1)
│  - Recall-based metric
│  - Longest common subsequence
│  - Higher = better coverage
│
├─ Quality Score (0-1)
│  - Combined metric
│  - Weighted average of BLEU + ROUGE
│  - >0.75 = Good quality
│
└─ Coverage Score (0-1)
   - Percentage of controls addressed
   - Based on framework completeness

# Rating Scale
★★★★★ (0.90-1.00): Excellent
★★★★☆ (0.75-0.89): Good
★★★☆☆ (0.60-0.74): Fair
★★☆☆☆ (0.40-0.59): Needs Improvement
★☆☆☆☆ (0.00-0.39): Poor
```

### **6. Dashboard App** (`dashboard/app.py`)

```python
# Purpose: Web interface for visualization

Technology Stack:
├─ Backend: Flask (Python)
├─ Frontend: HTML/CSS/JavaScript
├─ Charts: Chart.js
└─ Data: JSON files

# API Endpoints

GET /
├─ Main dashboard page
└─ Returns: HTML template

GET /api/status
├─ Pipeline execution status
└─ Returns: {status, stage, progress, message}

GET /api/metrics
├─ Quality metrics
└─ Returns: {bleu, rouge_l, quality_score, coverage}

GET /api/vulnerabilities
├─ Vulnerability summary
└─ Returns: {total, by_severity, by_scanner}

GET /api/policies
├─ Generated policies
└─ Returns: [{framework, policies: [...]}]

# Performance
- Response time: <30ms
- Caching: In-memory
- Reload: Manual refresh
```

---

## 📊 Dashboard Usage

### **Accessing Dashboard**

```bash
# Start dashboard
cd /home/vboxuser/devsecopsai/devsecopsai
python dashboard/app.py

# Output:
# * Running on http://127.0.0.1:5000
# * Debug mode: off

# Open browser
firefox http://localhost:5000
# or
google-chrome http://localhost:5000
```

### **Dashboard Sections**

#### **1. Pipeline Status**
```
Status: Completed ✓
Stage: Policy Generation
Progress: 100%
Last Updated: 2025-11-05 21:30:45
```

#### **2. Vulnerability Overview**
```
Total Vulnerabilities: 20
├─ HIGH:    2  (10%)  🔴
├─ MEDIUM:  4  (20%)  🟡
├─ LOW:    11  (55%)  🟢
└─ INFO:    3  (15%)  🔵

By Scanner:
├─ Bandit (SAST):     8
├─ Safety (SCA):      5
├─ OWASP-DC (SCA):    4
└─ ZAP (DAST):        3
```

#### **3. Generated Policies**
```
Total Policies: 11
Frameworks:
├─ NIST_CSF:      6 policies
└─ CIS_CONTROLS:  5 policies

Download Options:
[Download All] [Download by Framework] [View JSON]
```

#### **4. Quality Metrics (Radar Chart)**
```
       Precision (BLEU)
              |
              |    0.72
       -------+-------
      |               |
0.68  |               | 0.85
      |               |
       -------+-------
              |
         Coverage
```

**How to Read:**
- **Distance from center** = Higher quality
- **Balanced shape** = Well-rounded policies
- **Spikes** = Strong in some areas, weak in others

#### **5. Recommendations**
```
Top Priority Actions:
1. Fix 2 HIGH severity SQL Injection issues
2. Update 4 vulnerable dependencies
3. Implement authentication controls
4. Add input validation
5. Enable security headers
```

---

## 🔍 Troubleshooting

### **Common Issues**

#### **Issue 1: Ollama Not Running**
```
Error: ConnectionError: Failed to connect to Ollama

Solution:
1. Check Ollama status
   ps aux | grep ollama
   
2. Start Ollama
   ollama serve &
   
3. Verify connection
   curl http://localhost:11434/api/tags
```

#### **Issue 2: No Scan Reports Found**
```
Error: No vulnerability reports found

Solution:
1. Check reports directory
   ls -lh data/reports/
   
2. Run scans first
   python main.py scan --target ./sample_app --scanners all
   
3. Verify JSON files exist
   file data/reports/*.json
```

#### **Issue 3: Dashboard Not Starting**
```
Error: Address already in use

Solution:
1. Find process using port 5000
   lsof -i :5000
   
2. Kill existing process
   pkill -f "python.*dashboard.*app.py"
   
3. Restart dashboard
   python dashboard/app.py
```

#### **Issue 4: Policy Generation Fails**
```
Error: LLM generation timeout

Solution:
1. Check Ollama model
   ollama list
   
2. Pull model if missing
   ollama pull qwen2.5:1.5b
   
3. Increase timeout in .env
   LLM_TIMEOUT=300
```

#### **Issue 5: GitHub Actions Failing**
```
Error: npm ci failed with exit code 9

Solution:
1. Check Node version in workflow
   NODE_VERSION: '14'  # Must be 14, not 16+
   
2. Use npm install instead of npm ci
   run: npm install
   
3. Clear cache and retry
   Actions -> Select run -> Re-run jobs -> Re-run failed jobs
```

#### **Issue 6: Missing Dependencies**
```
Error: ModuleNotFoundError: No module named 'bs4'

Solution:
1. Install missing package
   pip install beautifulsoup4
   
2. Or reinstall all requirements
   pip install -r requirements.txt
   
3. Check requirements.txt includes:
   beautifulsoup4==4.12.2
   lxml==5.1.0
```

---

## 📈 Performance Benchmarks

```
Scan Times (sample_app):
├─ SAST (Bandit):          ~5 seconds
├─ SCA (Safety):           ~10 seconds
├─ DAST (ZAP Baseline):    ~60 seconds
└─ Total Scan Time:        ~75 seconds

Policy Generation:
├─ Report Parsing:         <1 second
├─ LLM Generation:         ~4 seconds per policy
├─ 10 policies:            ~40 seconds
└─ With caching:           <5 seconds

Dashboard:
├─ Page Load:              <100ms
├─ API Response:           <30ms
├─ Memory Usage:           ~50MB
└─ CPU Usage:              <5%

GitHub Actions:
├─ SAST Job:               ~2 minutes
├─ SCA Job:                ~3 minutes
├─ Build Job:              ~4 minutes
├─ DAST Job:               ~5 minutes
├─ Policy Gen Job:         ~2 minutes
└─ Total Pipeline:         ~15-20 minutes
```

---

## 🎓 Best Practices

### **Development**
1. **Always run scans locally before pushing**
2. **Review generated policies manually**
3. **Keep Ollama model updated**
4. **Use virtual environment for Python**
5. **Cache LLM responses to save time**

### **CI/CD**
1. **Set appropriate security thresholds**
2. **Monitor pipeline failures**
3. **Review artifacts regularly**
4. **Keep dependencies updated**
5. **Use secrets for sensitive data**

### **Security**
1. **Never commit .env files**
2. **Rotate API keys regularly**
3. **Review vulnerability reports**
4. **Implement high-priority fixes first**
5. **Document security decisions**

---

## 📚 Additional Resources

```
Project Files:
├─ README.md              - Quick start guide
├─ GETTING_STARTED.md     - Setup instructions
├─ STRUCTURE.md           - Code organization
├─ TESTING_GUIDE.md       - Testing documentation
└─ WORKFLOW.md            - This file

External Links:
├─ NIST CSF: https://www.nist.gov/cyberframework
├─ CIS Controls: https://www.cisecurity.org/controls
├─ OWASP: https://owasp.org
├─ Ollama: https://ollama.ai
└─ GitHub Repo: https://github.com/DOHA6/devsecopsai
```

---

## 🎯 Quick Reference Commands

```bash
# Setup
pip install -r requirements.txt
ollama pull qwen2.5:1.5b

# Scan
python main.py scan --target ./sample_app --scanners all

# Generate
python main.py generate --input data/reports --output output/generated_policies

# Dashboard
python dashboard/app.py

# Git
git add .
git commit -m "message"
git push origin main

# Check Status
ps aux | grep ollama
curl http://localhost:5000/api/status
ls -lh data/reports/
```

---

**Last Updated:** November 5, 2025  
**Version:** 1.0.0  
**Maintained By:** DOHA6  
**Repository:** https://github.com/DOHA6/devsecopsai
