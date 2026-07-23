from config.settings import Settings


def test_settings_reports_configured_integrations_without_exposing_values():
    settings = Settings(openai_api_key="secret", github_token="token")
    assert settings.configured_integrations() == ["openai", "github"]

