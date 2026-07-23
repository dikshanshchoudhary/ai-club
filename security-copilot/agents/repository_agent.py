from dataclasses import dataclass


@dataclass
class RepositoryAgent:
    def prepare(self, source: str) -> dict:
        return {"source": source, "status": "ready", "clone_required": source.startswith(("http://", "https://", "git@"))}

