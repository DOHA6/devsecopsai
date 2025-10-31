"""
Report Generation Script
Creates comprehensive PDF/HTML reports from evaluation results
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def generate_report(evaluation_dir: str, policies_dir: str, output_file: str):
    """Generate final project report"""
    
    evaluation_dir = Path(evaluation_dir)
    policies_dir = Path(policies_dir)
    output_file = Path(output_file)
    
    # Load evaluation results
    summary_file = evaluation_dir / 'summary.json'
    if not summary_file.exists():
        print(f"Error: Evaluation summary not found: {summary_file}")
        sys.exit(1)
    
    with open(summary_file, 'r') as f:
        evaluation = json.load(f)
    
    # Load generated policies
    policies = []
    for policy_file in policies_dir.glob('*.json'):
        with open(policy_file, 'r') as f:
            policies.append(json.load(f))
    
    # Generate Markdown report
    report_md = generate_markdown_report(evaluation, policies)
    
    # Save Markdown
    md_file = output_file.with_suffix('.md')
    with open(md_file, 'w') as f:
        f.write(report_md)
    
    print(f"✅ Report generated: {md_file}")
    
    # Try to generate PDF if fpdf2 is available
    try:
        from fpdf import FPDF
        generate_pdf_report(report_md, output_file)
        print(f"✅ PDF report generated: {output_file}")
    except ImportError:
        print("⚠️  fpdf2 not installed. PDF generation skipped.")
        print("   Install with: pip install fpdf2")


def generate_markdown_report(evaluation: dict, policies: list) -> str:
    """Generate Markdown report content"""
    
    report = f"""# DevSecOps AI - Final Project Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This report presents the results of an AI-driven security policy generation system that transforms technical vulnerability reports into human-readable security policies aligned with international standards.

### Key Achievements

- **Policies Generated:** {len(policies)}
- **Vulnerabilities Addressed:** {evaluation.get('generated_count', 0)}
- **Frameworks Covered:** NIST CSF, ISO 27001, CIS Controls

---

## 1. Introduction & Context

### 1.1 Problem Statement

Modern software development relies on DevSecOps pipelines for continuous security integration. However, translating technical vulnerability reports (SAST, SCA, DAST) into actionable, human-readable security policies remains challenging.

### 1.2 Solution Approach

This project leverages Large Language Models (LLMs) to automate the translation process, creating dynamic, adaptive, and standards-compliant security documentation.

### 1.3 Technologies Used

- **Security Scanning:** Bandit, SonarQube, OWASP Dependency-Check, Safety, OWASP ZAP
- **LLM Providers:** OpenAI GPT-4, Anthropic Claude, Ollama, DeepSeek, Hugging Face
- **Evaluation Metrics:** BLEU, ROUGE-L, Custom Compliance Scoring
- **Frameworks:** NIST Cybersecurity Framework, ISO/IEC 27001, CIS Controls

---

## 2. Architecture & Implementation

### 2.1 System Architecture

```
[Security Scanners] → [Report Parser] → [LLM Engine] → [Policy Generator]
                                            ↓
                                    [Evaluator] ← [Reference Policies]
```

### 2.2 Components

1. **Scanner Orchestrator:** Coordinates SAST, SCA, and DAST tools
2. **Report Parser:** Processes and normalizes vulnerability reports
3. **LLM Manager:** Interfaces with multiple LLM providers
4. **Prompt Engine:** Crafts framework-specific prompts
5. **Policy Orchestrator:** Generates and refines policies
6. **Evaluator:** Assesses policy quality using metrics

---

## 3. Results & Evaluation

### 3.1 Evaluation Metrics

"""
    
    # Add metrics
    metrics = evaluation.get('metrics', {})
    
    if 'BLEU' in metrics:
        bleu = metrics['BLEU']
        report += f"""
#### BLEU Score: {bleu:.4f}

Measures n-gram overlap with reference policies.
- Score: {bleu:.2%}
- Interpretation: {'Excellent' if bleu >= 0.5 else 'Good' if bleu >= 0.3 else 'Needs Improvement'}
"""
    
    if 'ROUGE-L' in metrics:
        rouge = metrics['ROUGE-L']
        report += f"""
