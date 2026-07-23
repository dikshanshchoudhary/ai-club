from ._adapter import passive_result


def match(source: str) -> dict:
    return passive_result("sigma", source)

