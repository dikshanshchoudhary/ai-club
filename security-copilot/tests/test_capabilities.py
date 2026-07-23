from agents.capabilities import CAPABILITIES, describe_capability
from agents.planner import SecurityPlanner


def test_advanced_capabilities_are_registered():
    assert len(CAPABILITIES) == 12
    assert describe_capability("cloud_posture")["category"] == "cloud"


def test_planner_routes_multi_agent_workflow():
    plan = SecurityPlanner().create_plan({"capability": "autonomous_investigation"})
    assert plan["stages"] == ["planner", "scanner", "analyst", "responder", "reporter"]

