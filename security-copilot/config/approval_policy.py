from dataclasses import dataclass
from enum import StrEnum


class ApprovalLevel(StrEnum):
    AUTOMATIC = "automatic"
    HUMAN_APPROVAL = "human_approval"
    EXPLICIT_DANGEROUS = "explicit_dangerous"


@dataclass(frozen=True)
class PolicyDecision:
    action: str
    level: ApprovalLevel
    allowed: bool
    reason: str


AUTOMATIC_ACTIONS = {
    "repository_scan", "cloud_scan", "read_logs", "read_github", "threat_lookup",
    "generate_report", "generate_fix", "risk_scoring",
}
HUMAN_APPROVAL_ACTIONS = {
    "delete_resources", "merge_pr", "close_incident", "restart_server", "modify_iam",
    "delete_kubernetes_resources", "block_ip", "firewall_change", "push_commit", "deploy_patch",
}
DANGEROUS_ACTIONS = {
    "terminate_ec2", "delete_s3", "rotate_credentials", "revoke_users", "delete_database", "production_deployment",
}


def check_action(action: str, *, explicit_approval: bool = False) -> PolicyDecision:
    action = action.lower()
    if action in AUTOMATIC_ACTIONS:
        return PolicyDecision(action, ApprovalLevel.AUTOMATIC, True, "Safe read-only or advisory action")
    if action in HUMAN_APPROVAL_ACTIONS:
        return PolicyDecision(action, ApprovalLevel.HUMAN_APPROVAL, explicit_approval, "Human approval is required before execution")
    if action in DANGEROUS_ACTIONS:
        return PolicyDecision(action, ApprovalLevel.EXPLICIT_DANGEROUS, False, "Dangerous operation is blocked by default")
    return PolicyDecision(action, ApprovalLevel.HUMAN_APPROVAL, False, "Unknown action requires review")


def require_approval(action: str, *, explicit_approval: bool = False) -> None:
    decision = check_action(action, explicit_approval=explicit_approval)
    if not decision.allowed:
        raise PermissionError(f"Action '{action}' blocked: {decision.reason}")

