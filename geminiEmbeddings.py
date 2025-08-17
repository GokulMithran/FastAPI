from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load .env variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Configure Gemini client
genai.configure(api_key=API_KEY)

# Create embedding
embedding = genai.embed_content(
    model="models/embedding-001",   # correct model path
    content="Artificial Intelligence is transforming industries."
)

# The embedding is directly under ['embedding']
vector = embedding["embedding"]

print(len(vector))      # vector length (default 3072)
print(vector[:5])       # first 5 values
