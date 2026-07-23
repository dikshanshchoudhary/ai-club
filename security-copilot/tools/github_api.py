from dataclasses import dataclass


@dataclass
class GitHubClient:
    """Inject a configured read-only transport when GitHub integration is enabled."""

    transport: object | None = None

    def get_pull_request(self, owner: str, repository: str, number: int) -> dict:
        if self.transport is None:
            return {"owner": owner, "repository": repository, "number": number, "status": "not_configured"}
        return self.transport.get(f"/repos/{owner}/{repository}/pulls/{number}")

