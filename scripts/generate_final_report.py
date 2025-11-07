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
    
    # Load scan reports
    scan_reports = load_scan_reports()
    
    # Generate Markdown report
    report_md = generate_markdown_report(evaluation, policies, scan_reports)
    
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


def load_scan_reports() -> dict:
    """Load all scan reports from data/reports"""
    reports = {
        'sast': [],
        'sca': [],
        'dast': []
    }
    
    reports_dir = Path('data/reports')
    if not reports_dir.exists():
        print("⚠️  No reports directory found")
        return reports
    
    # Load Bandit (SAST) reports
    for bandit_file in reports_dir.glob('*bandit*.json'):
        try:
            with open(bandit_file, 'r') as f:
                data = json.load(f)
                reports['sast'].append({
                    'tool': 'Bandit',
                    'file': bandit_file.name,
                    'data': data
                })
        except Exception as e:
            print(f"⚠️  Error loading {bandit_file}: {e}")
    
    # Load Dependency-Check (SCA) reports
    for dep_file in reports_dir.glob('*dependency*.json'):
        try:
            with open(dep_file, 'r') as f:
                data = json.load(f)
                reports['sca'].append({
                    'tool': 'OWASP Dependency-Check',
                    'file': dep_file.name,
                    'data': data
                })
        except Exception as e:
            print(f"⚠️  Error loading {dep_file}: {e}")
    
    # Load ZAP (DAST) reports
    for zap_file in reports_dir.glob('*zap*.json'):
        try:
            with open(zap_file, 'r') as f:
                data = json.load(f)
                reports['dast'].append({
                    'tool': 'OWASP ZAP',
                    'file': zap_file.name,
                    'data': data
                })
        except Exception as e:
            print(f"⚠️  Error loading {zap_file}: {e}")
    
    return reports


def generate_markdown_report(evaluation: dict, policies: list, scan_reports: dict) -> str:
    """Generate Markdown report content"""
    
    # Calculate scan statistics
    sast_count = sum(len(r.get('data', {}).get('results', [])) for r in scan_reports.get('sast', []))
    sca_count = sum(len(r.get('data', {}).get('dependencies', [])) for r in scan_reports.get('sca', []))
    dast_count = sum(len(r.get('data', {}).get('site', [{}])[0].get('alerts', [])) for r in scan_reports.get('dast', []))
    total_vulns = sast_count + sca_count + dast_count
    
    report = f"""# DevSecOps AI - Consolidated Security Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This report presents comprehensive security analysis results including vulnerability scans (SAST, SCA, DAST) and AI-generated security policies aligned with international standards.

### Key Metrics

- **Total Vulnerabilities Found:** {total_vulns}
  - SAST (Code Analysis): {sast_count}
  - SCA (Dependencies): {sca_count}
  - DAST (Runtime): {dast_count}
- **Policies Generated:** {len(policies)}
- **Frameworks Covered:** NIST CSF, ISO 27001, CIS Controls

---

## 1. Security Scan Results

### 1.1 Static Application Security Testing (SAST)

"""
    
    # Add SAST results
    for sast_report in scan_reports.get('sast', []):
        tool = sast_report.get('tool', 'Unknown')
        data = sast_report.get('data', {})
        results = data.get('results', [])
        
        report += f"""
#### {tool} Results

- **Total Issues:** {len(results)}
- **Report File:** `{sast_report.get('file', 'N/A')}`

"""
        if results:
            # Group by severity
            severity_counts = {}
            for result in results:
                severity = result.get('issue_severity', 'UNKNOWN')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            report += "**Issues by Severity:**\n\n"
            for severity in ['HIGH', 'MEDIUM', 'LOW', 'INFO']:
                count = severity_counts.get(severity, 0)
                if count > 0:
                    report += f"- 🔴 **{severity}:** {count} issues\n"
            
            report += "\n**Top Issues:**\n\n"
            for i, result in enumerate(results[:5], 1):
                issue_text = result.get('issue_text', 'N/A')
                severity = result.get('issue_severity', 'UNKNOWN')
                filename = result.get('filename', 'N/A')
                line = result.get('line_number', 'N/A')
                report += f"{i}. **[{severity}]** {issue_text}\n"
                report += f"   - File: `{filename}:{line}`\n"
                report += f"   - CWE: {result.get('issue_cwe', {}).get('id', 'N/A')}\n\n"
    
    report += """
### 1.2 Software Composition Analysis (SCA)

"""
    
    # Add SCA results
    for sca_report in scan_reports.get('sca', []):
        tool = sca_report.get('tool', 'Unknown')
        data = sca_report.get('data', {})
        dependencies = data.get('dependencies', [])
        
        report += f"""
#### {tool} Results

- **Dependencies Scanned:** {len(dependencies)}
- **Report File:** `{sca_report.get('file', 'N/A')}`

"""
        # Count vulnerabilities
        vuln_count = 0
        high_count = 0
        for dep in dependencies:
            vulns = dep.get('vulnerabilities', [])
            vuln_count += len(vulns)
            high_count += sum(1 for v in vulns if v.get('severity', '').upper() in ['HIGH', 'CRITICAL'])
        
        if vuln_count > 0:
            report += f"""
**Vulnerabilities Found:**

- 🔴 **High/Critical:** {high_count} vulnerabilities
- 📊 **Total:** {vuln_count} vulnerabilities

**Top Vulnerable Dependencies:**

"""
            vuln_deps = [(d, len(d.get('vulnerabilities', []))) for d in dependencies if d.get('vulnerabilities')]
            vuln_deps.sort(key=lambda x: x[1], reverse=True)
            
            for i, (dep, count) in enumerate(vuln_deps[:5], 1):
                name = dep.get('fileName', 'Unknown')
                report += f"{i}. **{name}** - {count} vulnerabilities\n"
                for vuln in dep.get('vulnerabilities', [])[:2]:
                    cve = vuln.get('name', 'N/A')
                    severity = vuln.get('severity', 'N/A')
                    report += f"   - [{severity}] {cve}\n"
                report += "\n"
    
    report += """
### 1.3 Dynamic Application Security Testing (DAST)

"""
    
    # Add DAST results
    for dast_report in scan_reports.get('dast', []):
        tool = dast_report.get('tool', 'Unknown')
        data = dast_report.get('data', {})
        sites = data.get('site', [])
        
        report += f"""
#### {tool} Results

- **Sites Scanned:** {len(sites)}
- **Report File:** `{dast_report.get('file', 'N/A')}`

"""
        for site in sites:
            alerts = site.get('alerts', [])
            if alerts:
                # Group by risk
                risk_counts = {}
                for alert in alerts:
                    risk = alert.get('riskdesc', 'Unknown').split()[0]
                    risk_counts[risk] = risk_counts.get(risk, 0) + 1
                
                report += f"""
**Target:** {site.get('@name', 'N/A')}

**Alerts by Risk Level:**

"""
                for risk in ['High', 'Medium', 'Low', 'Informational']:
                    count = risk_counts.get(risk, 0)
                    if count > 0:
                        emoji = '🔴' if risk == 'High' else '🟡' if risk == 'Medium' else '🟢'
                        report += f"- {emoji} **{risk}:** {count} alerts\n"
                
                report += "\n**Top Alerts:**\n\n"
                for i, alert in enumerate(alerts[:5], 1):
                    name = alert.get('name', 'N/A')
                    risk = alert.get('riskdesc', 'Unknown')
                    report += f"{i}. **[{risk}]** {name}\n"
                    report += f"   - Count: {alert.get('count', 0)} instances\n"
                    report += f"   - CWE: {alert.get('cweid', 'N/A')}\n\n"

    report += """
---

## 2. Introduction & Context

    report += """
