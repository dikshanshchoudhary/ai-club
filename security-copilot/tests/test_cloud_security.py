from agents.cloud_security import CloudSecurityAgent


def test_iam_routes_by_provider():
    assert CloudSecurityAgent().assess_iam("aws", "dev-account")["tool"] == "prowler"
    assert CloudSecurityAgent().assess_iam("azure", "dev-subscription")["tool"] == "scoutsuite"


def test_kubernetes_runs_benchmarks():
    result = CloudSecurityAgent().assess_kubernetes("dev-cluster")
    assert {check["tool"] for check in result["checks"]} == {"kube-bench", "kube-hunter"}

