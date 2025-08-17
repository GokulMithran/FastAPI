from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
import os

# Load embedding model (local, free)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Chroma client & collection
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("finzly_docs")

# Read file & preprocess
def load_and_store_file(file_path="sample_doc.txt"):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into chunks (200–300 words approx.)
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    embeddings = [model.encode(chunk).tolist() for chunk in chunks]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(chunks))]
    )

# Load file at startup
load_and_store_file()

# FastAPI app
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 2

@app.post("/search")
async def search_docs(request: QueryRequest):
    query_embedding = model.encode(request.query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=request.top_k
    )
    return {"query": request.query, "results": results}
