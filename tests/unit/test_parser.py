"""
Unit tests for Report Parser
"""

import pytest
import json
from pathlib import Path
from parsers.report_parser import ReportParser


@pytest.fixture
def sample_bandit_report(tmp_path):
    """Create a sample Bandit report"""
    report = {
        "results": [
            {
                "test_id": "B201",
                "test_name": "flask_debug_true",
                "issue_severity": "HIGH",
                "issue_confidence": "HIGH",
                "issue_text": "Flask debug mode",
                "filename": "app.py",
                "line_number": 10,
                "code": "app.run(debug=True)"
            }
        ],
        "metrics": {"_totals": {"loc": 100}},
        "generated_at": "2025-10-31T10:00:00"
    }
    
    report_file = tmp_path / "bandit_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f)
    
    return report_file


def test_parse_bandit_report(sample_bandit_report):
    """Test parsing Bandit report"""
    parser = ReportParser()
    result = parser.parse_file(sample_bandit_report)
    
    assert result['tool'] == 'bandit'
    assert result['category'] == 'SAST'
    assert len(result['vulnerabilities']) == 1
    assert result['vulnerabilities'][0]['severity'] == 'HIGH'


def test_detect_report_type():
    """Test report type detection"""
    parser = ReportParser()
    
    assert parser._detect_report_type(Path("bandit_report.json")) == 'bandit'
    assert parser._detect_report_type(Path("dependency_check_report.json")) == 'dependency_check'
    assert parser._detect_report_type(Path("zap_report.json")) == 'zap'


def test_normalize_severity():
    """Test severity normalization"""
    parser = ReportParser()
    
    assert parser.normalize_severity("CRITICAL") == "CRITICAL"
    assert parser.normalize_severity("WARNING") == "MEDIUM"
    assert parser.normalize_severity("ERROR") == "HIGH"
    assert parser.normalize_severity("BLOCKER") == "CRITICAL"


def test_parse_directory_empty(tmp_path):
    """Test parsing empty directory"""
    parser = ReportParser()
    results = parser.parse_directory(tmp_path)
    
    assert len(results) == 0


def test_parse_file_not_found():
    """Test parsing non-existent file"""
    parser = ReportParser()
    
    with pytest.raises(FileNotFoundError):
        parser.parse_file("nonexistent.json")
