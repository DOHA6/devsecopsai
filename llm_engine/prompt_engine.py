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
        """Generate prompt for refining/validating a policy - Optimized"""
        template = Template("""
Refine this {{ framework }} security policy:

{{ draft_policy }}

Issues: {{ summary }}

Make it:
1. Cover critical vulnerabilities
2. {{ framework }}-compliant
3. Clear and actionable

Be concise.
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
        """NIST Cybersecurity Framework prompt template - Optimized for speed"""
        return Template("""
Generate a NIST CSF security policy for these vulnerabilities.

Summary: {{ summary }}

Top Issues:
{% for vuln in vulnerabilities[:10] %}
- [{{ vuln.severity }}] {{ vuln.title }}
{% endfor %}

Include:
1. Risk Assessment (Identify)
2. Security Controls (Protect/Detect)
3. Response Plan (Respond/Recover)
4. Remediation Steps

Be concise and actionable.
""")
    
    def _get_iso_template(self) -> Template:
        """ISO/IEC 27001 prompt template - Optimized for speed"""
        return Template("""
Generate an ISO 27001 security policy.

Summary: {{ summary }}

Top Issues:
{% for vuln in vulnerabilities[:10] %}
- [{{ vuln.severity }}] {{ vuln.title }}
{% endfor %}

Include:
1. Scope & Risk Assessment
2. Annex A Controls (A.5-A.8)
3. Implementation Plan
4. Monitoring

Be concise.
""")
    
    def _get_cis_template(self) -> Template:
        """CIS Controls prompt template - Optimized for speed"""
        return Template("""
Generate a CIS Controls v8 security policy.

Summary: {{ summary }}

Top Issues:
{% for vuln in vulnerabilities[:10] %}
- [{{ vuln.severity }}] {{ vuln.title }}
{% endfor %}

Map to CIS Controls (1-8, 16):
1. Asset Management
2. Software Control
3. Data Protection
4. Secure Configuration
5. Access Control
6. Vulnerability Management

Include implementation guidance. Be concise.
""")
