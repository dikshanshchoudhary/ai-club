from workflows.live_repository_scan import normalize


def test_native_scanner_results_are_normalized():
    findings = normalize([{"tool": "semgrep", "data": {"results": [{"check_id": "xss", "path": "app.py", "start": {"line": 4}, "extra": {"message": "Unsafe output"}}]}}])
    assert findings[0]["tool"] == "semgrep"
    assert findings[0]["rule_id"] == "xss"
    assert findings[0]["file"] == "app.py"
    assert findings[0]["line"] == 4

