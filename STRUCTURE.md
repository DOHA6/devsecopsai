# 🎓 DevSecOps AI - Project Structure Overview

## 📁 Directory Structure

```
devsecopsai/
├── 📄 README.md                      # Main project documentation
├── 📄 PROJECT_GUIDE.md               # Academic deliverables guide
├── 📄 main.py                        # CLI entry point
├── 📄 requirements.txt               # Python dependencies
├── 📄 .env.example                   # Environment variables template
├── 📄 .gitignore                     # Git ignore rules
│
├── 📂 pipelines/                     # CI/CD configurations
│   ├── .gitlab-ci.yml               # GitLab CI pipeline
│   └── .github-actions.yml          # GitHub Actions workflow
│
├── 📂 scanners/                      # Security scanning tools
│   ├── scanner_orchestrator.py     # Main coordinator
│   ├── sast/                        # Static analysis
│   │   ├── bandit_scanner.py
│   │   └── sonarqube_scanner.py
│   ├── sca/                         # Dependency scanning
│   │   ├── dependency_check_scanner.py
│   │   └── safety_scanner.py
│   └── dast/                        # Dynamic analysis
│       └── zap_scanner.py
│
├── 📂 parsers/                       # Report parsing
│   └── report_parser.py             # Unified parser for all tools
│
├── 📂 llm_engine/                    # LLM integration
│   ├── llm_manager.py               # Multi-provider manager
│   └── prompt_engine.py             # Prompt templates
│
├── 📂 policy_generator/              # Policy creation
│   └── policy_orchestrator.py       # Policy generation logic
│
├── 📂 evaluation/                    # Quality assessment
│   └── evaluator.py                 # BLEU, ROUGE-L, compliance
│
├── 📂 data/                          # Sample data
│   ├── reports/                     # Sample vulnerability reports
│   └── reference_policies/          # Reference policy templates
│
├── 📂 docs/                          # Documentation
│   ├── setup.md                     # Setup instructions
│   ├── quickstart.md                # Quick start guide
│   └── ...
│
├── 📂 tests/                         # Test suite
│   ├── unit/                        # Unit tests
│   └── integration/                 # Integration tests
│
├── 📂 scripts/                       # Utility scripts
│   ├── setup.sh                     # Quick setup
│   ├── run_tests.sh                 # Test runner
│   └── generate_final_report.py    # Report generator
│
├── 📂 sample_app/                    # Vulnerable test app
│   ├── app.py                       # Flask app with vulnerabilities
│   └── requirements.txt             # Vulnerable dependencies
│
└── 📂 output/                        # Generated files (gitignored)
    ├── generated_policies/          # AI-generated policies
    └── evaluation_results/          # Evaluation metrics
```

## 🎯 Key Components

### 1. **Security Scanners** (`scanners/`)
- **SAST**: Bandit, SonarQube
- **SCA**: OWASP Dependency-Check, Safety
- **DAST**: OWASP ZAP
- Orchestrator coordinates all scanners

### 2. **Report Parser** (`parsers/`)
- Unified interface for all security tools
- Normalizes vulnerability data
- Supports JSON, XML, HTML formats

### 3. **LLM Engine** (`llm_engine/`)
- Multi-provider support:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
  - Ollama (Local models)
  - DeepSeek (R1)
  - Hugging Face (Transformers)
- Framework-specific prompt templates
- Retry logic and error handling

### 4. **Policy Generator** (`policy_generator/`)
- Generates policies from vulnerabilities
- Supports multiple frameworks:
  - NIST Cybersecurity Framework
  - ISO/IEC 27001
  - CIS Controls
- Category-specific policies
- Refinement capabilities

### 5. **Evaluator** (`evaluation/`)
- **BLEU**: N-gram overlap
- **ROUGE-L**: Longest common subsequence
- **Compliance**: Framework requirement coverage
- **Readability**: Flesch reading ease
- Generates detailed reports

## 🚀 Quick Start Commands

```bash
# 1. Setup
./scripts/setup.sh

# 2. Configure
nano .env  # Add your API keys

# 3. Test
python main.py check-config

# 4. Scan
python main.py scan --target ./sample_app

# 5. Generate Policies
python main.py generate \
  --input ./data/reports \
  --framework NIST_CSF

# 6. Evaluate
python main.py evaluate \
  --policies ./output/generated_policies \
  --reference ./data/reference_policies
```

