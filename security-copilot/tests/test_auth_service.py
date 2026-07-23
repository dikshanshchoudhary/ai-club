import pytest

from app.auth.service import AuthConfig, AuthService, Role


def test_session_is_signed_and_scoped_to_one_organization():
    service = AuthService(AuthConfig(organization_id="acme", jwt_secret="test-secret"))
    token = service.create_session("user-1", Role.SECURITY_ENGINEER)
    claims = service.verify_session(token)
    assert claims["org"] == "acme"
    assert claims["role"] == "security_engineer"


def test_roles_have_expected_permissions():
    service = AuthService(AuthConfig(jwt_secret="test-secret"))
    assert service.can(Role.ADMIN, "approve_actions")
    assert service.can(Role.DEVELOPER, "run_scans")
    assert not service.can(Role.VIEWER, "approve_actions")


def test_missing_secret_blocks_session_creation():
    with pytest.raises(RuntimeError):
        AuthService(AuthConfig(jwt_secret="")).create_session("user-1", Role.VIEWER)

