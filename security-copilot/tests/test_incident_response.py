from agents.incident_response import IncidentResponseAgent


def test_response_plan_contains_all_phases_and_requires_approval():
    plan = IncidentResponseAgent().generate_response_plan({"ransomware": True})
    assert [phase["name"] for phase in plan["phases"]] == ["triage", "containment", "eradication", "recovery"]
    assert plan["requires_approval"] is True
    assert "Isolate suspected hosts from the network" in plan["phases"][1]["actions"]


def test_timeline_is_ordered():
    timeline = IncidentResponseAgent().generate_timeline([
        {"timestamp": "2026-01-02"},
        {"timestamp": "2026-01-01"},
    ])
    assert timeline[0]["timestamp"] == "2026-01-01"

