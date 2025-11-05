"""
Scanner Orchestrator
Coordinates SAST, SCA, and DAST security scanning tools
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List
from loguru import logger

from .sast.bandit_scanner import BanditScanner
from .sca.dependency_check_scanner import DependencyCheckScanner
from .sca.safety_scanner import SafetyScanner
from .dast.zap_scanner import ZAPScanner


class ScannerOrchestrator:
    """Orchestrates multiple security scanning tools"""
    
    def __init__(self, output_dir: str = './data/reports'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize scanners
        self.scanners = {
            'sast': {
                'bandit': BanditScanner(self.output_dir)
            },
            'sca': {
                'dependency_check': DependencyCheckScanner(self.output_dir),
                'safety': SafetyScanner(self.output_dir)
            },
            'dast': {
                'zap': ZAPScanner(self.output_dir)
            }
        }
    
    def run_scans(self, target: str, scanner_types: List[str]) -> Dict[str, str]:
        """
        Run specified security scans on target
        
        Args:
            target: Path or URL to scan
            scanner_types: List of scanner types ('sast', 'sca', 'dast')
        
        Returns:
            Dictionary mapping scanner names to report file paths
        """
        results = {}
        
        for scanner_type in scanner_types:
            if scanner_type not in self.scanners:
                logger.warning(f"Unknown scanner type: {scanner_type}")
                continue
            
            logger.info(f"Running {scanner_type.upper()} scans...")
            
            for scanner_name, scanner in self.scanners[scanner_type].items():
                try:
                    logger.info(f"  - {scanner_name}")
                    report_path = scanner.scan(target)
                    results[f"{scanner_type}_{scanner_name}"] = str(report_path)
                    logger.info(f"    ✓ Report: {report_path}")
                except Exception as e:
                    logger.error(f"    ✗ {scanner_name} failed: {e}")
                    results[f"{scanner_type}_{scanner_name}"] = None
        
        return results
    
    def get_all_reports(self) -> List[Path]:
        """Get list of all generated report files"""
        report_files = []
        for pattern in ['*.json', '*.xml', '*.html']:
            report_files.extend(self.output_dir.glob(pattern))
        return report_files
