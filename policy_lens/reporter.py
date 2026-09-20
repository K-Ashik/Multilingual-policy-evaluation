import datetime
import os

class AuditReporter:
    def __init__(self, output_dir="./audit_reports"):
        """Initializes the reporter and creates the output directory if it doesn't exist."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_html_report(self, target_clause, baseline_match, calibration_data):
        """Generates a static HTML forensic audit report."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"compliance_audit_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        # Determine the status color based on the verdict and uncertainty
        verdict = calibration_data['consensus_verdict']
        if calibration_data['uncertainty_score'] > 0:
            status_color = "#f59e0b" # Amber for uncertainty / human review
            status_text = "HUMAN REVIEW REQUIRED"
        elif verdict == "CONFLICT":
            status_color = "#ef4444" # Red for conflict
            status_text = "POLICY CONFLICT DETECTED"
        else:
            status_color = "#10b981" # Green for aligned
            status_text = "STRICTLY ALIGNED"

        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Automated Compliance Audit</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f9fafb; color: #111827; padding: 40px; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
                .header {{ border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; margin-bottom: 20px; }}
                .status-badge {{ background-color: {status_color}; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 0.9em; display: inline-block; }}
                h1 {{ font-size: 1.5em; margin: 0 0 10px 0; }}
                .section {{ margin-bottom: 20px; }}
                .section-title {{ font-weight: bold; color: #4b5563; text-transform: uppercase; font-size: 0.85em; margin-bottom: 5px; }}
                .box {{ background: #f3f4f6; padding: 15px; border-radius: 6px; border: 1px solid #e5e7eb; }}
                .telemetry {{ font-family: monospace; background: #1f2937; color: #10b981; padding: 15px; border-radius: 6px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Multilingual Policy Alignment Audit</h1>
                    <div class="status-badge">{status_text}</div>
                    <p style="color: #6b7280; font-size: 0.9em; margin-top: 10px;">Generated: {timestamp}</p>
                </div>
                
                <div class="section">
                    <div class="section-title">Extracted Discrepancy</div>
                    <div class="box" style="border-left: 4px solid {status_color};">
                        {calibration_data['discrepancy_extracted']}
                    </div>
                </div>

                <div class="section">
                    <div class="section-title">System Telemetry (Multi-Agent Consensus)</div>
                    <div class="telemetry">
                        > Uncertainty Score: {calibration_data['uncertainty_score']:.2f}<br>
                        > Agent Passes: {calibration_data['all_verdicts']}<br>
                        > Human Intervention Triggered: {calibration_data['uncertainty_score'] > 0}
                    </div>
                </div>

                <div class="section">
                    <div class="section-title">Analyzed Text</div>
                    <div class="box">
                        <strong>Target Clause (German):</strong><br>
                        {target_clause}
                        <br><br>
                        <strong>Baseline Matched (English):</strong><br>
                        {baseline_match}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(html_content)
            
        return filepath