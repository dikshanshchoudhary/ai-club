from ._adapter import passive_result


def lookup(ip: str) -> dict:
    return passive_result("abuseipdb", ip)

