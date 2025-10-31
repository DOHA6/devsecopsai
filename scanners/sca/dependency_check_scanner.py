"""
OWASP Dependency-Check SCA Scanner
Identifies known vulnerabilities in project dependencies
"""

import subprocess
from pathlib import Path
from loguru import logger


class DependencyCheckScanner:
    """Wrapper for OWASP Dependency-Check"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.name = "dependency_check"
    
    def scan(self, target: str) -> Path:
        """
        Run Dependency-Check scan on target
        
        Args:
            target: Path to project to scan
        
        Returns:
            Path to generated report
        """
        report_path = self.output_dir / f"{self.name}_report.json"
        
        try:
            # Check if running in Docker
            try:
                subprocess.run(['docker', '--version'], check=True, capture_output=True)
                use_docker = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                use_docker = False
            
            if use_docker:
                # Run via Docker
                subprocess.run([
                    'docker', 'run', '--rm',
                    '-v', f'{Path(target).absolute()}:/src',
                    '-v', f'{self.output_dir.absolute()}:/report',
                    'owasp/dependency-check',
                    '--scan', '/src',
                    '--format', 'JSON',
                    '--format', 'HTML',
                    '--out', '/report',
                    '--project', 'DevSecOps-AI'
                ], check=True)
            else:
                # Run locally installed version
                subprocess.run([
                    'dependency-check',
                    '--scan', target,
                    '--format', 'JSON',
                    '--format', 'HTML',
                    '--out', str(self.output_dir),
                    '--project', 'DevSecOps-AI'
                ], check=True)
            
            logger.info(f"Dependency-Check scan completed: {report_path}")
            return report_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Dependency-Check scan failed: {e}")
            raise
        except FileNotFoundError:
            logger.error("Dependency-Check not found. Install or use Docker.")
            raise
