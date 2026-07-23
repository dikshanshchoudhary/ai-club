from ._adapter import passive_result


def scan(target: str) -> dict:
    return passive_result("trivy", target)

