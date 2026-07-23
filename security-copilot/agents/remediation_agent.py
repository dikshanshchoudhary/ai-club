from agents.code_security import CodeSecurityAgent


def suggest(findings: list[dict]) -> list[dict]:
    agent = CodeSecurityAgent()
    return [{"finding": finding, "suggestions": agent.suggest_secure_coding([finding])} for finding in findings]

