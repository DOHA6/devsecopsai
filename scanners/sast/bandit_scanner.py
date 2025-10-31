"""
Bandit SAST Scanner
Python security linter for detecting common security issues
"""

import json
import subprocess
from pathlib import Path
from loguru import logger


class BanditScanner:
    """Wrapper for Bandit security scanner"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.name = "bandit"
    
    def scan(self, target: str) -> Path:
        """
        Run Bandit scan on target directory
        
        Args:
            target: Path to Python code to scan
        
        Returns:
            Path to generated report
        """
        report_json = self.output_dir / f"{self.name}_report.json"
        report_html = self.output_dir / f"{self.name}_report.html"
        
        try:
            # Run Bandit with JSON output
            subprocess.run([
                'bandit',
                '-r', target,
                '-f', 'json',
                '-o', str(report_json)
            ], check=False, capture_output=True)
            
            # Also generate HTML report
            subprocess.run([
                'bandit',
                '-r', target,
                '-f', 'html',
                '-o', str(report_html)
            ], check=False, capture_output=True)
            
            logger.info(f"Bandit scan completed: {report_json}")
            return report_json
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Bandit scan failed: {e}")
            raise
        except FileNotFoundError:
            logger.error("Bandit not installed. Install with: pip install bandit")
            raise
    
    def parse_report(self, report_path: Path) -> dict:
        """Parse Bandit JSON report"""
        with open(report_path, 'r') as f:
            return json.load(f)
