from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MemoryCollection:
    key: str
    name: str
    purpose: str
    local_path: str
    sensitivity: str


MEMORY_COLLECTIONS = {
    collection.key: collection
    for collection in [
        MemoryCollection("past_incidents", "Past incidents", "Historical incident records and outcomes", "memory/previous_incidents", "restricted"),
        MemoryCollection("attack_patterns", "Attack patterns", "Observed patterns and defensive correlations", "memory/attack_patterns", "internal"),
        MemoryCollection("previous_investigations", "Previous investigations", "Prior investigations, hypotheses, and evidence", "memory/previous_investigations", "restricted"),
        MemoryCollection("organization_assets", "Organization assets", "Known systems, services, owners, and criticality", "memory/organization_assets", "confidential"),
        MemoryCollection("known_vulnerabilities", "Known vulnerabilities", "Tracked vulnerabilities and remediation state", "memory/known_vulnerabilities", "internal"),
        MemoryCollection("custom_rules", "Custom rules", "Organization-specific detection and policy rules", "memory/custom_rules", "confidential"),
    ]
}


def get_collection(key: str) -> dict | None:
    collection = MEMORY_COLLECTIONS.get(key.lower())
    return asdict(collection) if collection else None

