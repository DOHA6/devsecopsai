"""
SonarQube SAST Scanner
Comprehensive static code analysis platform
"""

import requests
import time
from pathlib import Path
from loguru import logger
import os


class SonarQubeScanner:
    """Wrapper for SonarQube scanner"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.name = "sonarqube"
        self.url = os.getenv('SONARQUBE_URL', 'http://localhost:9000')
        self.token = os.getenv('SONARQUBE_TOKEN')
    
    def scan(self, target: str) -> Path:
        """
        Run SonarQube scan on target
        
        Args:
            target: Path to code to scan
        
        Returns:
            Path to generated report
        """
        if not self.token:
            logger.warning("SonarQube token not set. Skipping scan.")
            return None
        
        project_key = Path(target).name.replace(' ', '_')
        report_path = self.output_dir / f"{self.name}_report.json"
        
        try:
            # Run sonar-scanner
            import subprocess
            subprocess.run([
                'sonar-scanner',
                f'-Dsonar.projectKey={project_key}',
                f'-Dsonar.sources={target}',
                f'-Dsonar.host.url={self.url}',
                f'-Dsonar.login={self.token}'
            ], check=True, capture_output=True)
            
            # Wait for analysis to complete
            time.sleep(5)
            
            # Fetch results via API
            issues = self._fetch_issues(project_key)
            
            # Save to JSON
            import json
            with open(report_path, 'w') as f:
                json.dump(issues, f, indent=2)
            
            logger.info(f"SonarQube scan completed: {report_path}")
            return report_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"SonarQube scan failed: {e}")
            raise
        except FileNotFoundError:
            logger.error("sonar-scanner not installed")
            raise
    
    def _fetch_issues(self, project_key: str) -> dict:
        """Fetch issues from SonarQube API"""
        url = f"{self.url}/api/issues/search"
        params = {
            'componentKeys': project_key,
            'ps': 500  # Page size
        }
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
