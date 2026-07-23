from ._adapter import passive_result


def scan(path: str) -> dict:
    return passive_result("checkov", path)

