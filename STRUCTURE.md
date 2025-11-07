# 📁 Project Structure

## Organization

```
devsecopsai/
├── 📱 sample_app/              # Sample vulnerable application
│   ├── backend/                # Spring Boot backend
│   └── frontend/               # React frontend
│
├── 🔍 scanners/                # Security scanning modules
│   ├── sast/                   # Static Analysis (Bandit, SpotBugs)
│   ├── sca/                    # Dependency Analysis (OWASP Dependency-Check)
│   └── dast/                   # Dynamic Testing (OWASP ZAP)
│
├── 🤖 llm_engine/              # AI/LLM integration
│   ├── llm_manager.py          # Multi-provider LLM support
│   └── prompt_engine.py        # Prompt generation
│
├── 📋 policy_generator/        # Policy generation
│   └── policy_orchestrator.py # Policy creation logic
│
├── 📊 parsers/                 # Report parsers
│   └── report_parser.py        # Parse scan results
│
├── ✅ evaluation/              # Quality metrics
│   └── evaluator.py            # BLEU, ROUGE-L scores
│
├── 📁 data/                    # Data and reports
│   ├── reports/                # Security scan outputs (JSON/HTML)
│   └── reference_policies/     # Baseline policies
│
├── 📤 output/                  # Generated outputs
│   ├── generated_policies/     # AI-generated policies
│   └── evaluation_results/     # Quality metrics
│
├── 🎨 dashboard/               # Web UI
│   └── app.py                  # Flask dashboard
│
├── 🔧 scripts/                 # Utility scripts
│   └── create_final_report.py # Generate consolidated report
│
├── 🔄 .github/workflows/       # CI/CD
│   └── devsecops.yml           # GitHub Actions pipeline
│
└── 🧪 tests/                   # Unit tests
    └── unit/
```

## Key Folders

### 📁 data/
- **Purpose**: Stores all security scan reports
- **Contents**: JSON/HTML files from Bandit, Dependency-Check, ZAP
- **Usage**: Input for AI policy generation

### 📤 output/
- **Purpose**: Contains generated policies and results
- **Contents**: 
  - `generated_policies/` - AI-created security policies
  - `evaluation_results/` - Quality metrics (BLEU, ROUGE-L)
  - `FINAL_SECURITY_REPORT.md` - Consolidated report
- **Usage**: Final deliverables

### 🔧 scripts/
- **Purpose**: Utility scripts for automation
- **Key Files**:
  - `create_final_report.py` - Generates consolidated report from all scans
- **Usage**: Run after scans complete

## Workflow

1. **Scan** → Generates reports in `data/reports/`
2. **Generate** → Creates policies in `output/generated_policies/`
3. **Evaluate** → Produces metrics in `output/evaluation_results/`
4. **Report** → Creates `output/FINAL_SECURITY_REPORT.md`

## CI/CD Artifacts

When the pipeline runs, download:

**📊-FINAL-SECURITY-REPORT** (artifact name)
- Single Markdown file with all findings
- Includes SAST, SCA, DAST results
- Shows generated policies
- Displays quality metrics
- Provides recommendations

## Clean Structure

- ✅ **No GitLab files** - Removed `.gitlab-ci.yml`
- ✅ **Organized by function** - Each folder has clear purpose
- ✅ **Single final report** - One artifact to download
- ✅ **90-day retention** - Final report kept for 3 months
