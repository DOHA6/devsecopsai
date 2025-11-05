"""
Policy Generator Orchestrator
Coordinates policy generation from vulnerability reports using LLMs
Optimized for speed with parallel processing
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

from llm_engine.llm_manager import LLMManager
from llm_engine.prompt_engine import PromptEngine


class PolicyOrchestrator:
    """Orchestrates security policy generation"""
    
    def __init__(
        self, 
        framework: str = "NIST_CSF",
        output_dir: str = "./output/generated_policies",
        model_override: Optional[str] = None,
        max_workers: Optional[int] = None
    ):
        self.framework = framework
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize LLM and prompt engines
        self.llm_manager = LLMManager(model=model_override, use_cache=True)
        self.prompt_engine = PromptEngine(framework=framework)
        
        # Parallel processing configuration
        self.max_workers = max_workers or int(os.getenv('MAX_PARALLEL_POLICIES', '3'))
    
    def generate_policies(self, vulnerability_reports: List[Dict]) -> List[Path]:
        """
        Generate security policies from vulnerability reports in parallel
        
        Args:
            vulnerability_reports: List of parsed vulnerability reports
        
        Returns:
            List of paths to generated policy files
        """
        generated_files = []
        
        # Aggregate vulnerabilities from all reports
        all_vulnerabilities = []
        for report in vulnerability_reports:
            all_vulnerabilities.extend(report.get('vulnerabilities', []))
        
        if not all_vulnerabilities:
            logger.warning("No vulnerabilities found in reports")
            return generated_files
        
        logger.info(f"Generating policies for {len(all_vulnerabilities)} vulnerabilities (parallel mode)")
        
        # Generate main policy (always first)
        policy_file = self._generate_main_policy(all_vulnerabilities)
        if policy_file:
            generated_files.append(policy_file)
        
        # Generate category-specific policies in parallel
        by_category = self._group_by_category(all_vulnerabilities)
        
        if by_category and self.max_workers > 1:
            # Parallel generation for categories
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_category = {
                    executor.submit(self._generate_category_policy, category, vulns): category
                    for category, vulns in by_category.items() if vulns
                }
                
                for future in as_completed(future_to_category):
                    category = future_to_category[future]
                    try:
                        policy_file = future.result()
                        if policy_file:
                            generated_files.append(policy_file)
                    except Exception as e:
                        logger.error(f"Failed to generate policy for {category}: {e}")
        else:
            # Sequential fallback
            for category, vulns in by_category.items():
                if vulns:
                    policy_file = self._generate_category_policy(category, vulns)
                    if policy_file:
                        generated_files.append(policy_file)
        
        return generated_files
    
    def _generate_main_policy(self, vulnerabilities: List[Dict]) -> Optional[Path]:
        """Generate comprehensive main policy - optimized"""
        logger.info("Generating main security policy...")
        
        try:
            # Create prompt
            prompt = self.prompt_engine.generate_policy_prompt(vulnerabilities)
            
            # Generate policy using LLM with optimized settings
            logger.info("Calling LLM for policy generation...")
            policy_content = self.llm_manager.generate_with_retry(
                prompt,
                temperature=0.3,
                max_tokens=512  # Reduced for speed
            )
            
            # Create policy document
            policy_doc = {
                'framework': self.framework,
                'generated_at': datetime.now().isoformat(),
                'vulnerability_count': len(vulnerabilities),
                'content': policy_content,
                'metadata': {
                    'llm_provider': self.llm_manager.provider_name,
                    'model': self.llm_manager.model
                }
            }
            
            # Save to file
            filename = f"{self.framework.lower()}_policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            output_file = self.output_dir / filename
            
            with open(output_file, 'w') as f:
                json.dump(policy_doc, f, indent=2)
            
            logger.info(f"Main policy generated: {output_file}")
            
            # Also save as markdown for readability
            md_file = output_file.with_suffix('.md')
            with open(md_file, 'w') as f:
                f.write(f"# Security Policy - {self.framework}\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**Vulnerabilities Addressed:** {len(vulnerabilities)}\n\n")
                f.write("---\n\n")
                f.write(policy_content)
            
            return output_file
            
        except Exception as e:
            logger.error(f"Failed to generate main policy: {e}")
            return None
    
    def _generate_category_policy(self, category: str, vulnerabilities: List[Dict]) -> Optional[Path]:
        """Generate policy for specific vulnerability category - optimized"""
        logger.info(f"Generating policy for {category} category...")
        
        try:
            # Create focused prompt
            prompt = self.prompt_engine.generate_policy_prompt(vulnerabilities)
            prompt += f"\n\nFocus on {category} controls."
            
            # Generate policy with optimized settings
            policy_content = self.llm_manager.generate_with_retry(
                prompt,
                temperature=0.3,
                max_tokens=400  # Reduced for speed
            )
            
            # Create policy document
            policy_doc = {
                'framework': self.framework,
                'category': category,
                'generated_at': datetime.now().isoformat(),
                'vulnerability_count': len(vulnerabilities),
                'content': policy_content,
                'metadata': {
                    'llm_provider': self.llm_manager.provider_name
                }
            }
            
            # Save to file
            filename = f"{self.framework.lower()}_{category.lower()}_policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            output_file = self.output_dir / filename
            
            with open(output_file, 'w') as f:
                json.dump(policy_doc, f, indent=2)
            
            logger.info(f"Category policy generated: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Failed to generate {category} policy: {e}")
            return None
    
    def refine_policy(self, policy_file: Path, vulnerabilities: List[Dict]) -> Optional[Path]:
        """Refine and improve an existing policy - optimized"""
        logger.info(f"Refining policy: {policy_file}")
        
        try:
            # Load existing policy
            with open(policy_file, 'r') as f:
                policy_doc = json.load(f)
            
            draft_content = policy_doc.get('content', '')
            
            # Create refinement prompt
            prompt = self.prompt_engine.generate_refinement_prompt(draft_content, vulnerabilities)
            
            # Generate refined policy with optimized settings
            refined_content = self.llm_manager.generate_with_retry(
                prompt,
                temperature=0.2,
                max_tokens=400  # Reduced for speed
            )
            
            # Update policy document
            policy_doc['content'] = refined_content
            policy_doc['refined_at'] = datetime.now().isoformat()
            policy_doc['version'] = policy_doc.get('version', 1) + 1
            
            # Save refined version
            filename = policy_file.stem + f"_v{policy_doc['version']}.json"
            output_file = policy_file.parent / filename
            
            with open(output_file, 'w') as f:
                json.dump(policy_doc, f, indent=2)
            
            logger.info(f"Refined policy saved: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Failed to refine policy: {e}")
            return None
    
    def _group_by_category(self, vulnerabilities: List[Dict]) -> Dict[str, List[Dict]]:
        """Group vulnerabilities by category (SAST, SCA, DAST)"""
        grouped = {}
        for vuln in vulnerabilities:
            category = vuln.get('category', 'UNKNOWN')
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(vuln)
        return grouped
    
    def _group_by_severity(self, vulnerabilities: List[Dict]) -> Dict[str, List[Dict]]:
        """Group vulnerabilities by severity"""
        grouped = {}
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'UNKNOWN')
            if severity not in grouped:
                grouped[severity] = []
            grouped[severity].append(vuln)
        return grouped
