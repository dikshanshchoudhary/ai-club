from ._adapter import passive_result


def lookup(indicator: str) -> dict:
    return passive_result("alienvault_otx", indicator)

