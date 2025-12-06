"""
Runtime Gatekeeper: Enforces DFA transitions.
"""

from typing import Dict, Any, Optional
import json

class RuntimeGatekeeper:
    """
    Monitors agent actions against DFA.
    """

    def __init__(self, dfa_serialized: Dict[str, Any], aps: List[str]):
        self.dfa = DFAProxy(dfa_serialized)  # From spec_compiler
        self.aps = aps
        self.current_state = self.dfa.initial

    def check_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check proposed action.

        Args:
            context (Dict): Agent context for prober.

        Returns:
            Dict: {"safe": bool, "reason": str, "feedback": Dict} if blocked.
        """
        # Probe symbols
        prober = SemanticProber()
        labeling = prober.probe(context, self.aps)
        
        # Transition
        safe = self.dfa.transition(labeling)
        
        if safe:
            return {"safe": True}
        
        # Blocked: Provide feedback
        feedback = {
            "status": "BLOCKED",
            "reason": f"Violation detected in state {self.dfa.current} with labeling {labeling}",
            "required_before_retry": [ap for ap, val in labeling.items() if not val]  # Example
        }
        return {"safe": False, "feedback": feedback}