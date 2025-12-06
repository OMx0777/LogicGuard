"""
Semantic Prober: Grounds symbols using SLM (GPT-4o-mini).
"""

import openai
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class SemanticProber:
    """
    Maps agent context to bool vector for atomic propositions.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.client = openai.OpenAI()

    def probe(self, context: Dict[str, Any], aps: List[str]) -> Dict[str, bool]:
        """
        Probe for each AP.

        Args:
            context (Dict): {"history": [...], "action_json": {...}}
            aps (List[str]): Atomic propositions, e.g., ["mgr_approval", "exec_refund"]

        Returns:
            Dict[str, bool]: e.g., {"mgr_approval": False, "exec_refund": True}
        """
        bool_vector = {}
        history_str = "\n".join([turn["content"] for turn in context.get("history", [])[-3:]])  # Last 3 turns
        action_str = json.dumps(context.get("action_json", {}))
        
        for ap in aps:
            prompt = f"""
You are a precise classifier. Analyze this context:
---
Agent History: {history_str}
Proposed Action: {action_str}
---
Question: Has "{ap}" been explicitly received/performed in this conversation?
Answer ONLY: YES or NO
"""
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=5
            )
            answer = response.choices[0].message.content.strip().upper()
            bool_vector[ap] = answer == "YES"
        
        return bool_vector