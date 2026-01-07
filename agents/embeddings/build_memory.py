import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os

os.makedirs("memory/faiss_index", exist_ok=True)

df = pd.read_csv("data/incident_logs.csv")

texts = (
    df["service"] + " " +
    df["region"] + " " +
    df["metric_type"] + " " +
    df["description"] + " " +
    df["action_taken"]
).tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "memory/faiss_index/index.bin")

with open("memory/metadata.pkl", "wb") as f:
    pickle.dump(df.to_dict("records"), f)

with open("memory/success_stats.json", "w") as f:
    f.write("{}")

print("Memory built successfully.")
