from workflows.scan_repository import run


def test_repository_pipeline_runs_requested_scanners_and_reports():
    result = run(".")
    assert result["gitleaks_scan"]["tool"] == "gitleaks"
    assert result["checkov_scan"]["tool"] == "checkov"
    assert result["reports"]["executive"]["report_type"] == "executive"
    assert result["reports"]["technical"]["report_type"] == "technical"
    assert result["github_issue"]["status"] == "not_requested"


def test_github_issue_requires_approval():
    result = run(".", open_github_issue=True)
    assert result["github_issue"]["status"] == "approval_required"

