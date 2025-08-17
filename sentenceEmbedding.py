from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
text = "Finzly builds modern banking platforms."
vector = model.encode(text)
print(vector[:10])  # print first 10 numbers
