from workflows.live_repository_scan import normalize


def test_scan_job_flow_has_normalizable_results():
    result = normalize([{"tool": "trivy", "data": {"Results": [{"Target": "image", "Vulnerabilities": []}]}}])
    assert isinstance(result, list)

