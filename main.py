import os
from Helper.load_data import load_markdown, save_metadata
from embeding import create_embeding
from faiss_indexer import FaissIndexer
from Helper.query import generate_answer_from_context
from Helper.split import split_documents
from fastapi import FastAPI, Request

app = FastAPI()
# wszystkie notatki
@app.get('/')
def home():
    return "API"

# tworzenie embedingu i bazy
@app.get("/create")
def create_database():
    path = 'data'
    files = [f'{path}/{file}' for file in os.listdir(path) if file.endswith('.md')]

    documents = []
    for file in files:
        documents.extend(load_markdown(file))  # Rozwijamy listę dokumentów

    chunks = split_documents(documents)

    # 🧠 Tworzymy metadane do zapisania
    metadata = []
    for idx, chunk in enumerate(chunks):
        metadata.append({
            "id": idx,
            "source": chunk.metadata.get("source", "unknown"),
            "text": chunk.page_content
        })

    # 🔤 Generujemy embeddingi
    embeddings = create_embeding([chunk.page_content for chunk in chunks])

    # 🧠 Tworzymy FAISS index
    indexer = FaissIndexer(dimension=embeddings.shape[1])
    indexer.add_vectors(embeddings)

    # 💾 Zapis metadanych do JSON-a
    save_metadata(metadata)

    return {"status": "success", "chunks": len(chunks)}


# aktualizacja bazy
# zadawanie pytań

def main():
    path = 'data'
    files = [f'{path}/{file}' for file in list(os.listdir(path)) if file.endswith('.md')]

    documents = []
    for file in files:
        documents.extend(load_markdown(file))  # Rozwijamy listę dokumentów
    chunks = split_documents(documents)

    # Generowanie embeddingów
    embeddings = create_embeding([chunk.page_content for chunk in chunks])  # Używamy page_content w każdym dokumencie
    # print(embeddings.shape[1])
    # Tworzymy instancję FaissIndexer
    indexer = FaissIndexer(dimension=embeddings.shape[1])
    indexer.add_vectors(embeddings)  # Dodajemy wektory do FAISS

    # Wyszukiwanie podobnych dokumentów
    query_embedding = indexer.create_embedding(
        ["W jaki sposób emocje wpływają na nasze decyzje i interakcje społeczne?"])
    distances, indices = indexer.search(query_embedding, k=2)

    closest_chunks = [chunks[i] for i in indices[0]]
    context = "\n".join([chunk.page_content for chunk in closest_chunks])
    query = "W jaki sposób emocje wpływają na nasze decyzje i interakcje społeczne?"
    # Generowanie odpowiedzi na podstawie zapytania i kontekstu
    answer = generate_answer_from_context(query, context)

    print(answer)



if __name__ == '__main__':
    main()