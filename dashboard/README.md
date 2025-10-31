# DevSecOps AI Dashboard

## 🎯 Overview

The DevSecOps AI Dashboard provides a **real-time web interface** to monitor your CI/CD pipeline results, security vulnerabilities, generated policies, and quality metrics.

## 📊 Features

### 1. **Pipeline Status Monitoring**
- Real-time pipeline stage tracking (Scan → Generate → Evaluate)
- Overall health status indicator
- Stage-by-stage progress visualization

### 2. **Vulnerability Analytics**
- Total vulnerability counts by severity (Critical, High, Medium, Low)
- Interactive severity distribution charts
- Detailed vulnerability list with:
  - Source scanner (Bandit, Safety, etc.)
  - Severity level
  - Description
  - Location in code
  - CWE mapping

### 3. **Policy Tracking**
- List of all generated policies
- Framework identification (NIST, ISO 27001, CIS)
- Creation timestamps
- File sizes

### 4. **Quality Metrics**
- BLEU scores (n-gram overlap)
- ROUGE-L scores (longest common subsequence)
- Compliance scores
- Readability metrics
- Interactive radar charts

### 5. **Historical Trends**
- Scan history over time
- Vulnerability trend graphs
- Comparative analysis

## 🚀 Quick Start

### Launch the Dashboard

```bash
# Option 1: Using the launch script
./start_dashboard.sh

# Option 2: Manual launch
cd dashboard
source ../venv/bin/activate
python app.py
```

### Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

### Dashboard URL from other machines

If you want to access from another computer on your network:
```
http://YOUR_IP_ADDRESS:5000
```

## 📱 Dashboard Sections

### Status Bar (Top)
- **Pipeline Status**: Current overall status
- **Status Badge**: Visual indicator (Success/Warning/Failed/Running/Pending)
- **Refresh Button**: Manual data refresh

### Metrics Cards
- **Critical Vulnerabilities**: Count requiring immediate action
- **High Severity**: Count to address in next sprint
- **Medium Severity**: Count to plan for remediation
- **Low Severity**: Count to monitor

### Charts
1. **Vulnerability Distribution**: Pie chart showing severity breakdown
2. **Policy Quality Metrics**: Radar chart with BLEU/ROUGE/Compliance scores
3. **Scan History**: Line graph showing vulnerability trends over time

### Lists
1. **Recent Vulnerabilities**: Scrollable list with full details
2. **Generated Policies**: All policies with frameworks and timestamps

## 🔄 Auto-Refresh

The dashboard automatically refreshes every **30 seconds** to show the latest data.

You can also manually refresh at any time using the "🔄 Refresh" button.

## 📂 Data Sources

The dashboard reads from:
- `data/reports/` - Security scan results
- `output/generated_policies/` - Generated policy documents
- `output/evaluation_results/` - Evaluation metrics
- `logs/` - Application logs

## 🎨 Dashboard Screenshot Preview

```
┌─────────────────────────────────────────────────────────────┐
│ 🛡️ DevSecOps AI Dashboard                                   │
│ Real-time CI/CD Pipeline Monitoring & Security Analytics    │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────┬─────────────────┐
│ ✓ Pipeline completed successfully        │  🔄 Refresh     │
│ [SUCCESS]                                 │                 │
└──────────────────────────────────────────┴─────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 📊 Pipeline Stages                                          │
│ ┌───────┐  ┌───────────┐  ┌────────────┐                   │
│ │ Scan  │→ │ Generate  │→ │ Evaluate   │                   │
│ │✓Done  │  │✓Done      │  │✓Done       │                   │
│ └───────┘  └───────────┘  └────────────┘                   │
└─────────────────────────────────────────────────────────────┘

┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│ 🔴 0 │  │ 🟠 2 │  │ 🟡 4 │  │ 🔵 6 │
│Critical│ │ High │  │Medium│  │ Low  │
└──────┘  └──────┘  └──────┘  └──────┘

┌────────────────────┐  ┌────────────────────┐
│ 📊 Vulnerability   │  │ 📈 Policy Quality  │
│    Distribution    │  │     Metrics        │
│                    │  │                    │
│   [Pie Chart]      │  │   [Radar Chart]    │
└────────────────────┘  └────────────────────┘

┌────────────────────┐  ┌────────────────────┐
│ 🔍 Recent Vulns    │  │ 📄 Generated       │
│                    │  │    Policies        │
│ • SQL Injection    │  │ • NIST Policy.md   │
│ • Debug Mode On    │  │ • ISO 27001.md     │
│ • Hardcoded Key    │  │ • CIS Controls.md  │
└────────────────────┘  └────────────────────┘
```

## 🔧 Configuration

### Port Configuration
By default, the dashboard runs on port 5000. To change:

Edit `dashboard/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change port here
```

### Data Directories
Configured in `dashboard/app.py`:
```python
REPORTS_DIR = BASE_DIR / "data" / "reports"
POLICIES_DIR = BASE_DIR / "output" / "generated_policies"
EVALUATION_DIR = BASE_DIR / "output" / "evaluation_results"
```

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Check if Flask is installed
pip install Flask==3.0.0

# Check if port 5000 is in use
lsof -i :5000

# Try a different port
cd dashboard
python app.py --port 8080
```

### No data showing
```bash
# Make sure you've run scans first
python main.py scan --target ./sample_app

# Generate policies
python main.py generate --input ./data/reports

# Check data directories exist
ls -la data/reports/
ls -la output/generated_policies/
```

### Browser connection refused
- Check firewall settings
- Ensure Flask is running (look for startup messages)
- Try `http://127.0.0.1:5000` instead of `localhost`

## 📊 API Endpoints

The dashboard exposes REST APIs for programmatic access:

- `GET /api/status` - Pipeline status
- `GET /api/vulnerabilities` - Vulnerability data
- `GET /api/metrics` - Evaluation metrics
- `GET /api/policies` - Generated policies list
- `GET /api/policy/<name>` - Specific policy content
- `GET /api/history` - Historical scan data

### Example API Usage
```bash
# Get current status
curl http://localhost:5000/api/status

# Get vulnerability counts
curl http://localhost:5000/api/vulnerabilities

# Get evaluation metrics
curl http://localhost:5000/api/metrics
```

## 🎯 Integration with CI/CD

### Option 1: Background Dashboard
Keep the dashboard running in the background during CI/CD:

```yaml
# .gitlab-ci.yml
dashboard:
  stage: monitoring
  script:
    - nohup ./start_dashboard.sh &
    - echo "Dashboard at http://$(hostname):5000"
  artifacts:
    reports:
      dotenv: dashboard.env
```

### Option 2: Static Report Generation
Generate a static HTML report instead:

```bash
# After pipeline completes
python dashboard/generate_static_report.py
```

## 🌟 Next Steps

1. **Customize Charts**: Edit `templates/index.html` to add more visualizations
2. **Add Authentication**: Implement user login for production use
3. **Export Reports**: Add PDF/Excel export functionality
4. **Notifications**: Add email/Slack alerts for critical vulnerabilities
5. **Multi-Project**: Support multiple projects in one dashboard

## 📝 Tips

- Keep the dashboard running during development for instant feedback
- Use the API endpoints to integrate with other tools
- Bookmark the dashboard URL for quick access
- Set up auto-refresh in your browser for continuous monitoring
- Use the vulnerability list to quickly identify and prioritize issues

---

**Need help?** Check the main `README.md` or `docs/` folder for more information.
