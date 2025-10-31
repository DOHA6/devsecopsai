"""
Unit tests for Policy Evaluator
"""

import pytest
import json
from pathlib import Path
from evaluation.evaluator import PolicyEvaluator


@pytest.fixture
def sample_generated_policy(tmp_path):
    """Create sample generated policy"""
    policy = {
        "framework": "NIST_CSF",
        "content": "This is a security policy that addresses identify, protect, detect, respond, and recover functions with risk assessment and monitoring procedures."
    }
    
    policy_dir = tmp_path / "generated"
    policy_dir.mkdir()
    policy_file = policy_dir / "policy.json"
    
    with open(policy_file, 'w') as f:
        json.dump(policy, f)
    
    return policy_dir


@pytest.fixture
def sample_reference_policy(tmp_path):
    """Create sample reference policy"""
    policy = {
        "framework": "NIST_CSF",
        "content": "Security policy covering identify, protect, detect, respond, recover with comprehensive risk assessment and continuous monitoring."
    }
    
    ref_dir = tmp_path / "reference"
    ref_dir.mkdir()
    ref_file = ref_dir / "reference.json"
    
    with open(ref_file, 'w') as f:
        json.dump(policy, f)
    
    return ref_dir


def test_load_policies(sample_generated_policy):
    """Test loading policy files"""
    evaluator = PolicyEvaluator(
        str(sample_generated_policy),
        ".",
        str(sample_generated_policy.parent / "output")
    )
    
    policies = evaluator._load_policies(sample_generated_policy)
    assert len(policies) == 1
    assert policies[0]['framework'] == 'NIST_CSF'


def test_get_required_elements():
    """Test getting required framework elements"""
    evaluator = PolicyEvaluator(".", ".", ".")
    
    nist_elements = evaluator._get_required_elements('NIST_CSF')
    assert 'identify' in nist_elements
    assert 'protect' in nist_elements
    assert 'detect' in nist_elements
    
    iso_elements = evaluator._get_required_elements('ISO_27001')
    assert 'risk assessment' in iso_elements
    assert 'security controls' in iso_elements


def test_calculate_compliance(sample_generated_policy):
    """Test compliance score calculation"""
    evaluator = PolicyEvaluator(
        str(sample_generated_policy),
        ".",
        str(sample_generated_policy.parent / "output")
    )
    
    policies = evaluator._load_policies(sample_generated_policy)
    score = evaluator._calculate_compliance(policies)
    
    assert 0.0 <= score <= 1.0
    assert score > 0  # Should find some required elements
