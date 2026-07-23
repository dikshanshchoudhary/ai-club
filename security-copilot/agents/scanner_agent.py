from tools import checkov, gitleaks, semgrep, trivy


def scan(path: str) -> list[dict]:
    return [semgrep.scan(path), trivy.scan(path), gitleaks.scan(path), checkov.scan(path)]

