#!/usr/bin/env python3
"""
Simple Final Report Generator
Creates a consolidated Markdown report from all security scans
"""

import json
import os
from pathlib import Path
from datetime import datetime


def create_final_report(output_path="output/FINAL_SECURITY_REPORT.md"):
    """Generate a consolidated security report"""
    
    report = []
    
    # Header
    report.append("# 🔐 DevSecOps Security Report\n")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("---\n\n")
    
    # Executive Summary
    report.append("## 📊 Executive Summary\n\n")
    
    # Count vulnerabilities
    total_vulns = 0
    high_vulns = 0
    
    # Scan reports directory
    reports_dir = Path("data/reports")
    if reports_dir.exists():
        report.append(f"**Reports analyzed:** {len(list(reports_dir.glob('*.json')))} files\n\n")
        
        # Analyze each report
        for report_file in reports_dir.glob("*.json"):
            try:
                with open(report_file, 'r') as f:
                    data = json.load(f)
                    
                    # Count issues based on report type
                    if 'results' in data:  # Bandit format
                        issues = data['results']
                        total_vulns += len(issues)
                        high_vulns += sum(1 for i in issues if i.get('issue_severity') in ['HIGH', 'CRITICAL'])
                    
                    elif 'dependencies' in data:  # Dependency-Check format
                        for dep in data.get('dependencies', []):
                            vulns = dep.get('vulnerabilities', [])
                            total_vulns += len(vulns)
                            high_vulns += sum(1 for v in vulns if v.get('severity', '').upper() in ['HIGH', 'CRITICAL'])
                    
                    elif 'site' in data:  # ZAP format
                        for site in data.get('site', []):
                            alerts = site.get('alerts', [])
                            total_vulns += len(alerts)
                            high_vulns += sum(1 for a in alerts if 'High' in a.get('riskdesc', ''))
                            
            except Exception as e:
                print(f"Warning: Could not parse {report_file}: {e}")
    
    report.append(f"- **Total Vulnerabilities Found:** {total_vulns}\n")
    report.append(f"- **High/Critical Severity:** {high_vulns}\n")
    report.append(f"- **Medium/Low Severity:** {total_vulns - high_vulns}\n\n")
    
    # Scan Results Section
    report.append("---\n\n")
    report.append("## 🔍 Detailed Scan Results\n\n")
    
    # SAST Results
    report.append("### 1. Static Analysis (SAST)\n\n")
    bandit_files = list(reports_dir.glob("*bandit*.json")) if reports_dir.exists() else []
    if bandit_files:
        for bandit_file in bandit_files:
            try:
                with open(bandit_file, 'r') as f:
                    data = json.load(f)
                    results = data.get('results', [])
                    report.append(f"**Report:** `{bandit_file.name}`\n")
                    report.append(f"- Issues found: {len(results)}\n\n")
                    
                    if results:
                        report.append("**Top Issues:**\n\n")
                        for i, issue in enumerate(results[:5], 1):
                            severity = issue.get('issue_severity', 'UNKNOWN')
                            text = issue.get('issue_text', 'N/A')
                            filename = issue.get('filename', 'N/A')
                            line = issue.get('line_number', 'N/A')
                            report.append(f"{i}. **[{severity}]** {text}\n")
                            report.append(f"   - Location: `{filename}:{line}`\n\n")
            except Exception as e:
                report.append(f"⚠️ Could not parse {bandit_file.name}: {e}\n\n")
    else:
        report.append("_No SAST reports found_\n\n")
    
    # SCA Results
    report.append("### 2. Dependency Analysis (SCA)\n\n")
    dep_files = list(reports_dir.glob("*dependency*.json")) if reports_dir.exists() else []
    if dep_files:
        for dep_file in dep_files:
            try:
                with open(dep_file, 'r') as f:
                    data = json.load(f)
                    dependencies = data.get('dependencies', [])
                    report.append(f"**Report:** `{dep_file.name}`\n")
                    report.append(f"- Dependencies scanned: {len(dependencies)}\n\n")
                    
                    vuln_deps = [d for d in dependencies if d.get('vulnerabilities')]
                    if vuln_deps:
                        report.append("**Vulnerable Dependencies:**\n\n")
                        for i, dep in enumerate(vuln_deps[:5], 1):
                            name = dep.get('fileName', 'Unknown')
                            vulns = dep.get('vulnerabilities', [])
                            report.append(f"{i}. **{name}** - {len(vulns)} vulnerabilities\n")
                            for vuln in vulns[:2]:
                                cve = vuln.get('name', 'N/A')
                                severity = vuln.get('severity', 'N/A')
                                report.append(f"   - [{severity}] {cve}\n")
                            report.append("\n")
            except Exception as e:
                report.append(f"⚠️ Could not parse {dep_file.name}: {e}\n\n")
    else:
        report.append("_No SCA reports found_\n\n")
    
    # DAST Results
    report.append("### 3. Runtime Testing (DAST)\n\n")
    zap_files = list(reports_dir.glob("*zap*.json")) if reports_dir.exists() else []
    if zap_files:
        for zap_file in zap_files:
            try:
                with open(zap_file, 'r') as f:
                    data = json.load(f)
                    sites = data.get('site', [])
                    report.append(f"**Report:** `{zap_file.name}`\n")
                    
                    for site in sites:
                        alerts = site.get('alerts', [])
                        report.append(f"- Alerts found: {len(alerts)}\n\n")
                        
                        if alerts:
                            report.append("**Top Alerts:**\n\n")
                            for i, alert in enumerate(alerts[:5], 1):
                                name = alert.get('name', 'N/A')
                                risk = alert.get('riskdesc', 'Unknown')
                                count = alert.get('count', 0)
                                report.append(f"{i}. **[{risk}]** {name}\n")
                                report.append(f"   - Instances: {count}\n\n")
            except Exception as e:
                report.append(f"⚠️ Could not parse {zap_file.name}: {e}\n\n")
    else:
        report.append("_No DAST reports found_\n\n")
    
    # Generated Policies
    report.append("---\n\n")
    report.append("## 📋 Generated Security Policies\n\n")
    
    policies_dir = Path("output/generated_policies")
    if policies_dir.exists():
        policy_files = list(policies_dir.glob("*.json"))
        report.append(f"**Total policies generated:** {len(policy_files)}\n\n")
        
        for policy_file in policy_files:
            try:
                with open(policy_file, 'r') as f:
                    policy = json.load(f)
                    framework = policy.get('framework', 'Unknown')
                    report.append(f"- **{framework}** (`{policy_file.name}`)\n")
            except Exception as e:
                report.append(f"- `{policy_file.name}` (parse error)\n")
    else:
        report.append("_No policies generated yet_\n\n")
    
    # Evaluation Metrics
    report.append("\n---\n\n")
    report.append("## 📈 Quality Metrics\n\n")
    
    eval_file = Path("output/evaluation_results/summary.json")
    if eval_file.exists():
        try:
            with open(eval_file, 'r') as f:
                evaluation = json.load(f)
                metrics = evaluation.get('metrics', {})
                
                if 'BLEU' in metrics:
                    report.append(f"- **BLEU Score:** {metrics['BLEU']:.4f}\n")
                if 'ROUGE-L' in metrics:
                    report.append(f"- **ROUGE-L Score:** {metrics['ROUGE-L']:.4f}\n")
                if 'COMPLIANCE' in metrics:
                    report.append(f"- **Compliance Score:** {metrics['COMPLIANCE']:.4f}\n")
        except Exception as e:
            report.append(f"_Could not load evaluation metrics: {e}_\n")
    else:
        report.append("_No evaluation metrics available_\n")
    
    # Recommendations
    report.append("\n---\n\n")
    report.append("## 💡 Recommendations\n\n")
    
    if high_vulns > 10:
        report.append("- ⚠️ **CRITICAL**: High number of critical vulnerabilities detected. Immediate action required.\n")
    elif high_vulns > 5:
        report.append("- ⚠️ **WARNING**: Several high-severity issues found. Plan remediation.\n")
    else:
        report.append("- ✅ **GOOD**: Manageable number of critical issues.\n")
    
    report.append("- 📚 Review generated security policies\n")
    report.append("- 🔄 Update vulnerable dependencies\n")
    report.append("- 🔍 Run scans regularly (weekly recommended)\n")
    
    # Footer
    report.append("\n---\n\n")
    report.append("**Generated by DevSecOps AI Pipeline**\n")
    report.append(f"**Report Location:** `{output_path}`\n")
    
    # Write report
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(''.join(report))
    
    print(f"✅ Final report generated: {output_file}")
    print(f"📄 File size: {output_file.stat().st_size} bytes")
    
    return str(output_file)


if __name__ == "__main__":
    create_final_report()
