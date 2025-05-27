import os
from openai import AsyncOpenAI

openai_client = AsyncOpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))


async def generate_using_openai(context: str, user_prompt: str,  is_verbose: bool = False) -> str:
  full_prompt = (
    f"You are a helpful assistant. Use the context below to answer the question.\n\n"
    f"Context:\n{context}\n\n"
    f"Question: {user_prompt}"
  )

  if is_verbose:
    print(f"Full Prompt: {full_prompt}")

  response = await openai_client.chat.completions.create(
    model="gpt-4",
    messages=[
      {
        "role": "system",
        "content": (
          "You are an assistant that answers user questions based on diary entries retrieved using a vector search system. "
          "Only use the provided context to generate responses. Be concise, informative, and assume the user is reading diary content."
          "Answer in second person"
        )
      },
      {
        "role": "user",
        "content": full_prompt
      }
    ]
  )
  if is_verbose:
    print(f"Open AI Response: {response}")

  return response.choices[0].message.content.strip()
