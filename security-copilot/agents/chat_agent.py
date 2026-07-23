from dataclasses import dataclass

from memory.retriever import InMemoryRetriever
from models.llm import ProviderAbstraction


@dataclass
class AIChatAgent:
    retriever: InMemoryRetriever
    provider: ProviderAbstraction | None = None

    def ask(self, question: str) -> dict:
        context = self.retriever.search(question)
        prompt = "Answer using only the retrieved security context. If evidence is missing, say so.\n\nQuestion: " + question + "\n\nContext: " + str(context)
        answer = (self.provider or ProviderAbstraction()).complete(prompt)
        return {"question": question, "retrieved_context": context, "answer": answer, "status": "completed"}

