import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def generate_using_gemini(context: str, user_prompt: str, is_verbose: bool = False) -> str:
  full_prompt = (
    f"Use the Context below to answer the Question to the best your ability.\n\n"
    f"Context:\n{context}\n\n"
    f"Question: {user_prompt}"
  )
  response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=full_prompt,
    config=types.GenerateContentConfig(
      temperature=0.1,
      system_instruction="Assume the user is reading diary content and the Context you are getting is from diary entries that where stored in a vector db",
    )
  )
  if is_verbose:
    print(f"Gemini Response: {response}")

  return response.text