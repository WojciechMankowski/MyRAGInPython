import faiss

# Ścieżka do indeksu
index = faiss.read_index("data/faiss_index.idx")

# Liczba wektorów w bazie
print(f"Liczba dokumentów w bazie: {index.ntotal}")
