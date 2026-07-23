from ._adapter import passive_result


def inspect(capture: str) -> dict:
    return passive_result("wireshark", capture)

