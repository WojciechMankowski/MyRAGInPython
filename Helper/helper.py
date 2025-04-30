import faiss

from faiss_indexer import FaissIndexer
import numpy as np

def create_faiss_index(indexer: FaissIndexer, embeddings: np.ndarray):

    # Dodajemy wektory (embeddingi) do indeksu
    indexer.index.add(embeddings)
    print(f"Index created with {embeddings.shape[0]} vectors of dimension {embeddings.shape[1]}.")

def search_faiss_index(indexer: FaissIndexer, query_embedding: np.ndarray, k: int = 5):
    distances, indices = indexer.index.search(query_embedding, k)
    return distances, indices


def update_faiss_vector(indexer: FaissIndexer, old_index: int, new_embedding: np.ndarray):
    """
    Aktualizuje wektor w indeksie FAISS. (Operacja usunięcia i ponownego dodania wektora).

    :param indexer: Instancja klasy FaissIndexer.
    :param old_index: Indeks wektora, który ma zostać zaktualizowany.
    :param new_embedding: Nowy wektor (embedding), który zastąpi stary.
    """
    # FAISS nie obsługuje bezpośredniej aktualizacji, więc usuwamy i dodajemy wektor
    print(f"Updating vector at index {old_index}...")

    # Usuwanie wektora
    remove_faiss_vector(indexer, old_index)

    # Dodanie nowego wektora
    indexer.index.add(new_embedding.reshape(1, -1))  # Dodajemy pojedynczy wektor
    print(f"Vector at index {old_index} updated.")


def remove_faiss_vector(indexer: FaissIndexer, index_to_remove: int):
    print(f"Removing vector at index {index_to_remove}...")

    # Tworzymy nowy indeks, usuwając wektor
    new_index = faiss.IndexFlatL2(indexer.dimension)
    new_index.add(
        indexer.index.reconstruct_n(0, indexer.index.ntotal))  # Dodajemy tylko pozostałe wektory (bez usuniętego)

    # Zamieniamy starą instancję indeksu na nową
    indexer.index = new_index
    print(f"Vector at index {index_to_remove} removed.")






