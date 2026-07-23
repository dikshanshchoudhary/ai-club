from ._adapter import passive_result


def search(indicator: str) -> dict:
    return passive_result("misp", indicator)

