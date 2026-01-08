from utils.vector_store import VectorStore
class RetrievalAgent:
    def __init__(self):
        self.store = VectorStore(
            "memory/faiss_index/index.bin",
            "memory/metadata.pkl"
        )

    def run(self, query):
        if isinstance(query, dict):
            query = " ".join(str(v) for v in query.values())
        return self.store.search(query, k=5)
