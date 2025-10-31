"""
DevSecOps AI Dashboard
Visualizes CI/CD pipeline results, security scans, and policy generation metrics
"""
import os
import json
import glob
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from collections import defaultdict

app = Flask(__name__)

# Configuration
BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "data" / "reports"
POLICIES_DIR = BASE_DIR / "output" / "generated_policies"
EVALUATION_DIR = BASE_DIR / "output" / "evaluation_results"
LOGS_DIR = BASE_DIR / "logs"

def load_latest_scan_results():
    """Load the most recent security scan results"""
    results = {
        'bandit': None,
        'dependency_check': None,
        'safety': None,
        'sonarqube': None,
        'zap': None
    }
    
    # Load Bandit results
    bandit_files = glob.glob(str(REPORTS_DIR / "bandit_report*.json"))
    if bandit_files:
        latest = max(bandit_files, key=os.path.getmtime)
        with open(latest, 'r') as f:
            results['bandit'] = json.load(f)
    
    # Load Dependency Check results
    dep_files = glob.glob(str(REPORTS_DIR / "dependency_check_report*.json"))
    if dep_files:
        latest = max(dep_files, key=os.path.getmtime)
        with open(latest, 'r') as f:
            results['dependency_check'] = json.load(f)
    
    # Load Safety results
    safety_files = glob.glob(str(REPORTS_DIR / "safety_report*.json"))
    if safety_files:
        latest = max(safety_files, key=os.path.getmtime)
        with open(latest, 'r') as f:
            results['safety'] = json.load(f)
    
    return results

def aggregate_vulnerabilities(scan_results):
    """Aggregate vulnerability counts by severity"""
    severity_counts = defaultdict(int)
    vulnerability_details = []
    
    # Process Bandit results
    if scan_results.get('bandit'):
        for result in scan_results['bandit'].get('results', []):
            severity = result.get('issue_severity', 'UNKNOWN')
            severity_counts[severity] += 1
            vulnerability_details.append({
                'source': 'Bandit (SAST)',
                'severity': severity,
                'description': result.get('issue_text', ''),
                'location': f"{result.get('filename', '')}:{result.get('line_number', '')}",
                'cwe': result.get('issue_cwe', {}).get('id', 'N/A')
            })
    
    # Process Dependency Check results
    if scan_results.get('dependency_check'):
        for dep in scan_results['dependency_check'].get('dependencies', []):
            for vuln in dep.get('vulnerabilities', []):
                severity = vuln.get('severity', 'UNKNOWN')
                severity_counts[severity] += 1
                vulnerability_details.append({
                    'source': 'Dependency Check (SCA)',
                    'severity': severity,
                    'description': vuln.get('description', ''),
                    'location': dep.get('fileName', ''),
                    'cwe': vuln.get('cwes', ['N/A'])[0] if vuln.get('cwes') else 'N/A'
                })
    
    # Process Safety results
    if scan_results.get('safety'):
        for vuln in scan_results['safety']:
            severity_counts['MEDIUM'] += 1  # Safety typically reports medium severity
            vulnerability_details.append({
                'source': 'Safety (SCA)',
                'severity': 'MEDIUM',
                'description': vuln.get('advisory', ''),
                'location': f"{vuln.get('package', '')} {vuln.get('installed_version', '')}",
                'cwe': 'N/A'
            })
    
    return dict(severity_counts), vulnerability_details

def load_evaluation_metrics():
    """Load policy evaluation metrics"""
    eval_files = glob.glob(str(EVALUATION_DIR / "evaluation_*.json"))
    if not eval_files:
        return None
    
    latest = max(eval_files, key=os.path.getmtime)
    with open(latest, 'r') as f:
        return json.load(f)

def load_generated_policies():
    """Load information about generated policies"""
    policies = []
    policy_files = glob.glob(str(POLICIES_DIR / "**/*.md"), recursive=True)
    
    for policy_file in policy_files:
        stat = os.stat(policy_file)
        policies.append({
            'name': os.path.basename(policy_file),
            'framework': 'NIST_CSF' if 'nist' in policy_file.lower() else 
                        'ISO_27001' if 'iso' in policy_file.lower() else
                        'CIS_Controls' if 'cis' in policy_file.lower() else 'Unknown',
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'path': policy_file
        })
    
    return policies

