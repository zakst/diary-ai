import ollama


async def generate_using_ollama(context: str, user_prompt: str, is_verbose: bool = False) -> str:
  full_prompt = (
    f"Use the Context below to answer the Question to the best of your ability.\n\n"
    f"Context:\n{context}\n\n"
    f"Question: {user_prompt}"
  )

  response = ollama.chat(
    model="llama3",
    messages=[
      {"role": "system",
       "content": "Assume the user is reading diary content and the Context you are getting is from diary entries that were stored in a vector db."},
      {"role": "user", "content": full_prompt}
    ]
  )

  if is_verbose:
    print(f"Ollama Response: {response['message']['content']}")

  return response["message"]["content"]
