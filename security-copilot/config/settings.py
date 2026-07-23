import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str | None = os.getenv("DATABASE_URL")
    primary_llm: str = os.getenv("PRIMARY_LLM", "gemini")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    fallback_llms: str = os.getenv("FALLBACK_LLMS", "claude,gemini,llama")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    github_token: str | None = os.getenv("GITHUB_TOKEN")
    aws_region: str | None = os.getenv("AWS_REGION")
    azure_client_id: str | None = os.getenv("AZURE_CLIENT_ID")
    azure_tenant_id: str | None = os.getenv("AZURE_TENANT_ID")
    gcp_service_account_file: str | None = os.getenv("GCP_SERVICE_ACCOUNT_FILE")
    virustotal_api_key: str | None = os.getenv("VT_API_KEY")
    shodan_api_key: str | None = os.getenv("SHODAN_KEY")
    secret_provider: str | None = os.getenv("SECRET_PROVIDER")

    def configured_integrations(self) -> list[str]:
        configured = []
        if self.gemini_api_key:
            configured.append("gemini")
        if self.openai_api_key:
            configured.append("openai")
        if self.github_token:
            configured.append("github")
        if self.virustotal_api_key:
            configured.append("virustotal")
        if self.shodan_api_key:
            configured.append("shodan")
        if self.aws_region:
            configured.append("aws")
        if self.azure_client_id and self.azure_tenant_id:
            configured.append("azure")
        if self.gcp_service_account_file:
            configured.append("gcp")
        return configured


settings = Settings()
