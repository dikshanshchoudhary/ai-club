from dataclasses import dataclass
import json
import os
from typing import Protocol
from urllib.request import Request, urlopen


class LLMProvider(Protocol):
    name: str

    def complete(self, prompt: str, *, system: str | None = None) -> str: ...


@dataclass
class GeminiProvider:
    api_key: str
    model: str = "gemini-3.5-flash"
    name: str = "gemini"

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        text = f"{system}\n\n{prompt}" if system else prompt
        body = json.dumps({"contents": [{"parts": [{"text": text}]}]}).encode()
        request = Request(f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent", data=body, headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"}, method="POST")
        with urlopen(request, timeout=90) as response:
            payload = json.loads(response.read().decode())
        return payload["candidates"][0]["content"]["parts"][0]["text"]


@dataclass
class ProviderAbstraction:
    primary: LLMProvider | None = None
    fallbacks: tuple[LLMProvider, ...] = ()

    def complete(self, prompt: str, *, system: str | None = None) -> dict:
        providers = tuple(provider for provider in (self.primary, *self.fallbacks) if provider)
        if not providers:
            return {"status": "not_configured", "provider": None, "text": None}
        for provider in providers:
            try:
                return {"status": "completed", "provider": provider.name, "text": provider.complete(prompt, system=system)}
            except Exception as exc:
                last_error = str(exc)
        return {"status": "provider_error", "provider": None, "text": None, "error": last_error}


def complete(prompt: str, *, system: str | None = None, provider: ProviderAbstraction | None = None) -> dict:
    if provider is None:
        api_key = os.getenv("GEMINI_API_KEY")
        provider = ProviderAbstraction(primary=GeminiProvider(api_key, os.getenv("GEMINI_MODEL", "gemini-3.5-flash"))) if api_key else ProviderAbstraction()
    return provider.complete(prompt, system=system)
