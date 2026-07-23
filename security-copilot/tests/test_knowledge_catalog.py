from knowledge.catalog import KNOWLEDGE_SOURCES, get_source


def test_catalog_contains_requested_sources():
    assert len(KNOWLEDGE_SOURCES) == 10
    assert get_source("cisa_kev")["category"] == "vulnerability"
    assert get_source("pci_dss")["category"] == "compliance"

