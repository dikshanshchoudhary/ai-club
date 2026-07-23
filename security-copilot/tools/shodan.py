from ._adapter import passive_result


def lookup(target: str) -> dict:
    return passive_result("shodan", target)

