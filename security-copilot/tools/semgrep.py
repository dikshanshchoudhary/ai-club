from ._adapter import passive_result


def scan(path: str, ruleset: str = "auto") -> dict:
    result = passive_result("semgrep", path)
    result["ruleset"] = ruleset
    return result
