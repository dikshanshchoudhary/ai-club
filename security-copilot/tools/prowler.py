from ._adapter import passive_result


def check(scope: str, check_type: str = "posture") -> dict:
    result = passive_result("prowler", scope)
    result["check_type"] = check_type
    return result

