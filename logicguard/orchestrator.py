"""
Orchestrator: Integrates modules as middleware.
"""

from typing import Callable, Dict, Any
import json

class LogicGuardOrchestrator:
    """
    Proxy for agent-tool calls.
    """

    def __init__(self, ltl_formula: str, aps: List[str], agent_call: Callable, tool_call: Callable):
        self.compiler = SpecCompiler()
        dfa_serialized = self.compiler.compile_formula(ltl_formula, aps)
        self.gatekeeper = RuntimeGatekeeper(dfa_serialized, aps)
        self.agent_call = agent_call  # e.g., lambda prompt: openai.chat(...)
        self.tool_call = tool_call    # e.g., lambda action: env.execute(action)

    def run(self, user_input: str, history: List[Dict]) -> Dict[str, Any]:
        """
        Orchestrate a turn: Agent proposes -> Gatekeep -> Tool if safe.
        """
        # Agent proposes action
        prompt = f"History: {json.dumps(history)}\nUser: {user_input}\nPropose action JSON:"
        agent_response = self.agent_call(prompt)
        try:
            action_json = json.loads(agent_response)
        except:
            action_json = {"action": "respond", "content": agent_response}

        context = {"history": history, "action_json": action_json}
        gate_result = self.gatekeeper.check_action(context)

        if gate_result["safe"]:
            # Execute tool
            tool_output = self.tool_call(action_json)
            return {"action": "tool", "output": tool_output}
        else:
            # Feedback to agent
            feedback_prompt = f"{prompt}\nBlocked: {gate_result['feedback']}\nRe-plan:"
            new_response = self.agent_call(feedback_prompt)
            return {"action": "respond", "content": new_response, "blocked": True}