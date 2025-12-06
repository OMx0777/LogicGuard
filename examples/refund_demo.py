"""
Demo: Refund workflow.
"""

import os
from dotenv import load_dotenv
from logicguard import SpecCompiler, SemanticProber, RuntimeGatekeeper
from examples.ltl_specs import PHI_REFUND1, APS_REFUND

load_dotenv()

def demo():
    # Compile spec
    compiler = SpecCompiler()
    dfa = compiler.compile_formula(PHI_REFUND1, APS_REFUND)
    
    # Simulate context (no approval, attempt refund)
    context = {
        "history": [{"content": "User requests $150 refund."}],
        "action_json": {"tool": "exec_refund", "amount": 150}
    }
    
    # Probe & Gatekeep
    prober = SemanticProber()
    labeling = prober.probe(context, APS_REFUND)
    gatekeeper = RuntimeGatekeeper(dfa, APS_REFUND)
    result = gatekeeper.check_action(context)
    
    print("Labeling:", labeling)
    print("Safe?", result["safe"])
    if not result["safe"]:
        print("Feedback:", result["feedback"])

if __name__ == "__main__":
    demo()