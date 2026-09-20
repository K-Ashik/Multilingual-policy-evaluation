# Policy-Lens-Eval 🔍

A closed-loop, multi-agent Large Language Model (LLM) evaluation framework for multilingual policy alignment and compliance governance. 

This Python package automates the detection of "requirements drift" between centralized baseline policies (English) and localized subsidiary documents (Foreign Languages). By utilizing Retrieval-Augmented Generation (RAG) and multi-agent consensus algorithms, the framework produces deterministic, mathematically calibrated audit trails for enterprise regulatory environments.

## 🏗 System Architecture

The framework is highly modular, bypassing standard conversational chat interfaces in favor of a headless pipeline designed for continuous CI/CD compliance integration:

1. **Retriever Module (`PolicyRetriever`):** A local, privacy-first vector database utilizing `ChromaDB` and `BAAI/bge-m3` sentence embeddings to instantly map foreign clauses to their corresponding English baseline rules.
2. **Assessor Module (`PolicyAssessor`):** A JSON-constrained generative evaluator powered by the Groq API (Llama/GPT-OSS architectures) that performs strict semantic discrepancy analysis.
3. **Calibrator Module (`EntropyCalibrator`):** Implements Self-Consistency (Multi-Agent Consensus). The system runs identical zero-shot evaluations across multiple isolated agents. If consensus fractures, the system calculates an uncertainty score and automatically triggers a human-in-the-loop escalation protocol.
4. **Reporter Module (`AuditReporter`):** Compiles the system telemetry, consensus data, and extracted text into a static, immutable HTML forensic report for regulatory storage.

## 🚀 Installation

Ensure you have Python 3.9+ installed, then clone the repository and install the dependencies:

```bash
git clone [https://github.com/yourusername/policy_lens_eval.git](https://github.com/yourusername/policy_lens_eval.git)
cd policy_lens_eval
pip install -r requirements.txt

```

## Set your API key for the generative Assessor module:

```bash
export GROQ_API_KEY="your_api_key_here"
```

## 💻 Usage Pipeline

The framework is designed to be imported seamlessly into existing digitalization pipelines or Jupyter Notebooks.

```bash

from policy_lens.retriever import PolicyRetriever
from policy_lens.assessor import PolicyAssessor
from policy_lens.calibrator import EntropyCalibrator
from policy_lens.reporter import AuditReporter

# 1. Initialize the Pipeline Components
retriever = PolicyRetriever(db_path="../policy_vector_db")
assessor = PolicyAssessor()
calibrator = EntropyCalibrator()
reporter = AuditReporter()

# 2. Ingest Target Clause
target_clause = "Amtsblatt der Europäischen Union, das innerhalb von 15 Tagen veröffentlicht werden muss."
match = retriever.search_baseline(target_clause)

# 3. Execute Multi-Agent Evaluation & Calibration
evaluations = assessor.evaluate_clause(match['matched_text'], target_clause)
calibration_data = calibrator.compute_uncertainty(evaluations)

# 4. Generate Static Audit Artifact
report_path = reporter.generate_html_report(target_clause, match['matched_text'], calibration_data)

```

## 🛡️ Telemetry & Audit Generation
The framework outputs strict, timestamped HTML artifacts detailing the extracted discrepancy, the multi-pass agent voting record, and the calculated uncertainty score.

## 🔬 Use Cases
**Requirements Engineering**: Measuring semantic drift in closed-loop software requirements.

**Compliance Digitalization**: Automating cross-border regulatory alignment checks (e.g., AML, Sanctions, Corporate Governance).

**Forensic Auditing**: Generating static, immutable records of AI decision-making for external regulators.
