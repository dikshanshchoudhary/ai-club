from dataclasses import dataclass
from typing import Protocol


class EmbeddingProvider(Protocol):
    name: str

    def embed(self, text: str) -> list[float]: ...


@dataclass
class EmbeddingAbstraction:
    provider: EmbeddingProvider | None = None

    def embed(self, text: str) -> dict:
        if self.provider is None:
            return {"status": "not_configured", "model": "text-embedding-3-large", "vector": []}
        return {"status": "completed", "model": self.provider.name, "vector": self.provider.embed(text)}

