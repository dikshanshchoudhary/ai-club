from agents.code_security import CodeSecurityAgent


def test_agent_runs_configured_check_boundaries():
    result = CodeSecurityAgent().find_vulnerabilities(".")
    assert {check["tool"] for check in result["checks"]} == {"semgrep", "codeql", "trivy"}


def test_agent_generates_secure_coding_suggestion():
    suggestions = CodeSecurityAgent().suggest_secure_coding([{"category": "secret"}])
    assert suggestions[0]["title"] == "Remove embedded secrets"

