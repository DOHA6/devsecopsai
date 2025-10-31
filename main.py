"""
Main CLI entry point for DevSecOps AI project
Handles scanning, policy generation, and evaluation workflows
"""

import click
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scanners.scanner_orchestrator import ScannerOrchestrator
from parsers.report_parser import ReportParser
from policy_generator.policy_orchestrator import PolicyOrchestrator
from evaluation.evaluator import PolicyEvaluator


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """DevSecOps AI - Automated Security Policy Generation"""
    # Configure logging
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', './logs/devsecopsai.log')
    
    # Create logs directory if it doesn't exist
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(log_file, rotation="10 MB", retention="30 days", level=log_level)
    logger.info("DevSecOps AI CLI started")


@cli.command()
@click.option('--target', required=True, help='Target application path or URL to scan')
@click.option('--scanners', default='all', help='Comma-separated list: sast,sca,dast or "all"')
@click.option('--output', default='./data/reports', help='Output directory for scan reports')
def scan(target: str, scanners: str, output: str):
    """Run security scans (SAST, SCA, DAST) on target"""
    logger.info(f"Starting security scan on target: {target}")
    
    try:
        orchestrator = ScannerOrchestrator(output_dir=output)
        
        if scanners == 'all':
            scanner_list = ['sast', 'sca', 'dast']
        else:
            scanner_list = [s.strip() for s in scanners.split(',')]
        
        results = orchestrator.run_scans(target, scanner_list)
        
        click.echo(f"✅ Scans completed successfully!")
        click.echo(f"📊 Results saved to: {output}")
        
        for scanner_type, report_path in results.items():
            click.echo(f"  - {scanner_type.upper()}: {report_path}")
        
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        click.echo(f"❌ Scan failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--input', required=True, help='Input directory with vulnerability reports')
@click.option('--output', default='./output/generated_policies', help='Output directory for policies')
@click.option('--framework', default='NIST_CSF', 
              type=click.Choice(['NIST_CSF', 'ISO_27001', 'CIS_CONTROLS'], case_sensitive=False),
              help='Security framework to use')
@click.option('--model', default=None, help='LLM model to use (overrides env variable)')
def generate(input: str, output: str, framework: str, model: str):
    """Generate security policies from vulnerability reports"""
    logger.info(f"Generating policies using {framework} framework")
    
    try:
        # Parse vulnerability reports
        click.echo("📄 Parsing vulnerability reports...")
        parser = ReportParser()
        parsed_data = parser.parse_directory(input)
        
        if not parsed_data:
            click.echo("⚠️  No vulnerability reports found", err=True)
            sys.exit(1)
        
        click.echo(f"✅ Parsed {len(parsed_data)} vulnerability reports")
        
        # Generate policies
        click.echo(f"🤖 Generating policies using {framework}...")
        orchestrator = PolicyOrchestrator(framework=framework, output_dir=output, model_override=model)
        policies = orchestrator.generate_policies(parsed_data)
        
        click.echo(f"✅ Generated {len(policies)} security policies")
        click.echo(f"📁 Policies saved to: {output}")
        
        for policy_file in policies:
            click.echo(f"  - {policy_file}")
        
    except Exception as e:
        logger.error(f"Policy generation failed: {e}")
        click.echo(f"❌ Policy generation failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--policies', required=True, help='Directory with generated policies')
@click.option('--reference', required=True, help='Directory with reference policies')
@click.option('--output', default='./output/evaluation_results', help='Output directory for results')
@click.option('--metrics', default='BLEU,ROUGE-L', help='Comma-separated metrics to calculate')
def evaluate(policies: str, reference: str, output: str, metrics: str):
    """Evaluate generated policies against reference policies"""
    logger.info("Starting policy evaluation")
    
    try:
        click.echo("📊 Evaluating generated policies...")
        
        evaluator = PolicyEvaluator(
            generated_dir=policies,
            reference_dir=reference,
            output_dir=output
        )
        
        metric_list = [m.strip() for m in metrics.split(',')]
        results = evaluator.evaluate(metric_list)
        
        click.echo("✅ Evaluation completed!")
        click.echo("\n📈 Results Summary:")
        
        if 'BLEU' in results:
            click.echo(f"  BLEU Score: {results['BLEU']:.4f}")
        if 'ROUGE-L' in results:
            click.echo(f"  ROUGE-L Score: {results['ROUGE-L']:.4f}")
        if 'COMPLIANCE' in results:
            click.echo(f"  Compliance Score: {results['COMPLIANCE']:.4f}")
        
        click.echo(f"\n📁 Detailed results saved to: {output}")
        
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        click.echo(f"❌ Evaluation failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--input', required=True, help='Path to vulnerability report file')
def parse(input: str):
    """Parse a single vulnerability report and display structured output"""
    logger.info(f"Parsing report: {input}")
    
    try:
        parser = ReportParser()
        data = parser.parse_file(input)
        
        click.echo("\n📄 Parsed Vulnerability Report:\n")
        click.echo(f"Total Vulnerabilities: {len(data.get('vulnerabilities', []))}")
        
        # Group by severity
        severity_count = {}
        for vuln in data.get('vulnerabilities', []):
            severity = vuln.get('severity', 'UNKNOWN')
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        click.echo("\nBy Severity:")
        for severity, count in sorted(severity_count.items()):
            click.echo(f"  {severity}: {count}")
        
    except Exception as e:
        logger.error(f"Parsing failed: {e}")
        click.echo(f"❌ Parsing failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def init():
    """Initialize project structure and configuration"""
    logger.info("Initializing project")
    
    try:
        # Create necessary directories
        directories = [
            'data/reports',
            'data/reference_policies',
            'output/generated_policies',
            'output/evaluation_results',
            'logs',
            'tests/unit',
            'tests/integration',
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            click.echo(f"✅ Created directory: {directory}")
        
        # Copy .env.example to .env if it doesn't exist
        if not Path('.env').exists():
            if Path('.env.example').exists():
                import shutil
                shutil.copy('.env.example', '.env')
                click.echo("✅ Created .env file from .env.example")
                click.echo("⚠️  Please edit .env with your API keys and configuration")
            else:
                click.echo("⚠️  .env.example not found")
        else:
            click.echo("ℹ️  .env file already exists")
        
        click.echo("\n✅ Project initialized successfully!")
        click.echo("\nNext steps:")
        click.echo("1. Edit .env file with your configuration")
        click.echo("2. Install dependencies: pip install -r requirements.txt")
        click.echo("3. Run a scan: python main.py scan --target <path>")
        
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        click.echo(f"❌ Initialization failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def check_config():
    """Check configuration and verify API keys"""
    logger.info("Checking configuration")
    
    click.echo("🔍 Checking configuration...\n")
    
    # Check LLM configuration
    provider = os.getenv('LLM_PROVIDER')
    click.echo(f"LLM Provider: {provider or '❌ Not set'}")
    
    if provider == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
        click.echo(f"OpenAI API Key: {'✅ Set' if api_key else '❌ Not set'}")
    elif provider == 'anthropic':
        api_key = os.getenv('ANTHROPIC_API_KEY')
        click.echo(f"Anthropic API Key: {'✅ Set' if api_key else '❌ Not set'}")
    elif provider == 'ollama':
        host = os.getenv('OLLAMA_HOST')
        click.echo(f"Ollama Host: {host or '❌ Not set'}")
    
    # Check security tool configuration
    click.echo(f"\nSecurity Tools:")
    click.echo(f"SonarQube URL: {os.getenv('SONARQUBE_URL') or '❌ Not set'}")
    click.echo(f"ZAP Proxy: {os.getenv('ZAP_PROXY_ADDRESS') or '❌ Not set'}")
    
    # Check directories
    click.echo(f"\nDirectories:")
    for directory in ['data/reports', 'data/reference_policies', 'output', 'logs']:
        exists = Path(directory).exists()
        click.echo(f"{directory}: {'✅ Exists' if exists else '❌ Missing'}")


if __name__ == '__main__':
    cli()
