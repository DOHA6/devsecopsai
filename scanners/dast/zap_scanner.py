"""
OWASP ZAP DAST Scanner
Dynamic application security testing for web applications
"""

import time
from pathlib import Path
from loguru import logger
try:
    from zapv2 import ZAPv2
except ImportError:
    ZAPv2 = None
import os


class ZAPScanner:
    """Wrapper for OWASP ZAP scanner"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.name = "zap"
        self.api_key = os.getenv('ZAP_API_KEY')
        self.proxy_address = os.getenv('ZAP_PROXY_ADDRESS', 'http://localhost:8080')
    
    def scan(self, target: str) -> Path:
        """
        Run ZAP scan on target URL
        
        Args:
            target: URL to scan (must be http:// or https://)
        
        Returns:
            Path to generated report
        """
        if not target.startswith(('http://', 'https://')):
            logger.warning(f"ZAP requires HTTP/HTTPS URL. Skipping: {target}")
            return None
        
        report_json = self.output_dir / f"{self.name}_report.json"
        report_html = self.output_dir / f"{self.name}_report.html"
        
        try:
            if ZAPv2 is None:
                logger.warning("ZAP Python API not installed. Using Docker...")
                return self._scan_with_docker(target, report_json, report_html)
            
            # Use ZAP API
            zap = ZAPv2(
                apikey=self.api_key,
                proxies={'http': self.proxy_address, 'https': self.proxy_address}
            )
            
            logger.info(f"Starting ZAP spider scan on {target}")
            scan_id = zap.spider.scan(target)
            
            # Wait for spider to complete
            while int(zap.spider.status(scan_id)) < 100:
                logger.info(f"Spider progress: {zap.spider.status(scan_id)}%")
                time.sleep(5)
            
            logger.info("Spider scan completed. Starting active scan...")
            scan_id = zap.ascan.scan(target)
            
            # Wait for active scan to complete
            while int(zap.ascan.status(scan_id)) < 100:
                logger.info(f"Active scan progress: {zap.ascan.status(scan_id)}%")
                time.sleep(10)
            
            # Generate reports
            html_report = zap.core.htmlreport()
            json_report = zap.core.jsonreport()
            
            with open(report_html, 'w') as f:
                f.write(html_report)
            with open(report_json, 'w') as f:
                f.write(json_report)
            
            logger.info(f"ZAP scan completed: {report_json}")
            return report_json
            
        except Exception as e:
            logger.error(f"ZAP scan failed: {e}")
            raise
    
    def _scan_with_docker(self, target: str, report_json: Path, report_html: Path) -> Path:
        """Run ZAP using Docker container"""
        import subprocess
        
        try:
            # Run ZAP baseline scan
            subprocess.run([
                'docker', 'run', '--rm',
                '-v', f'{self.output_dir.absolute()}:/zap/wrk',
                'owasp/zap2docker-stable',
                'zap-baseline.py',
                '-t', target,
                '-J', f'/zap/wrk/{report_json.name}',
                '-r', f'/zap/wrk/{report_html.name}',
                '-I'  # Ignore warnings
            ], check=False)  # ZAP returns non-zero if issues found
            
            return report_json
        except subprocess.CalledProcessError as e:
            logger.error(f"ZAP Docker scan failed: {e}")
            raise
