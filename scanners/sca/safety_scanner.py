"""
Safety SCA Scanner
Checks Python dependencies for known security vulnerabilities
"""

import json
import subprocess
from pathlib import Path
from loguru import logger


class SafetyScanner:
    """Wrapper for Safety security scanner"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.name = "safety"
    
    def scan(self, target: str) -> Path:
        """
        Run Safety scan on Python dependencies
        
        Args:
            target: Path to project (looks for requirements.txt or Pipfile)
        
        Returns:
            Path to generated report
        """
        report_path = self.output_dir / f"{self.name}_report.json"
        
        try:
            # Run Safety check
            result = subprocess.run([
                'safety', 'check',
                '--json',
                '--file', str(Path(target) / 'requirements.txt')
            ], capture_output=True, text=True, check=False)
            
            # Parse and save output
            try:
                report_data = json.loads(result.stdout) if result.stdout else []
            except json.JSONDecodeError:
                report_data = {
                    'error': 'Failed to parse Safety output',
                    'raw_output': result.stdout
                }
            
            with open(report_path, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            logger.info(f"Safety scan completed: {report_path}")
            return report_path
            
        except FileNotFoundError:
            logger.error("Safety not installed. Install with: pip install safety")
            raise
        except Exception as e:
            logger.error(f"Safety scan failed: {e}")
            raise
