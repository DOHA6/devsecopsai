"""
Policy Evaluator
Evaluates generated policies using BLEU, ROUGE-L, and custom metrics
"""

import json
from pathlib import Path
from typing import Dict, List
from loguru import logger
from datetime import datetime


class PolicyEvaluator:
    """Evaluates generated security policies"""
    
    def __init__(
        self,
        generated_dir: str,
        reference_dir: str,
        output_dir: str = "./output/evaluation_results"
    ):
        self.generated_dir = Path(generated_dir)
        self.reference_dir = Path(reference_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def evaluate(self, metrics: List[str] = None) -> Dict:
        """
        Evaluate generated policies
        
        Args:
            metrics: List of metrics to calculate (BLEU, ROUGE-L, COMPLIANCE)
        
        Returns:
            Dictionary of evaluation results
        """
        if metrics is None:
            metrics = ['BLEU', 'ROUGE-L', 'COMPLIANCE']
        
        logger.info(f"Evaluating policies with metrics: {metrics}")
        
        # Load generated and reference policies
        generated_policies = self._load_policies(self.generated_dir)
        reference_policies = self._load_policies(self.reference_dir)
        
        if not generated_policies:
            raise ValueError("No generated policies found")
        
        if not reference_policies:
            logger.warning("No reference policies found. Some metrics unavailable.")
            reference_policies = []
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'generated_count': len(generated_policies),
            'reference_count': len(reference_policies),
            'metrics': {}
        }
        
        # Calculate each metric
        for metric in metrics:
            if metric.upper() == 'BLEU':
                results['metrics']['BLEU'] = self._calculate_bleu(
                    generated_policies, reference_policies
                )
            elif metric.upper() == 'ROUGE-L':
                results['metrics']['ROUGE-L'] = self._calculate_rouge(
                    generated_policies, reference_policies
                )
            elif metric.upper() == 'COMPLIANCE':
                results['metrics']['COMPLIANCE'] = self._calculate_compliance(
                    generated_policies
                )
            elif metric.upper() == 'READABILITY':
                results['metrics']['READABILITY'] = self._calculate_readability(
                    generated_policies
                )
        
        # Save results
        self._save_results(results)
        
        return results['metrics']
    
    def _load_policies(self, directory: Path) -> List[Dict]:
        """Load policy files from directory"""
        policies = []
        
        for json_file in directory.glob('*.json'):
            try:
                with open(json_file, 'r') as f:
                    policy = json.load(f)
                    policy['file'] = str(json_file)
                    policies.append(policy)
            except Exception as e:
                logger.error(f"Failed to load {json_file}: {e}")
        
        return policies
    
    def _calculate_bleu(self, generated: List[Dict], reference: List[Dict]) -> float:
        """Calculate BLEU score"""
        if not reference:
            logger.warning("No reference policies for BLEU calculation")
            return 0.0
        
        try:
            from sacrebleu import corpus_bleu
            
            # Extract content
            generated_texts = [p.get('content', '') for p in generated]
            reference_texts = [[p.get('content', '')] for p in reference]
            
            # Ensure we have matching pairs
            min_len = min(len(generated_texts), len(reference_texts))
            generated_texts = generated_texts[:min_len]
            reference_texts = reference_texts[:min_len]
            
            if not generated_texts or not reference_texts:
                return 0.0
            
            # Calculate BLEU
            bleu = corpus_bleu(generated_texts, reference_texts)
            score = bleu.score / 100.0  # Normalize to 0-1
            
            logger.info(f"BLEU score: {score:.4f}")
            return score
            
        except ImportError:
            logger.error("sacrebleu not installed. Install with: pip install sacrebleu")
            return 0.0
        except Exception as e:
            logger.error(f"BLEU calculation failed: {e}")
            return 0.0
    
    def _calculate_rouge(self, generated: List[Dict], reference: List[Dict]) -> float:
        """Calculate ROUGE-L score"""
        if not reference:
            logger.warning("No reference policies for ROUGE calculation")
            return 0.0
        
        try:
            from rouge_score import rouge_scorer
            
            scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
            
            scores = []
            for gen_policy in generated:
                gen_text = gen_policy.get('content', '')
                
                # Compare with all reference policies and take max score
                max_score = 0.0
                for ref_policy in reference:
                    ref_text = ref_policy.get('content', '')
                    score = scorer.score(ref_text, gen_text)
                    max_score = max(max_score, score['rougeL'].fmeasure)
                
                scores.append(max_score)
            
            avg_score = sum(scores) / len(scores) if scores else 0.0
            logger.info(f"ROUGE-L score: {avg_score:.4f}")
            return avg_score
            
        except ImportError:
            logger.error("rouge-score not installed. Install with: pip install rouge-score")
            return 0.0
        except Exception as e:
            logger.error(f"ROUGE calculation failed: {e}")
            return 0.0
    
    def _calculate_compliance(self, generated: List[Dict]) -> float:
        """Calculate compliance score based on framework requirements"""
        scores = []
        
        for policy in generated:
            framework = policy.get('framework', '')
            content = policy.get('content', '').lower()
            
            # Define required elements for each framework
            required_elements = self._get_required_elements(framework)
            
            # Check presence of required elements
            present = sum(1 for element in required_elements if element.lower() in content)
            score = present / len(required_elements) if required_elements else 0.0
            scores.append(score)
        
        avg_score = sum(scores) / len(scores) if scores else 0.0
        logger.info(f"Compliance score: {avg_score:.4f}")
        return avg_score
    
    def _calculate_readability(self, generated: List[Dict]) -> float:
        """Calculate readability score"""
        try:
            import textstat
            
            scores = []
            for policy in generated:
                content = policy.get('content', '')
                # Flesch Reading Ease: 0-100 (higher = easier)
                score = textstat.flesch_reading_ease(content)
                # Normalize to 0-1
                normalized = max(0, min(100, score)) / 100.0
                scores.append(normalized)
            
            avg_score = sum(scores) / len(scores) if scores else 0.0
            logger.info(f"Readability score: {avg_score:.4f}")
            return avg_score
            
        except ImportError:
            logger.error("textstat not installed. Install with: pip install textstat")
            return 0.0
        except Exception as e:
            logger.error(f"Readability calculation failed: {e}")
            return 0.0
    
    def _get_required_elements(self, framework: str) -> List[str]:
        """Get required elements for framework compliance"""
        elements = {
            'NIST_CSF': [
                'identify', 'protect', 'detect', 'respond', 'recover',
                'risk assessment', 'security controls', 'monitoring',
                'incident response', 'asset management'
            ],
            'ISO_27001': [
                'scope', 'information security policy', 'risk assessment',
                'security controls', 'annex a', 'organizational controls',
                'monitoring', 'continual improvement', 'management review'
            ],
            'CIS_CONTROLS': [
                'inventory', 'data protection', 'secure configuration',
                'account management', 'access control', 'vulnerability management',
                'audit log', 'application security'
            ]
        }
        
        return elements.get(framework, [])
    
    def _save_results(self, results: Dict):
        """Save evaluation results"""
        # Save JSON summary
        summary_file = self.output_dir / 'summary.json'
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Evaluation results saved: {summary_file}")
        
        # Save detailed report as Markdown
        report_file = self.output_dir / 'evaluation_report.md'
        with open(report_file, 'w') as f:
            f.write("# Security Policy Evaluation Report\n\n")
            f.write(f"**Generated:** {results['timestamp']}\n\n")
            f.write(f"**Policies Evaluated:** {results['generated_count']}\n")
            f.write(f"**Reference Policies:** {results['reference_count']}\n\n")
            f.write("## Metrics\n\n")
            
            for metric, score in results['metrics'].items():
                f.write(f"- **{metric}**: {score:.4f}\n")
            
            f.write("\n## Interpretation\n\n")
            f.write(self._generate_interpretation(results['metrics']))
        
        logger.info(f"Evaluation report saved: {report_file}")
    
    def _generate_interpretation(self, metrics: Dict) -> str:
        """Generate human-readable interpretation of results"""
        interpretation = []
        
        if 'BLEU' in metrics:
            score = metrics['BLEU']
            if score >= 0.5:
                interpretation.append("✅ **BLEU**: Excellent similarity to reference policies")
            elif score >= 0.3:
                interpretation.append("⚠️ **BLEU**: Moderate similarity to reference policies")
            else:
                interpretation.append("❌ **BLEU**: Low similarity to reference policies")
        
        if 'ROUGE-L' in metrics:
            score = metrics['ROUGE-L']
            if score >= 0.5:
                interpretation.append("✅ **ROUGE-L**: Strong content overlap with references")
            elif score >= 0.3:
                interpretation.append("⚠️ **ROUGE-L**: Moderate content overlap")
            else:
                interpretation.append("❌ **ROUGE-L**: Limited content overlap")
        
        if 'COMPLIANCE' in metrics:
            score = metrics['COMPLIANCE']
            if score >= 0.8:
                interpretation.append("✅ **COMPLIANCE**: Excellent framework adherence")
            elif score >= 0.6:
                interpretation.append("⚠️ **COMPLIANCE**: Good framework adherence")
            else:
                interpretation.append("❌ **COMPLIANCE**: Insufficient framework coverage")
        
        return "\n".join(interpretation)
