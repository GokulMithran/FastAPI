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

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_gemini(request: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(request.prompt)

        # Extract response text
        answer = response.text.strip() if response and hasattr(response, "text") else "No response"

        # Extract token usage metadata (if available)
        usage = getattr(response, "usage_metadata", None)
        if usage:
            token_info = {
                "prompt_tokens": usage.prompt_token_count,
                "completion_tokens": usage.candidates_token_count,
                "total_tokens": usage.total_token_count
            }
               # Pricing for Gemini 1.5 Flash
            input_price = 0.35 / 1_000_000   # per token
            output_price = 0.70 / 1_000_000  # per token

            estimated_cost = (token_info.get("prompt_tokens", 0) * input_price) + (token_info.get("completion_tokens", 0) * output_price)
            cost = round(estimated_cost, 6)  # keep 6 decimal places
        else:
            token_info = None

        return {
            "response": answer,
            "usage": token_info,
            "cost": cost
        }
    except Exception as e:
        return {"error": str(e)}
