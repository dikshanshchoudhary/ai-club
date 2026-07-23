from memory.registry import MEMORY_COLLECTIONS, get_collection


def test_memory_registry_contains_requested_collections():
    assert len(MEMORY_COLLECTIONS) == 6
    assert get_collection("organization_assets")["sensitivity"] == "confidential"
    assert get_collection("custom_rules")["local_path"] == "memory/custom_rules"

