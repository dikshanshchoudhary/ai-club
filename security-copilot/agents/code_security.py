from dataclasses import dataclass

from tools import checkov, codeql, gitleaks, semgrep, trivy
from tools.github_api import GitHubClient


@dataclass
class CodeSecurityAgent:
    """Coordinate read-only code security checks and review preparation."""

    github: GitHubClient | None = None

    def find_vulnerabilities(self, path: str) -> dict:
        return {"path": path, "checks": [semgrep.scan(path), codeql.scan(path), trivy.scan(path), gitleaks.scan(path), checkov.scan(path)], "status": "completed"}

    def detect_secrets(self, path: str) -> dict:
        return {"path": path, "result": semgrep.scan(path, ruleset="secrets"), "status": "completed"}

    def review_pull_request(self, owner: str, repository: str, number: int) -> dict:
        if self.github is None:
            return {"owner": owner, "repository": repository, "number": number, "status": "not_configured"}
        return {"pull_request": self.github.get_pull_request(owner, repository, number), "status": "review_ready"}

    def suggest_secure_coding(self, findings: list[dict]) -> list[dict]:
        suggestions = []
        for finding in findings:
            category = str(finding.get("category", "")).lower()
            if "secret" in category:
                suggestions.append({"title": "Remove embedded secrets", "action": "Rotate the secret and use a managed secret store."})
            elif "injection" in category:
                suggestions.append({"title": "Prevent injection", "action": "Use parameterized APIs and validate untrusted input."})
            elif "dependency" in category or "cve" in category:
                suggestions.append({"title": "Update vulnerable dependencies", "action": "Upgrade to a supported fixed version and pin it."})
            else:
                suggestions.append({"title": "Review finding manually", "action": "Confirm exploitability and add a regression test."})
        return suggestions


def analyze_repository(path: str) -> dict:
    return CodeSecurityAgent().find_vulnerabilities(path)
