from typing import List
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class FaissIndexer:
    def __init__(self, dimension: int):
        """
        Inicjalizuje obiekt klasy FaissIndexer.

        :param dimension: Wymiar wektora (np. 768 dla modelu 'paraphrase-MiniLM-L6-v2').
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # Używamy prostego indeksu na podstawie odległości L2.
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Wczytanie modelu do generowania embeddingów.

    def create_embedding(self, text: List[str]) -> np.ndarray:
        """
        Tworzy embeddingi dla listy tekstów przy użyciu modelu SentenceTransformer.

        :param text: Lista tekstów do zamiany na embeddingi.
        :return: Wektory embeddingów dla tekstów.
        """
        embeddings = self.model.encode(text)
        print("Generated embeddings:", embeddings)  # Wyświetla wygenerowane embeddingi
        return embeddings

    def add_vectors(self, embeddings: np.ndarray):
        """
        Generuje embeddingi z tekstów i dodaje je do indeksu FAISS.

        :param text: Lista tekstów do dodania.
        """
        self.index.add(embeddings)  # Dodajemy wygenerowane embeddingi do indeksu FAISS.

    def search(self, query: np.ndarray, k: int = 5):
        """
        Wyszukuje najbliższych sąsiadów dla zadanego zapytania.

        :param query: Wektor zapytania.
        :param k: Liczba najbliższych sąsiadów, które chcemy znaleźć.
        :return: K najbliższych wektorów i ich odległości.
        """
        distances, indices = self.index.search(query, k)
        return distances, indices

    def remove_vector(self, id: int):
        """
        Usuwa wektor z indeksu FAISS.

        :param id: Identyfikator wektora, który chcemy usunąć.
        """
        raise NotImplementedError("FAISS nie obsługuje bezpośrednio usuwania wektorów w IndexFlatL2.")

    def update_vector(self, id: int, new_vector: np.ndarray):
        """
        Aktualizuje wektor w indeksie FAISS (wymaga usunięcia i ponownego dodania).

        :param id: Identyfikator wektora, który chcemy zaktualizować.
        :param new_vector: Nowy wektor, który zastąpi stary.
        """
        self.remove_vector(id)
        self.add_vectors([new_vector])  # Ponowne dodanie nowego wektora.

