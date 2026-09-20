import json
import os
from groq import Groq

class PolicyAssessor:
    def __init__(self, api_key=None):
        self.client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY"))
        self.model = "openai/gpt-oss-120b" # The model that worked for you

    def evaluate_clause(self, english_baseline, foreign_clause):
        prompt = f"""
        You are a strict compliance auditor.
        
        ENGLISH BASELINE RULE:
        {english_baseline}
        
        LOCALIZED FOREIGN CLAUSE:
        {foreign_clause}
        
        Evaluate if the foreign clause strictly aligns with the baseline rule. 
        Respond ONLY with a JSON object using this exact schema:
        {{
            "verdict": "ALIGNED" or "CONFLICT" or "AMBIGUOUS",
            "discrepancy_extracted": "A 1-2 sentence explanation of the specific difference, if any."
        }}
        """
        
        evaluations = []
        # Run 3 times with higher temperature for consensus variance
        for _ in range(3):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.5 
            )
            evaluations.append(json.loads(response.choices[0].message.content))
            
        return evaluations