from typing import List, Optional
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os


class FaissIndexer:
    def __init__(self, dimension: int, index_path: Optional[str] = None):
        """
        Inicjalizuje obiekt FaissIndexer.
        Jeśli index_path jest podany i plik istnieje, załaduj indeks z dysku.
        W przeciwnym razie utwórz nowy pusty indeks FAISS.

        :param dimension: Wymiar embeddingów (np. 768).
        :param index_path: Ścieżka do pliku indeksu FAISS (jeśli istnieje).
        """
        self.dimension = dimension
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        if index_path and os.path.exists(index_path):
            print(f"🔁 Wczytywanie istniejącego indeksu z {index_path}")
            self.index = faiss.read_index(index_path)
        else:
            print(f"🆕 Tworzenie nowego indeksu FAISS (dim={dimension})")
            self.index = faiss.IndexFlatL2(dimension)

    def create_embedding(self, texts: List[str]) -> np.ndarray:
        """
        Tworzy embeddingi z listy tekstów.

        :param texts: Lista tekstów.
        :return: Tablica numpy z embeddingami (float32).
        """
        embeddings = self.model.encode(texts)
        return embeddings.astype("float32")

    def add_vectors(self, embeddings: np.ndarray):
        """
        Dodaje wektory do indeksu FAISS.

        :param embeddings: Tablica wektorów (float32).
        """
        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, k: int = 5):
        """
        Wyszukuje najbliższe wektory do zapytania.

        :param query_embedding: Wektor zapytania (1 x dim).
        :param k: Ilość najbliższych sąsiadów.
        :return: (dystanse, indeksy)
        """
        return self.index.search(query_embedding, k)

    def save_index(self, path: str):
        """
        Zapisuje indeks FAISS na dysk.

        :param path: Ścieżka do pliku.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        faiss.write_index(self.index, path)
        print(f"✅ Zapisano indeks FAISS do: {path}")

    def load_index(self, path: str):
        """
        Wczytuje indeks FAISS z dysku.

        :param path: Ścieżka do pliku.
        """
        if os.path.exists(path):
            self.index = faiss.read_index(path)
            print(f"📥 Indeks wczytany z: {path}")
        else:
            raise FileNotFoundError(f"❌ Nie znaleziono pliku indeksu: {path}")
