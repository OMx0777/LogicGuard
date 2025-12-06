"""
Basic unit test.
"""

import pytest
from logicguard.spec_compiler import SpecCompiler
from logicguard.runtime_gatekeeper import RuntimeGatekeeper
from examples.ltl_specs import PHI_REFUND1, APS_REFUND

def test_block_without_approval():
    compiler = SpecCompiler()
    dfa = compiler.compile_formula(PHI_REFUND1, APS_REFUND)
    context = {
        "history": [{"content": "No approval."}],
        "action_json": {"tool": "exec_refund"}
    }
    gatekeeper = RuntimeGatekeeper(dfa, APS_REFUND)
    result = gatekeeper.check_action(context)
    assert not result["safe"]

# Run with: pytest tests/