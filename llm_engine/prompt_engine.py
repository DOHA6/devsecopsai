"""
Prompt Engineering Module
Crafts effective prompts for security policy generation
"""

from typing import Dict, List
from jinja2 import Template


class PromptEngine:
    """Generates prompts for LLM-based policy creation"""
    
    def __init__(self, framework: str = "NIST_CSF"):
        self.framework = framework
        self.templates = {
            'NIST_CSF': self._get_nist_template(),
            'ISO_27001': self._get_iso_template(),
            'CIS_CONTROLS': self._get_cis_template()
        }
    
    def generate_policy_prompt(self, vulnerabilities: List[Dict]) -> str:
        """
        Generate prompt for creating security policy from vulnerabilities
        
        Args:
            vulnerabilities: List of vulnerability data
        
        Returns:
            Formatted prompt string
        """
        template = self.templates.get(self.framework)
        if not template:
            raise ValueError(f"Unknown framework: {self.framework}")
        
        # Prepare vulnerability summary
        vuln_summary = self._summarize_vulnerabilities(vulnerabilities)
        
        # Render template
        return template.render(
            framework=self.framework,
            vulnerabilities=vulnerabilities,
            summary=vuln_summary,
            total_count=len(vulnerabilities)
        )
    
    def generate_refinement_prompt(self, draft_policy: str, vulnerabilities: List[Dict]) -> str:
        """Generate prompt for refining/validating a policy"""
        template = Template("""
You are a cybersecurity compliance expert. Review and refine the following security policy.

Original Vulnerabilities Found:
{{ summary }}

Draft Policy:
{{ draft_policy }}

Task: Refine this policy to:
1. Ensure all critical vulnerabilities are addressed
2. Align with {{ framework }} requirements
3. Use clear, professional language
4. Include specific remediation guidance
5. Ensure completeness and accuracy

Provide the refined policy in a structured format.
""")
        
        vuln_summary = self._summarize_vulnerabilities(vulnerabilities)
        
        return template.render(
            draft_policy=draft_policy,
            framework=self.framework,
            summary=vuln_summary
        )
    
    def _summarize_vulnerabilities(self, vulnerabilities: List[Dict]) -> str:
        """Create a concise summary of vulnerabilities"""
        if not vulnerabilities:
            return "No vulnerabilities found."
        
        # Group by severity
        by_severity = {}
        by_category = {}
        
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'UNKNOWN')
            category = vuln.get('category', 'UNKNOWN')
            
            by_severity[severity] = by_severity.get(severity, 0) + 1
            by_category[category] = by_category.get(category, 0) + 1
        
        summary = f"Total Vulnerabilities: {len(vulnerabilities)}\n\n"
        summary += "By Severity:\n"
        for severity, count in sorted(by_severity.items(), key=lambda x: x[1], reverse=True):
            summary += f"  - {severity}: {count}\n"
        
        summary += "\nBy Category:\n"
        for category, count in by_category.items():
            summary += f"  - {category}: {count}\n"
        
        # List top issues
        summary += "\nKey Vulnerabilities:\n"
        for i, vuln in enumerate(vulnerabilities[:10], 1):
            title = vuln.get('title', 'Unknown')
            severity = vuln.get('severity', 'UNKNOWN')
            summary += f"  {i}. [{severity}] {title}\n"
        
        if len(vulnerabilities) > 10:
            summary += f"  ... and {len(vulnerabilities) - 10} more\n"
        
        return summary
    
    def _get_nist_template(self) -> Template:
        """NIST Cybersecurity Framework prompt template"""
        return Template("""
You are an expert in cybersecurity policy writing and the NIST Cybersecurity Framework (CSF).

Context:
A security assessment has identified vulnerabilities in a software system. Your task is to generate a comprehensive security policy document that addresses these findings while aligning with NIST CSF.

Vulnerability Summary:
{{ summary }}

Detailed Vulnerabilities:
{% for vuln in vulnerabilities[:20] %}
- ID: {{ vuln.id }}
  Title: {{ vuln.title }}
  Severity: {{ vuln.severity }}
  Description: {{ vuln.description }}
  Category: {{ vuln.category }}
{% endfor %}

Task:
Generate a structured security policy document that:

1. **Identifies** the risks and vulnerabilities (NIST: Identify function)
2. **Protects** systems through security controls (NIST: Protect function)
3. **Detects** security events and anomalies (NIST: Detect function)
4. **Responds** to identified security incidents (NIST: Respond function)
5. **Recovers** from security incidents (NIST: Recover function)

Format the policy with:
- Executive Summary
- Risk Assessment
- Security Controls (mapped to NIST CSF)
- Remediation Recommendations
- Implementation Timeline
- Monitoring and Review Procedures

Use professional, clear language suitable for both technical and non-technical stakeholders.
""")
    
    def _get_iso_template(self) -> Template:
        """ISO/IEC 27001 prompt template"""
        return Template("""
You are an expert in information security management and ISO/IEC 27001:2022.

Context:
A security assessment has identified vulnerabilities in an information system. Generate a security policy that addresses these issues in accordance with ISO 27001 requirements.

Vulnerability Summary:
{{ summary }}

Detailed Vulnerabilities:
{% for vuln in vulnerabilities[:20] %}
- ID: {{ vuln.id }}
  Title: {{ vuln.title }}
  Severity: {{ vuln.severity }}
  Description: {{ vuln.description }}
  Category: {{ vuln.category }}
{% endfor %}

Task:
Generate an ISO 27001-compliant security policy that includes:

1. **Scope and Objectives** (Clause 4)
2. **Information Security Policy** (Clause 5)
3. **Risk Assessment** (Clause 6)
4. **Security Controls** mapped to Annex A controls:
   - A.5: Organizational controls
   - A.6: People controls
   - A.7: Physical controls
   - A.8: Technological controls
5. **Implementation Plan**
6. **Monitoring and Measurement** (Clause 9)
7. **Continual Improvement** (Clause 10)

Format the policy professionally with clear structure, objectives, and actionable controls.
""")
    
    def _get_cis_template(self) -> Template:
        """CIS Controls prompt template"""
        return Template("""
You are an expert in cybersecurity best practices and CIS Critical Security Controls.

Context:
Security vulnerabilities have been identified. Generate a policy document that addresses these using CIS Controls framework.

Vulnerability Summary:
{{ summary }}

Detailed Vulnerabilities:
{% for vuln in vulnerabilities[:20] %}
- ID: {{ vuln.id }}
  Title: {{ vuln.title }}
  Severity: {{ vuln.severity }}
  Description: {{ vuln.description }}
  Category: {{ vuln.category }}
{% endfor %}

Task:
Generate a security policy mapped to relevant CIS Controls v8:

Focus on applicable controls such as:
- CIS Control 1: Inventory and Control of Enterprise Assets
- CIS Control 2: Inventory and Control of Software Assets
- CIS Control 3: Data Protection
- CIS Control 4: Secure Configuration
- CIS Control 5: Account Management
- CIS Control 6: Access Control Management
- CIS Control 7: Continuous Vulnerability Management
- CIS Control 8: Audit Log Management
- CIS Control 16: Application Software Security

Provide:
1. Policy Overview
2. Identified Risks
3. Security Controls (mapped to specific CIS Controls)
4. Implementation Guidance
5. Verification and Validation Methods

Use clear, actionable language appropriate for IT security teams.
""")