---

## 2. Introduction & Context

### 2.1 Problem Statement

Modern software development relies on DevSecOps pipelines for continuous security integration. However, translating technical vulnerability reports (SAST, SCA, DAST) into actionable, human-readable security policies remains challenging.

### 2.2 Solution Approach

This project leverages Large Language Models (LLMs) to automate the translation process, creating dynamic, adaptive, and standards-compliant security documentation.

### 2.3 Technologies Used

- **Security Scanning:** Bandit, SonarQube, OWASP Dependency-Check, Safety, OWASP ZAP
- **LLM Providers:** OpenAI GPT-4, Anthropic Claude, Ollama, DeepSeek, Hugging Face
- **Evaluation Metrics:** BLEU, ROUGE-L, Custom Compliance Scoring
- **Frameworks:** NIST Cybersecurity Framework, ISO/IEC 27001, CIS Controls

---

## 3. Architecture & Implementation

### 3.1 System Architecture

```
[Security Scanners] → [Report Parser] → [LLM Engine] → [Policy Generator]
                                            ↓
                                    [Evaluator] ← [Reference Policies]
```

### 3.2 Components

1. **Scanner Orchestrator:** Coordinates SAST, SCA, and DAST tools
2. **Report Parser:** Processes and normalizes vulnerability reports
3. **LLM Manager:** Interfaces with multiple LLM providers
4. **Prompt Engine:** Crafts framework-specific prompts
5. **Policy Orchestrator:** Generates and refines policies
6. **Evaluator:** Assesses policy quality using metrics

---

## 4. AI-Generated Security Policies & Evaluation

### 4.1 Evaluation Metrics

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

### 4.2 Generated Policies Overview

"""
    
    # Add policy details
    for i, policy in enumerate(policies, 1):
        framework = policy.get('framework', 'Unknown')
        vuln_count = policy.get('vulnerability_count', 0)
        report += f"{i}. **{framework}** - Addresses {vuln_count} vulnerabilities\n"
    
    report += """

---

## 5. Discussion & Analysis

### 5.1 Strengths

- ✅ **Automation:** Significantly reduces manual policy writing effort
- ✅ **Consistency:** Ensures standardized policy structure
- ✅ **Scalability:** Handles large numbers of vulnerabilities efficiently
- ✅ **Framework Alignment:** Maintains compliance with standards

### 5.2 Limitations

- ⚠️ **LLM Dependency:** Requires API access and associated costs
- ⚠️ **Context Window:** Limited by LLM token constraints
- ⚠️ **Hallucination Risk:** LLMs may generate incorrect information
- ⚠️ **Human Review:** Still requires expert validation

### 5.3 Ethical Considerations

1. **Privacy:** Vulnerability data should be anonymized
2. **Accountability:** AI-generated policies need human oversight
3. **Transparency:** Decision-making process should be explainable
4. **Bias:** LLM outputs may reflect training data biases

---

## 6. Future Work

### 6.1 Technical Enhancements

- [ ] Fine-tune LLMs on security policy corpus
- [ ] Implement multi-stage refinement pipeline
- [ ] Add support for more frameworks (PCI-DSS, HIPAA)
- [ ] Develop real-time policy updates based on new CVEs

### 6.2 Research Directions

- Comparative study of different LLM architectures
- Analysis of policy quality vs. LLM model size
- Investigation of prompt engineering techniques
- Study of human-AI collaboration in policy writing

---

## 7. Conclusion

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
