"""
Domain-specific LTL specifications.
"""

# Refund Domain
PHI_REFUND1 = "neg(exec_refund) U (mgr_approval)"  # No refund until approval
PHI_REFUND2 = "G (amount > 1000 -> dual_approval)"  # Global for high amounts

# Auth Domain
PHI_AUTH1 = "G (pwd_change -> F 2fa_success)"
PHI_AUTH2 = "neg(delete_account) U (user_consent)"

# Logistics
PHI_LOG1 = "G ((high_value & reroute) -> F supervisor_ok)"
PHI_LOG2 = "G (intl_ship -> F customs_cleared)"

APS_REFUND = ["exec_refund", "mgr_approval", "amount", "dual_approval"]