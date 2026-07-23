from ._adapter import passive_result


def check(cluster: str) -> dict:
    return passive_result("kube-bench", cluster)

