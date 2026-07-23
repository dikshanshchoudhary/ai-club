import json
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


class ScannerExecutionError(RuntimeError):
    pass


def _run(command: list[str], *, cwd: str | None = None, timeout: int = 300) -> tuple[int, str, str]:
    if shutil.which(command[0]) is None:
        raise ScannerExecutionError(f"Required executable not found: {command[0]}")
    process = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)
    return process.returncode, process.stdout, process.stderr


def clone_repository(source: str, destination: str) -> str:
    if source.startswith(("http://", "https://", "git@", "ssh://")):
        code, _, stderr = _run(["git", "clone", "--depth", "1", source, destination], timeout=600)
        if code != 0:
            raise ScannerExecutionError(f"Repository clone failed: {stderr[-1000:]}")
        return destination
    path = Path(source).resolve()
    if not path.is_dir():
        raise ScannerExecutionError(f"Repository path does not exist: {source}")
    return str(path)


def _json_output(command: list[str], *, cwd: str) -> dict | list:
    _, stdout, stderr = _run(command, cwd=cwd)
    for candidate in (stdout, stderr):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return {"raw_output": stdout[-4000:], "error_output": stderr[-4000:]}


def execute_scanners(repository_path: str) -> list[dict]:
    """Run the four MVP scanners and preserve each native JSON result."""
    results = []
    commands = {
        "semgrep": ["semgrep", "scan", "--config", "auto", "--json", repository_path],
        "trivy": ["trivy", "fs", "--format", "json", repository_path],
        "checkov": ["checkov", "-d", repository_path, "-o", "json"],
    }
    for tool, command in commands.items():
        try:
            results.append({"tool": tool, "status": "completed", "data": _json_output(command, cwd=repository_path)})
        except (ScannerExecutionError, subprocess.TimeoutExpired) as exc:
            results.append({"tool": tool, "status": "unavailable", "error": str(exc)})

    with TemporaryDirectory(prefix="security-copilot-gitleaks-") as report_dir:
        report_path = str(Path(report_dir) / "gitleaks.json")
        try:
            code, stdout, stderr = _run(["gitleaks", "detect", "--source", repository_path, "--report-format", "json", "--report-path", report_path], cwd=repository_path)
            data = json.loads(Path(report_path).read_text(encoding="utf-8")) if Path(report_path).exists() else []
            results.append({"tool": "gitleaks", "status": "completed" if code in (0, 1) else "failed", "data": data, "stderr": stderr[-4000:], "stdout": stdout[-4000:]})
        except (ScannerExecutionError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            results.append({"tool": "gitleaks", "status": "unavailable", "error": str(exc)})
    return results