## 📊 Research Workflow

### Phase 1: Data Collection
```bash
# Scan multiple targets
python main.py scan --target ./sample_app
python main.py scan --target /path/to/real/project
```

### Phase 2: Policy Generation (Comparative Study)
```bash
# Try different LLMs
LLM_PROVIDER=openai LLM_MODEL=gpt-4 python main.py generate ...
LLM_PROVIDER=openai LLM_MODEL=gpt-3.5-turbo python main.py generate ...
LLM_PROVIDER=anthropic python main.py generate ...
LLM_PROVIDER=ollama python main.py generate ...
```

### Phase 3: Evaluation
```bash
# Calculate all metrics
python main.py evaluate \
  --policies ./output/generated_policies \
  --reference ./data/reference_policies \
  --metrics BLEU,ROUGE-L,COMPLIANCE,READABILITY
```

### Phase 4: Report Generation
```bash
# Create final academic report
python scripts/generate_final_report.py \
  --evaluation ./output/evaluation_results \
  --policies ./output/generated_policies \
  --output ./reports/final_report.pdf
```

## 📚 Documentation

- **README.md**: Project overview and features
- **PROJECT_GUIDE.md**: Academic deliverables checklist
- **docs/setup.md**: Detailed setup instructions
- **docs/quickstart.md**: 5-minute quick start
- **CONTRIBUTING.md**: Contribution guidelines

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov --cov-report=html

# Specific tests
pytest tests/unit/test_parser.py
```

## 📈 Expected Outputs

### Generated Policies
- `output/generated_policies/*.json` - Policy documents
- `output/generated_policies/*.md` - Readable format

### Evaluation Results
- `output/evaluation_results/summary.json` - Metrics
- `output/evaluation_results/evaluation_report.md` - Analysis

### Final Report
- `reports/final_report.md` - Comprehensive report
- `reports/final_report.pdf` - Academic submission

## 🎓 Academic Deliverables

1. ✅ **Technical Implementation** (25%)
   - All components implemented
   - CI/CD pipelines configured
   - Multi-tool integration

2. ✅ **Research Components** (20%)
   - LLM comparison framework
   - Evaluation metrics
   - Analysis tools

3. ✅ **Policy Quality** (20%)
   - Multiple metrics
   - Standards compliance
   - Automated assessment

4. 📝 **Report** (15%)
   - Use generated report as template
   - Add your analysis
   - Include visualizations

5. 🎤 **Presentation** (20%)
   - Demo the system
   - Show results
   - Discuss findings

## 💡 Tips for Success

### Technical
- Start with sample data
- Use Ollama for development (free)
- Save all experiments
- Document configurations

### Research
- Compare at least 3 LLMs
- Run multiple evaluations
- Create comparison tables
- Visualize results

### Report Writing
- Follow academic structure
- Include all metrics
- Discuss limitations
- Address ethics

## 🔗 Key Files to Understand

1. **main.py** - Start here, CLI interface
2. **llm_engine/llm_manager.py** - LLM integration
3. **policy_generator/policy_orchestrator.py** - Policy creation
4. **evaluation/evaluator.py** - Metrics calculation
5. **pipelines/.gitlab-ci.yml** - CI/CD example

## 📞 Getting Help

- Read documentation in `docs/`
- Check sample files in `data/`
- Review test cases in `tests/`
- Examine code comments

## ✨ What Makes This Special

1. **Multi-LLM Support**: Compare different models
2. **Standards Compliance**: NIST, ISO, CIS
3. **Quantitative Evaluation**: BLEU, ROUGE-L
4. **Production Ready**: CI/CD integration
5. **Research Oriented**: Comparative study framework
6. **Well Documented**: Comprehensive guides
7. **Extensible**: Easy to add new tools/frameworks

## 🎯 Success Metrics

Your project is successful if you can:
- ✅ Scan code for vulnerabilities
- ✅ Generate policies with AI
- ✅ Evaluate policy quality
- ✅ Compare different LLMs
- ✅ Produce academic report
- ✅ Demonstrate the system

## 🚀 Next Steps

1. Run `./scripts/setup.sh`
2. Configure your `.env`
3. Try the quick start commands
4. Start your research!

Good luck! 🎓
