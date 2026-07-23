from dataclasses import dataclass, field


@dataclass
class InMemoryRetriever:
    """MVP retrieval boundary; replace storage with Qdrant in production."""

    documents: list[dict] = field(default_factory=list)

    def add(self, document: dict) -> None:
        self.documents.append(document)

    def search(self, query: str, limit: int = 5) -> list[dict]:
        terms = set(query.lower().split())
        scored = []
        for document in self.documents:
            text = str(document).lower()
            score = sum(term in text for term in terms)
            if score:
                scored.append((score, document))
        return [document for _, document in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]

