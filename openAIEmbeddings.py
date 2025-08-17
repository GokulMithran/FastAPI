from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
import os

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input="Artificial Intelligence is transforming industries."
)

print(len(embedding.data[0].embedding))  # vector length
print(embedding.data[0].embedding[:5])   # first 5 values
