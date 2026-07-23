from agents.chat_agent import AIChatAgent
from memory.retriever import InMemoryRetriever


def test_chat_retrieves_scan_context_before_answering():
    retriever = InMemoryRetriever()
    retriever.add({"finding": "SQL injection in login query", "severity": "high"})
    result = AIChatAgent(retriever).ask("Show SQL injection risks")
    assert result["retrieved_context"]
    assert result["answer"]["status"] == "not_configured"

