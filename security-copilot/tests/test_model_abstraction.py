from models.llm import GeminiProvider, ProviderAbstraction
from models.embeddings import EmbeddingAbstraction


class FakeProvider:
    name = "fake"

    def complete(self, prompt, *, system=None):
        return f"answer:{prompt}"


def test_llm_provider_abstraction_uses_primary():
    result = ProviderAbstraction(primary=FakeProvider()).complete("hello")
    assert result == {"status": "completed", "provider": "fake", "text": "answer:hello"}


def test_embedding_abstraction_is_safe_when_unconfigured():
    result = EmbeddingAbstraction().embed("hello")
    assert result["model"] == "text-embedding-3-large"
    assert result["status"] == "not_configured"


def test_gemini_provider_uses_configured_model():
    provider = GeminiProvider("not-a-real-key", "gemini-test")
    assert provider.name == "gemini"
    assert provider.model == "gemini-test"
