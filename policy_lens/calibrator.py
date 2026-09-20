class EntropyCalibrator:
    def __init__(self, uncertainty_threshold=0.10):
        self.uncertainty_threshold = uncertainty_threshold

    def compute_uncertainty(self, evaluations):
        """Calculates uncertainty based on multi-agent consensus disagreement."""
        verdicts = [eval.get("verdict", "AMBIGUOUS") for eval in evaluations]
        
        # Count the most common verdict
        majority_count = max([verdicts.count(v) for v in set(verdicts)])
        
        # If 3/3 agree, disagreement is 0.0. If 2/3 agree, disagreement is 0.33.
        disagreement_ratio = 1.0 - (majority_count / len(verdicts))
        
        # Find the winning verdict
        consensus_verdict = max(set(verdicts), key=verdicts.count)
        
        # Grab the discrepancy text from the first evaluation that matches the consensus
        final_discrepancy = next(
            (eval["discrepancy_extracted"] for eval in evaluations if eval["verdict"] == consensus_verdict), 
            "Consensus reached without specific explanation."
        )
        
        return {
            "consensus_verdict": consensus_verdict,
            "discrepancy_extracted": final_discrepancy,
            "uncertainty_score": disagreement_ratio,
            "all_verdicts": verdicts
        }

    def requires_human_review(self, uncertainty_score):
        return uncertainty_score > self.uncertainty_threshold