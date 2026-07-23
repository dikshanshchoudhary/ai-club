from ._adapter import passive_result


def query(query_text: str) -> dict:
    return passive_result("osquery", query_text)

