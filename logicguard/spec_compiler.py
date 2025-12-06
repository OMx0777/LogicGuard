"""
Symbolic Spec Compiler: Translates LTLf formulas to DFA.
"""

from ltlf2dfa.ltlf2dfa import LTLf2DFA
from typing import List, Dict, Any
import json

class SpecCompiler:
    """
    Compiles natural language SOPs to LTLf and then to DFA.
    Note: NL to LTLf is manual for now; future: LLM-assisted.
    """

    def __init__(self):
        self.dfas = {}  # formula -> DFA

    def compile_formula(self, ltl_formula: str, ap: List[str]) -> Dict[str, Any]:
        """
        Compile LTLf formula to DFA.

        Args:
            ltl_formula (str): LTLf formula, e.g., "G (req -> F approved)"
            ap (List[str]): Atomic propositions, e.g., ["req", "approved"]

        Returns:
            Dict: Serialized DFA (states, transitions, accepting, initial).
        """
        try:
            parser = LTLf2DFA()
            dfa = parser(ltl_formula, ap)
            # Serialize for persistence
            serialized = {
                "states": list(dfa.states),
                "alphabet": dfa.alphabet,
                "transitions": {str(s): {tuple(k): str(v) for k, v in dfa.transitions[s].items()} for s in dfa.states},
                "initial": str(dfa.initial_state),
                "accepting": [str(s) for s in dfa.accepting_states]
            }
            self.dfas[ltl_formula] = serialized
            return serialized
        except Exception as e:
            raise ValueError(f"LTLf compilation failed: {e}")

    def load_dfa(self, serialized: Dict[str, Any]) -> 'DFAProxy':
        """
        Load serialized DFA (placeholder; use ltlf2dfa directly in prod).
        """
        # For simplicity, re-compile if needed; in prod, cache.
        return self.dfas.get(serialized.get("formula", ""), None)

# Placeholder DFAProxy for runtime use (simplified; extend with automata-lib if needed)
class DFAProxy:
    def __init__(self, serialized: Dict[str, Any]):
        self.states = serialized["states"]
        self.transitions = serialized["transitions"]
        self.initial = serialized["initial"]
        self.accepting = set(serialized["accepting"])
        self.current = self.initial

    def transition(self, labeling: Dict[str, bool]) -> bool:
        """Transition on bool vector; return if accepting."""
        word = tuple(1 if labeling.get(ap, False) else 0 for ap in self.alphabet)  # Binary word
        next_state = self.transitions[self.current].get(word)
        if next_state is None:
            return False  # Sink
        self.current = next_state
        return next_state in self.accepting