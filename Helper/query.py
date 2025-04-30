from langchain_ollama import OllamaLLM

def generate_answer_from_context(query: str, context: str) -> dict[str, str]:
    print("Uruchomienie modelu AI")

    # Parametry modelu – możesz je dostosować wedle uznania
    llm = OllamaLLM(
        model="llama3",
        temperature=0.7,       # więcej kreatywności
        num_predict=800        # zwiększ długość odpowiedzi (w tokenach)
    )

    prompt = f"""
Odpowiedz szczegółowo na poniższe pytanie, bazując wyłącznie na dostarczonym kontekście.
Odpowiedź sformatuj w języku Markdown (używaj nagłówków, list, pogrubień, itp.).
Staraj się, by odpowiedź była wyczerpująca, logicznie uporządkowana i miała co najmniej kilka akapitów. Jeśli czegoś nie
nie wiesz to nie wymyślaj. Możesz zaproponować dodatkowe pytania.

### Pytanie:
{query}

### Kontekst:
{context}
""".strip()

    return {"answer": llm.invoke(prompt)}
