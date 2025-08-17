from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

import os

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = OpenAI(api_key=API_KEY)


class PromptRequest(BaseModel):
    prompt: str


@app.post("/ask")
async def ask_gpt(request: PromptRequest):
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request.prompt}
        ]
    )
    return {"response": response.choices[0].message.content}
