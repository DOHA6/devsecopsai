# DevSecOps AI - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DevSecOps AI System                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  Phase 1: Security Scanning                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Bandit  │  │SonarQube │  │  OWASP   │  │   OWASP  │          │
│  │  (SAST)  │  │  (SAST)  │  │Dep-Check │  │    ZAP   │          │
│  │          │  │          │  │   (SCA)  │  │  (DAST)  │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │             │              │              │                 │
│       └─────────────┴──────────────┴──────────────┘                │
│                            │                                        │
│                   ┌────────▼────────┐                              │
│                   │    Scanner      │                              │
│                   │  Orchestrator   │                              │
│                   └────────┬────────┘                              │
│                            │                                        │
│                     JSON/XML/HTML Reports                          │
└────────────────────────────┬───────────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────────┐
│  Phase 2: Report Parsing                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│                   ┌────────────────┐                                │
│                   │ Report Parser  │                                │
│                   │  (Normalizer)  │                                │
│                   └────────┬───────┘                                │
│                            │                                        │
│                   Structured Vulnerability Data                     │
│                   {id, severity, description, ...}                  │
└────────────────────────────┬───────────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────────┐
│  Phase 3: Policy Generation                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────┐           │
│  │              Prompt Engine                          │           │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │           │
│  │  │NIST CSF  │ │ISO 27001 │ │   CIS    │           │           │
│  │  │ Template │ │ Template │ │ Controls │           │           │
│  │  └──────────┘ └──────────┘ └──────────┘           │           │
│  └────────────────────┬────────────────────────────────┘           │
│                       │                                             │
│                   Formatted Prompt                                  │
│                       │                                             │
│  ┌────────────────────▼────────────────────────────────┐           │
│  │              LLM Manager                            │           │
│  │  ┌────────┐ ┌─────────┐ ┌────────┐ ┌────────┐    │           │
│  │  │ OpenAI │ │Anthropic│ │ Ollama │ │DeepSeek│    │           │
│  │  │  GPT-4 │ │ Claude  │ │LLaMA 3 │ │   R1   │    │           │
│  │  └────────┘ └─────────┘ └────────┘ └────────┘    │           │
│  └────────────────────┬────────────────────────────────┘           │
│                       │                                             │
│                 Generated Policy Text                               │
│                       │                                             │
│  ┌────────────────────▼────────────────────────────────┐           │
│  │         Policy Orchestrator                         │           │
│  │    (Formatting, Structuring, Refinement)           │           │
│  └────────────────────┬────────────────────────────────┘           │
│                       │                                             │
│              Structured Policy Document                             │
└────────────────────────┬───────────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────────┐
│  Phase 4: Evaluation                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────┐           │
│  │           Policy Evaluator                          │           │
│  │                                                      │           │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │           │
│  │  │   BLEU   │  │ ROUGE-L  │  │Compliance│         │           │
│  │  │  Score   │  │  Score   │  │  Score   │         │           │
│  │  └──────────┘  └──────────┘  └──────────┘         │           │
│  │                                                      │           │
│  │         Compare with Reference Policies             │           │
│  │                                                      │           │
│  └──────────────────────┬──────────────────────────────┘           │
│                         │                                           │
│                Evaluation Metrics & Report                          │
└────────────────────────┬───────────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────────┐
│  Phase 5: Reporting                                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────┐           │
│  │         Report Generator                            │           │
│  │                                                      │           │
│  │  • Executive Summary                                │           │
│  │  • Metrics Visualization                            │           │
│  │  • LLM Comparison                                   │           │
│  │  • Recommendations                                  │           │
│  │                                                      │           │
│  │  Output: PDF / Markdown / HTML                      │           │
│  └─────────────────────────────────────────────────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Source Code → Scanners → Vulnerabilities → Parser → Structured Data
                                                         ↓
Final Report ← Evaluator ← Generated Policy ← LLM ← Prompt Engine
```

## Component Interactions

### 1. Scanner → Parser
- **Input**: JSON/XML/HTML reports
- **Output**: Normalized vulnerability objects
- **Format**: `{id, severity, description, cwe, ...}`

### 2. Parser → Prompt Engine
- **Input**: List of vulnerabilities
- **Output**: Framework-specific prompt
- **Context**: NIST CSF / ISO 27001 / CIS

### 3. Prompt Engine → LLM
- **Input**: Formatted prompt with context
- **Output**: Raw policy text
- **Provider**: OpenAI / Anthropic / Ollama / etc.

### 4. LLM → Policy Orchestrator
- **Input**: Raw policy text
- **Output**: Structured policy document
- **Format**: JSON with metadata

### 5. Policy → Evaluator
- **Input**: Generated policy + Reference policies
- **Output**: Metric scores
- **Metrics**: BLEU, ROUGE-L, Compliance

## Integration Points

### CI/CD Integration
```
GitLab CI / GitHub Actions
    ↓
Security Scans (on commit)
    ↓
Policy Generation (automated)
    ↓
Evaluation & Report
    ↓
Artifact Storage
```

### API Integration
```
Application Code
    ↓
CLI Interface (main.py)
    ↓
    ├─→ scan()      → Scanner Orchestrator
    ├─→ generate()  → Policy Orchestrator
    └─→ evaluate()  → Evaluator
```

## Technology Stack

### Programming
- **Language**: Python 3.9+
- **CLI**: Click
- **Async**: asyncio (optional)

### Security Tools
- **SAST**: Bandit, SonarQube
- **SCA**: OWASP Dependency-Check, Safety
- **DAST**: OWASP ZAP

### AI/ML
- **LLMs**: OpenAI, Anthropic, Ollama, DeepSeek
- **NLP**: NLTK, spaCy
- **Metrics**: sacrebleu, rouge-score

### DevOps
- **CI/CD**: GitLab CI, GitHub Actions
- **Containers**: Docker
- **Cloud**: AWS, Azure (optional)

## Scalability Considerations

### Horizontal Scaling
- Multiple scanner instances
- Distributed LLM calls
- Batch processing

### Performance
- Async I/O for scanner coordination
- LLM request caching
- Parallel policy generation

### Storage
- Report archiving
- Policy versioning
- Metrics database

## Security & Privacy

### Data Protection
- Anonymize sensitive data
- Encrypt API keys
- Secure credential storage

### Access Control
- API rate limiting
- Authentication for CI/CD
- Audit logging

## Extensibility

### Adding New Scanner
1. Implement scanner class
2. Add to orchestrator
3. Update parser

### Adding New LLM
1. Create provider class
2. Implement `generate()` method
3. Register in LLM Manager

### Adding New Framework
1. Create prompt template
2. Add framework mapping
3. Update compliance checker

## Monitoring & Observability

### Logging
- Structured logging (loguru)
- Level-based filtering
- File rotation

### Metrics
- Scan duration
- LLM response time
- Policy generation success rate
- API costs

### Alerting
- Failed scans
- API errors
- Low quality scores
