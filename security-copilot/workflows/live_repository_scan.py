from pathlib import Path
from tempfile import TemporaryDirectory

from tools.real_scanners import clone_repository, execute_scanners


def normalize(results: list[dict]) -> list[dict]:
    findings = []
    for result in results:
        data = result.get("data", [])
        native_findings = data if isinstance(data, list) else data.get("results", data.get("findings", [])) if isinstance(data, dict) else []
        for finding in native_findings:
            findings.append({
                "tool": result["tool"],
                "severity": str(finding.get("severity", finding.get("level", "unknown"))).lower(),
                "rule_id": finding.get("check_id") or finding.get("VulnerabilityID") or finding.get("RuleID"),
                "title": finding.get("message") or finding.get("Title") or finding.get("name", "Security finding"),
                "file": finding.get("path") or finding.get("Target") or finding.get("File"),
                "line": finding.get("start", {}).get("line") if isinstance(finding.get("start"), dict) else finding.get("StartLine"),
                "raw": finding,
            })
    return findings


def run(source: str) -> dict:
    """Clone/use a repository, run scanners, and return normalized findings."""
    with TemporaryDirectory(prefix="security-copilot-repo-") as workspace:
        target = str(Path(workspace) / "repo")
        repository_path = clone_repository(source, target)
        scanner_results = execute_scanners(repository_path)
        findings = normalize(scanner_results)
        return {"source": source, "repository_path": repository_path, "scanners": scanner_results, "findings": findings, "finding_count": len(findings), "status": "completed"}


def run_and_store(source: str, database_url: str | None = None, repository_id: str | None = None) -> dict:
    result = run(source)
    if database_url and repository_id:
        from storage.postgres import PostgresFindingStore
        result["risk_score"] = min(100, result["finding_count"] * 10)
        PostgresFindingStore(database_url).save_scan(repository_id, result)
        result["stored"] = True
    else:
        result["stored"] = False
    return result
