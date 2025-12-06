# LogicGuard
# LogicGuard: Neurosymbolic AgenticOps for Runtime Enforcement of SOPs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

LogicGuard is a neurosymbolic framework for enforcing Standard Operating Procedures (SOPs) in LLM-based agents using Linear Temporal Logic on Finite Traces (LTLf). It mitigates "Logic Drift" by wrapping agents in a deterministic runtime monitor.

This repo contains the prototype implementation from the paper:  
**Neurosymbolic AgenticOps: Runtime Enforcement of Standard Operating Procedures to Mitigate Stochastic Failure**  
*Om Sathe, 2025*

## Quick Start

1. **Install Dependencies** (Python 3.11+):
   ```bash
   pip install -r requirements.txt