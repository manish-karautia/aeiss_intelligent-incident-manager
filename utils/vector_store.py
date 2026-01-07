import faiss
import pickle
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

class VectorStore:
    def __init__(self, index_path, metadata_path):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query, k=5):
        vector = self.model.encode([query])
        _, indices = self.index.search(vector, k)
        return [self.metadata[i] for i in indices[0]]
