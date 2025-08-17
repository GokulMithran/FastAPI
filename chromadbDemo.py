import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()

collection = client.create_collection("docs")

# Add documents to the collection
docs = [
    "Finzly is a fintech company that builds modern banking platforms.",
    "LangChain is a framework for building applications with LLMs.",
    "Python is a popular programming language for AI and ML."
]

embeddings = [model.encode(doc).tolist() for doc in docs]


collection.add(
    documents=docs,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(docs))]
)

# Query
query = "What is Finzly?"
results = collection.query(
    query_embeddings=[model.encode(query).tolist()],
    n_results=2
)
print(results)