def get_pipeline_status():
    """Get overall pipeline status"""
    scan_results = load_latest_scan_results()
    has_scans = any(scan_results.values())
    
    policies = load_generated_policies()
    has_policies = len(policies) > 0
    
    evaluation = load_evaluation_metrics()
    has_evaluation = evaluation is not None
    
    severity_counts, _ = aggregate_vulnerabilities(scan_results)
    has_critical = severity_counts.get('CRITICAL', 0) > 0
    has_high = severity_counts.get('HIGH', 0) > 0
    
    # Determine overall status
    if not has_scans:
        status = 'pending'
        message = 'No scans completed yet'
    elif has_critical:
        status = 'failed'
        message = f'Critical vulnerabilities found'
    elif has_high > 5:
        status = 'warning'
        message = f'{has_high} high-severity vulnerabilities found'
    elif has_policies:
        status = 'success'
        message = 'Pipeline completed successfully'
    else:
        status = 'running'
        message = 'Scans completed, generating policies...'
    
    return {
        'status': status,
        'message': message,
        'stages': {
            'scan': 'completed' if has_scans else 'pending',
            'policy_generation': 'completed' if has_policies else 'pending',
            'evaluation': 'completed' if has_evaluation else 'pending'
        }
    }

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """Get pipeline status"""
    return jsonify(get_pipeline_status())

@app.route('/api/vulnerabilities')
def api_vulnerabilities():
    """Get vulnerability statistics"""
    scan_results = load_latest_scan_results()
    severity_counts, vulnerability_details = aggregate_vulnerabilities(scan_results)
    
    return jsonify({
        'severity_counts': severity_counts,
        'total': sum(severity_counts.values()),
        'details': vulnerability_details[:50]  # Limit to 50 for performance
    })

@app.route('/api/metrics')
def api_metrics():
    """Get evaluation metrics"""
    metrics = load_evaluation_metrics()
    if not metrics:
        return jsonify({'error': 'No evaluation data available'}), 404
    
    return jsonify(metrics)

@app.route('/api/policies')
def api_policies():
    """Get generated policies"""
    policies = load_generated_policies()
    return jsonify({
        'total': len(policies),
        'policies': policies
    })

@app.route('/api/policy/<path:policy_name>')
def api_policy_content(policy_name):
    """Get content of a specific policy"""
    policy_path = POLICIES_DIR / policy_name
    if not policy_path.exists():
        return jsonify({'error': 'Policy not found'}), 404
    
    with open(policy_path, 'r') as f:
        content = f.read()
    
    return jsonify({
        'name': policy_name,
        'content': content
    })

@app.route('/api/history')
def api_history():
    """Get historical scan data"""
    history = []
    
    # Collect all report files with timestamps
    report_files = glob.glob(str(REPORTS_DIR / "*.json"))
    
    for report_file in sorted(report_files, key=os.path.getmtime):
        try:
            with open(report_file, 'r') as f:
                data = json.load(f)
            
            stat = os.stat(report_file)
            timestamp = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
            # Count vulnerabilities
            vuln_count = 0
            if 'results' in data:  # Bandit format
                vuln_count = len(data['results'])
            elif 'dependencies' in data:  # Dependency Check format
                vuln_count = sum(len(dep.get('vulnerabilities', [])) 
                               for dep in data['dependencies'])
            
            history.append({
                'timestamp': timestamp,
                'scanner': os.path.basename(report_file).split('_')[0],
                'vulnerabilities': vuln_count
            })
        except:
            continue
    
    return jsonify(history[-20:])  # Last 20 scans

if __name__ == '__main__':
    # Ensure directories exist
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    POLICIES_DIR.mkdir(parents=True, exist_ok=True)
    EVALUATION_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("DevSecOps AI Dashboard Starting...")
    print("="*70)
    print(f"\n🌐 Dashboard URL: http://localhost:5000")
    print(f"📊 Reports Directory: {REPORTS_DIR}")
    print(f"📄 Policies Directory: {POLICIES_DIR}")
    print(f"📈 Evaluation Directory: {EVALUATION_DIR}")
    print("\nPress Ctrl+C to stop the server\n")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
