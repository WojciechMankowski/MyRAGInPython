import json
import os
import faiss
from fastapi import FastAPI
from Helper.load_data import load_markdown
from Helper.split import split_documents
from embeding import create_embeding
from faiss_indexer import FaissIndexer
from Helper.query import generate_answer_from_context
from Helper.Answer import Question, Answer


app = FastAPI()

DATA_DIR = "data"
FAISS_INDEX_PATH = f"{DATA_DIR}/faiss_index.idx"
METADATA_PATH = f"{DATA_DIR}/data.json"

# Endpoint: wszystkie notatki
@app.get("/")
def home():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r') as file:
            files = json.load(file)
        return files
    return {"message": "Brak danych."}

# Endpoint: tworzenie bazy
@app.get("/create")
def create_database():
    os.makedirs(DATA_DIR, exist_ok=True)

    files = [f"{DATA_DIR}/{file}" for file in os.listdir(DATA_DIR) if file.endswith('.md')]
    documents = []
    for file in files:
        documents.extend(load_markdown(file))
    chunks = split_documents(documents)

    texts = [chunk.page_content for chunk in chunks]
    embeddings = create_embeding(texts)

    indexer = FaissIndexer(dimension=embeddings.shape[1])
    indexer.add_vectors(embeddings)
    indexer.save_index(FAISS_INDEX_PATH)

    metadata = [
        {
            "id": i,
            "text": chunk.page_content,
            "source": chunk.metadata.get("source", "unknown")
        }
        for i, chunk in enumerate(chunks)
    ]
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return {"status": "success", "chunks": len(chunks)}

# Endpoint: zadawanie pytania
@app.get("/ask/{question}")
def get_ask(question: str):
    if not os.path.exists(FAISS_INDEX_PATH):
        return {"error": "Baza danych nie została jeszcze utworzona. Najpierw wywołaj /create"}

    indexer = FaissIndexer(dimension=768, index_path=FAISS_INDEX_PATH)  # Użyj prawidłowego wymiaru
    query_embedding =indexer.create_embedding([question])
    distances, indices = indexer.search(query_embedding, k=2)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    top_chunks = [metadata[i] for i in indices[0] if i < len(metadata)]

    context = "\n".join([chunk["text"] for chunk in top_chunks])
    answer = generate_answer_from_context(question, context)

    print(answer)



    return {
        "question": question,
        'answer': answer['answer'],
        "sources": list(set(chunk["source"] for chunk in top_chunks))
    }

def main():
    path = 'data'
    files = [f'{path}/{file}' for file in list(os.listdir(path)) if file.endswith('.md')]

    documents = []
    for file in files:
        documents.extend(load_markdown(file))  # Rozwijamy listę dokumentów
    chunks = split_documents(documents)

    # Generowanie embeddingów
    embeddings = create_embeding([chunk.page_content for chunk in chunks])
    # Używamy page_content w każdym dokumencie
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