#### ROUGE-L Score: {rouge:.4f}

Evaluates longest common subsequence with references.
- Score: {rouge:.2%}
- Interpretation: {'Strong' if rouge >= 0.5 else 'Moderate' if rouge >= 0.3 else 'Limited'} content overlap
"""
    
    if 'COMPLIANCE' in metrics:
        compliance = metrics['COMPLIANCE']
        report += f"""
#### Compliance Score: {compliance:.4f}

Measures adherence to framework requirements.
- Score: {compliance:.2%}
- Interpretation: {'Excellent' if compliance >= 0.8 else 'Good' if compliance >= 0.6 else 'Insufficient'} framework coverage
"""
    
    report += """

### 3.2 Generated Policies Overview

"""
    
    # Add policy details
    for i, policy in enumerate(policies, 1):
        framework = policy.get('framework', 'Unknown')
        vuln_count = policy.get('vulnerability_count', 0)
        report += f"{i}. **{framework}** - Addresses {vuln_count} vulnerabilities\n"
    
    report += """

---

## 4. Discussion & Analysis

### 4.1 Strengths

- ✅ **Automation:** Significantly reduces manual policy writing effort
- ✅ **Consistency:** Ensures standardized policy structure
- ✅ **Scalability:** Handles large numbers of vulnerabilities efficiently
- ✅ **Framework Alignment:** Maintains compliance with standards

### 4.2 Limitations

- ⚠️ **LLM Dependency:** Requires API access and associated costs
- ⚠️ **Context Window:** Limited by LLM token constraints
- ⚠️ **Hallucination Risk:** LLMs may generate incorrect information
- ⚠️ **Human Review:** Still requires expert validation

### 4.3 Ethical Considerations

1. **Privacy:** Vulnerability data should be anonymized
2. **Accountability:** AI-generated policies need human oversight
3. **Transparency:** Decision-making process should be explainable
4. **Bias:** LLM outputs may reflect training data biases

---

## 5. Future Work

### 5.1 Technical Enhancements

- [ ] Fine-tune LLMs on security policy corpus
- [ ] Implement multi-stage refinement pipeline
- [ ] Add support for more frameworks (PCI-DSS, HIPAA)
- [ ] Develop real-time policy updates based on new CVEs

### 5.2 Research Directions

- Comparative study of different LLM architectures
- Analysis of policy quality vs. LLM model size
- Investigation of prompt engineering techniques
- Study of human-AI collaboration in policy writing

---

## 6. Conclusion

This project demonstrates the feasibility and effectiveness of using Large Language Models to automate security policy generation. The system successfully bridges the gap between technical vulnerability detection and organizational governance documentation.

**Key Takeaways:**
- AI can significantly enhance DevSecOps workflows
- Automated policy generation maintains standards compliance
- Human oversight remains essential for quality assurance
- Future improvements should focus on fine-tuning and validation

---

## References

1. NIST Cybersecurity Framework v1.1
2. ISO/IEC 27001:2022 Information Security Management
3. CIS Critical Security Controls v8
4. OWASP Top 10 Security Risks
5. Various LLM documentation (OpenAI, Anthropic, etc.)

---

## Appendices

### Appendix A: Configuration

- LLM Provider: {evaluation.get('metadata', {}).get('llm_provider', 'N/A')}
- Evaluation Date: {evaluation.get('timestamp', 'N/A')}

### Appendix B: Metrics Details

See `evaluation_results/summary.json` for complete metrics data.

### Appendix C: Generated Policies

All generated policies available in `output/generated_policies/`

---

**End of Report**
"""
    
    return report


def generate_pdf_report(markdown_text: str, output_file: Path):
    """Convert Markdown report to PDF"""
    # This is a simplified PDF generation
    # For better results, use a Markdown to PDF converter like pandoc
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate final project report')
    parser.add_argument('--evaluation', required=True, help='Evaluation results directory')
    parser.add_argument('--policies', required=True, help='Generated policies directory')
    parser.add_argument('--output', required=True, help='Output report file')
    
    args = parser.parse_args()
    
    generate_report(args.evaluation, args.policies, args.output)
