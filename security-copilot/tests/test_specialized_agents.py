from agents.repository_agent import RepositoryAgent
from agents.risk_agent import score
from agents.scanner_agent import scan
from agents.vulnerability_agent import normalize


def test_specialized_agents_have_independent_boundaries():
    assert RepositoryAgent().prepare("https://github.com/acme/repo")["clone_required"] is True
    results = scan(".")
    assert len(results) == 4
    assert normalize(results)[0]["tool"] == "semgrep"
    assert score([{"severity": "high"}]) == 25

