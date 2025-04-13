
import os

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from embeding import create_embeding

from faiss_indexer import FaissIndexer
from query import generate_answer_from_context


def load_markdown(file: str):
    loader = UnstructuredMarkdownLoader(file)
    docs = loader.load()
    return docs  # docs to teraz lista dokumentów


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    all_chunks = []
    for doc in documents:
        chunks = text_splitter.split_documents([doc])  # Przechodzimy przez każdy dokument
        all_chunks.extend(chunks)  # Dodajemy je do listy
    return all_chunks


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