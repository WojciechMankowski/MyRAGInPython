from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np


def create_embeding(text: List[str]) -> np.ndarray:
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(text)
    # print(embeddings.shape)
    return embeddings