import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    SECURITY_ENGINEER = "security_engineer"
    DEVELOPER = "developer"
    VIEWER = "viewer"


@dataclass(frozen=True)
class AuthConfig:
    organization_id: str = os.getenv("ORGANIZATION_ID", "default")
    jwt_secret: str = os.getenv("JWT_SECRET", "")
    github_client_id: str | None = os.getenv("GITHUB_OAUTH_CLIENT_ID")
    google_client_id: str | None = os.getenv("GOOGLE_OAUTH_CLIENT_ID")


class AuthService:
    """MVP auth boundary for one organization and signed, expiring sessions."""

    def __init__(self, config: AuthConfig | None = None):
        self.config = config or AuthConfig()

    def oauth_providers(self) -> list[str]:
        return [name for name, configured in (("github", self.config.github_client_id), ("google", self.config.google_client_id)) if configured]

    def create_session(self, subject: str, role: Role, *, expires_in: int = 3600) -> str:
        if not self.config.jwt_secret:
            raise RuntimeError("JWT_SECRET must be configured")
        header = self._encode({"alg": "HS256", "typ": "JWT"})
        payload = self._encode({"sub": subject, "role": role.value, "org": self.config.organization_id, "exp": int(time.time()) + expires_in})
        unsigned = f"{header}.{payload}"
        signature = self._sign(unsigned)
        return f"{unsigned}.{signature}"

    def verify_session(self, token: str) -> dict:
        try:
            header, payload, signature = token.split(".")
            unsigned = f"{header}.{payload}"
            if not hmac.compare_digest(signature, self._sign(unsigned)):
                raise ValueError("invalid signature")
            claims = json.loads(self._decode(payload))
            if claims["org"] != self.config.organization_id or claims["exp"] < time.time():
                raise ValueError("invalid or expired session")
            return claims
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            raise PermissionError("Invalid session") from exc

    def can(self, role: Role, permission: str) -> bool:
        permissions = {
            Role.ADMIN: {"manage_users", "run_scans", "approve_actions", "view_reports"},
            Role.SECURITY_ENGINEER: {"run_scans", "approve_actions", "view_reports"},
            Role.DEVELOPER: {"run_scans", "view_reports"},
            Role.VIEWER: {"view_reports"},
        }
        return permission in permissions[role]

    @staticmethod
    def _encode(value: dict) -> str:
        raw = json.dumps(value, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(raw).decode().rstrip("=")

    @staticmethod
    def _decode(value: str) -> str:
        return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)).decode()

    def _sign(self, value: str) -> str:
        digest = hmac.new(self.config.jwt_secret.encode(), value.encode(), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(digest).decode().rstrip("=")

