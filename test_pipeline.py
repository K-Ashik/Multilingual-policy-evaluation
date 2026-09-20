import json
from policy_lens.retriever import PolicyRetriever
from policy_lens.assessor import PolicyAssessor
from policy_lens.calibrator import EntropyCalibrator
from policy_lens.reporter import AuditReporter # Import the new module

def run_evaluation():
    print("Initializing Pipeline...")
    retriever = PolicyRetriever(db_path="../policy_vector_db")
    assessor = PolicyAssessor()
    calibrator = EntropyCalibrator()
    reporter = AuditReporter() # Initialize the reporter

    test_german_clause = "Diese Verordnung bietet einen klaren Weg zur Reduzierung der CO2-Emissionen im Straßenverkehr und trägt zu dem verbindlichen Ziel bei, die Treibhausgasemissionen bis 2030 um mindestens 40 % im Vergleich zu 1990 zu senken."
    
    print(f"\n1. Target Clause: {test_german_clause}")
    
    print("2. Retrieving English Baseline...")
    match = retriever.search_baseline(test_german_clause)
    if not match:
        return
    print(f"   -> Found Match: {match['matched_text'][:100]}...")

    print("\n3. Running Multi-Agent Assessment (3 Passes)...")
    evaluations = assessor.evaluate_clause(
        english_baseline=match['matched_text'],
        foreign_clause=test_german_clause
    )
    
    print("4. Calibrating Consensus Uncertainty...")
    calibration = calibrator.compute_uncertainty(evaluations)
    
    print("5. Generating Static HTML Audit Report...")
    report_path = reporter.generate_html_report(
        target_clause=test_german_clause,
        baseline_match=match['matched_text'],
        calibration_data=calibration
    )
    
    print(f"\nSUCCESS: Pipeline complete. Audit saved to: {report_path}")

if __name__ == "__main__":
    run_evaluation()