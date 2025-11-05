"""
Vulnerability Report Parser
Processes and normalizes reports from different security tools
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Union
from loguru import logger
import xmltodict
from bs4 import BeautifulSoup


class ReportParser:
    """Parses vulnerability reports from various security tools"""
    
    def __init__(self):
        self.parsers = {
            'bandit': self._parse_bandit,
            'dependency_check': self._parse_dependency_check,
            'safety': self._parse_safety,
            'zap': self._parse_zap
        }
    
    def parse_file(self, file_path: Union[str, Path]) -> Dict:
        """
        Parse a single vulnerability report file
        
        Args:
            file_path: Path to report file
        
        Returns:
            Normalized vulnerability data
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Report file not found: {file_path}")
        
        # Detect report type from filename
        report_type = self._detect_report_type(file_path)
        
        if report_type not in self.parsers:
            logger.warning(f"Unknown report type: {report_type}")
            return self._parse_generic(file_path)
        
        logger.info(f"Parsing {report_type} report: {file_path}")
        return self.parsers[report_type](file_path)
    
    def parse_directory(self, directory: Union[str, Path]) -> List[Dict]:
        """Parse all report files in a directory"""
        directory = Path(directory)
        parsed_reports = []
        
        # Find all JSON, XML, and HTML files
        for pattern in ['*.json', '*.xml', '*.html']:
            for file_path in directory.glob(pattern):
                try:
                    parsed = self.parse_file(file_path)
                    if parsed:
                        parsed_reports.append(parsed)
                except Exception as e:
                    logger.error(f"Failed to parse {file_path}: {e}")
        
        return parsed_reports
    
    def _detect_report_type(self, file_path: Path) -> str:
        """Detect report type from filename"""
        name = file_path.name.lower()
        
        if 'bandit' in name:
            return 'bandit'
        elif 'dependency' in name or 'owasp' in name:
            return 'dependency_check'
        elif 'safety' in name:
            return 'safety'
        elif 'zap' in name:
            return 'zap'
        
        return 'unknown'
    
    def _parse_bandit(self, file_path: Path) -> Dict:
        """Parse Bandit JSON report"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        vulnerabilities = []
        for result in data.get('results', []):
            vulnerabilities.append({
                'id': result.get('test_id'),
                'title': result.get('test_name'),
                'description': result.get('issue_text'),
                'severity': result.get('issue_severity'),
                'confidence': result.get('issue_confidence'),
                'file': result.get('filename'),
                'line': result.get('line_number'),
                'code': result.get('code'),
                'cwe': result.get('cwe', {}).get('id') if result.get('cwe') else None,
                'tool': 'bandit',
                'category': 'SAST'
            })
        
        return {
            'tool': 'bandit',
            'category': 'SAST',
            'timestamp': data.get('generated_at'),
            'metrics': data.get('metrics'),
            'vulnerabilities': vulnerabilities
        }
    
    def _parse_dependency_check(self, file_path: Path) -> Dict:
        """Parse OWASP Dependency-Check JSON report"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        vulnerabilities = []
        for dependency in data.get('dependencies', []):
            for vuln in dependency.get('vulnerabilities', []):
                vulnerabilities.append({
                    'id': vuln.get('name'),  # CVE ID
                    'title': vuln.get('name'),
                    'description': vuln.get('description'),
                    'severity': vuln.get('severity'),
                    'cvss_score': vuln.get('cvssv3', {}).get('baseScore') if vuln.get('cvssv3') else None,
                    'cwe': vuln.get('cwe'),
                    'dependency': dependency.get('fileName'),
                    'references': [ref.get('url') for ref in vuln.get('references', [])],
                    'tool': 'dependency-check',
                    'category': 'SCA'
                })
        
        return {
            'tool': 'dependency-check',
            'category': 'SCA',
            'project': data.get('projectInfo', {}).get('name'),
            'scan_date': data.get('reportDate'),
            'vulnerabilities': vulnerabilities
        }
    
    def _parse_safety(self, file_path: Path) -> Dict:
        """Parse Safety JSON report"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        vulnerabilities = []
        if isinstance(data, list):
            for vuln in data:
                vulnerabilities.append({
                    'id': vuln.get('advisory'),
                    'title': vuln.get('advisory'),
                    'description': vuln.get('advisory'),
                    'severity': 'UNKNOWN',  # Safety doesn't provide severity
                    'package': vuln.get('package_name'),
                    'installed_version': vuln.get('installed_version'),
                    'affected_versions': vuln.get('affected_versions'),
                    'tool': 'safety',
                    'category': 'SCA'
                })
        
        return {
            'tool': 'safety',
            'category': 'SCA',
            'vulnerabilities': vulnerabilities
        }
    
    def _parse_zap(self, file_path: Path) -> Dict:
        """Parse OWASP ZAP JSON report"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        vulnerabilities = []
        for site in data.get('site', []):
            for alert in site.get('alerts', []):
                vulnerabilities.append({
                    'id': alert.get('pluginid'),
                    'title': alert.get('alert'),
                    'description': alert.get('desc'),
                    'severity': alert.get('riskdesc', '').split()[0],  # Extract severity
                    'confidence': alert.get('confidence'),
                    'url': alert.get('url'),
                    'method': alert.get('method'),
                    'solution': alert.get('solution'),
                    'reference': alert.get('reference'),
                    'cwe': alert.get('cweid'),
                    'wasc': alert.get('wascid'),
                    'tool': 'zap',
                    'category': 'DAST'
                })
        
        return {
            'tool': 'zap',
            'category': 'DAST',
            'scan_date': data.get('@generated'),
            'vulnerabilities': vulnerabilities
        }
    
    def _parse_generic(self, file_path: Path) -> Dict:
        """Generic parser for unknown report formats"""
        logger.warning(f"Using generic parser for: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return {
                'tool': 'unknown',
                'category': 'UNKNOWN',
                'raw_data': data,
                'vulnerabilities': []
            }
        except json.JSONDecodeError:
            return {
                'tool': 'unknown',
                'category': 'UNKNOWN',
                'error': 'Failed to parse report',
                'vulnerabilities': []
            }
    
    def normalize_severity(self, severity: str) -> str:
        """Normalize severity levels across different tools"""
        severity_map = {
            'CRITICAL': 'CRITICAL',
            'HIGH': 'HIGH',
            'MEDIUM': 'MEDIUM',
            'LOW': 'LOW',
            'INFO': 'INFO',
            'INFORMATIONAL': 'INFO',
            'WARNING': 'MEDIUM',
            'ERROR': 'HIGH',
            'BLOCKER': 'CRITICAL'
        }
        
        return severity_map.get(severity.upper(), 'UNKNOWN')
