from utils.vector_store import VectorStore

class RetrievalAgent:
    def __init__(self):
        self.store = VectorStore(
            "memory/faiss_index/index.bin",
            "memory/metadata.pkl"
        )

    def run(self, query):
        return self.store.search(query, k=5)
