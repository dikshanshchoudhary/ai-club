from ._adapter import passive_result


def check(scope: str, provider: str = "aws", check_type: str = "posture") -> dict:
    result = passive_result("scoutsuite", scope)
    result.update({"provider": provider, "check_type": check_type})
    return result

