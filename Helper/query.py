from langchain_ollama import OllamaLLM

def generate_answer_from_context(query: str, context: str) -> {str: str}:
    llm = OllamaLLM(model="gemma3")
    return {"answer": llm.invoke(f"Na podstawie poniższego tekstu odpowiedz na pytanie: {query}\n\n{context}")}