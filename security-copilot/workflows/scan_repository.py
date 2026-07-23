from agents.code_security import CodeSecurityAgent
from agents.planner import SecurityPlanner
from agents.report_generator import SecurityReportAgent
from agents.repository_agent import RepositoryAgent
from agents.risk_agent import score as risk_score
from agents.scanner_agent import scan as run_scanners
from agents.vulnerability_agent import explain, normalize
from agents.remediation_agent import suggest
from config.approval_policy import check_action
from models.llm import complete


def run(path: str, report_type: str = "technical", output_format: str = "markdown", *, open_github_issue: bool = False, issue_approved: bool = False) -> dict:
    """Run the repository scan pipeline and return every reviewable stage."""
    planner = SecurityPlanner()
    agent = CodeSecurityAgent()
    plan = planner.create_plan({"objective": "scan repository", "scope": {"path": path}})
    repository = RepositoryAgent().prepare(path)
    vulnerability_scan = agent.find_vulnerabilities(path)
    secret_scan = agent.detect_secrets(path)
    normalized_findings = normalize(run_scanners(path) + [secret_scan["result"]])
    findings = normalized_findings
    analysis = {
        "finding_count": len(findings),
        "findings": findings,
        "summary": complete("Analyze normalized repository security findings and identify the highest-risk issues."),
    }
    score = risk_score(findings)
    explanations = explain(findings)
    suggestions = suggest(findings)
    reports = {
        "executive": SecurityReportAgent().create(findings, "executive", output_format),
        "technical": SecurityReportAgent().create(findings, "technical", output_format),
    }
    issue = {"status": "not_requested"}
    if open_github_issue:
        decision = check_action("push_commit", explicit_approval=issue_approved)
        issue = {"status": "ready" if decision.allowed else "approval_required", "reason": decision.reason}
    return {
        "plan": plan,
        "repository": repository,
        "semgrep_scan": vulnerability_scan["checks"][0],
        "trivy_scan": vulnerability_scan["checks"][2],
        "gitleaks_scan": vulnerability_scan["checks"][3],
        "checkov_scan": vulnerability_scan["checks"][4],
        "normalized_findings": normalized_findings,
        "secret_detection": secret_scan,
        "ai_analysis": analysis,
        "risk_score": score,
        "vulnerability_explanations": explanations,
        "fix_suggestions": suggestions,
        "reports": reports,
        "report": reports["technical"],
        "github_issue": issue,
        "status": "completed",
    }
