from ._adapter import passive_result


def lookup(identifier: str) -> dict:
    return passive_result("cve_lookup", identifier)

