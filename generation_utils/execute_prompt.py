import os
from typing import List
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, SearchParams

from embeddings import embed_text
from generation_utils.gemini_generation import generate_using_gemini
from generation_utils.ollama_generation import generate_using_ollama
from generation_utils.open_ai_generation import generate_using_openai

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
GENERATION_LLM = os.getenv("GENERATION_LLM")

qdrant_client = AsyncQdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

async def process_prompt(user_prompt: str, selected_user: str, is_verbose: bool = False) -> str | None:
  query_vector = await embed_text(user_prompt)
  if is_verbose:
    print(f"Query Vector: {query_vector}")
  search_result = await qdrant_client.search(
    collection_name=QDRANT_COLLECTION,
    query_vector=query_vector,
    limit=10,
    search_params=SearchParams(hnsw_ef=128, exact=True),
    with_payload=True,
    query_filter=Filter(
      must=[
        FieldCondition(
          key="tags",
          match=MatchValue(value=selected_user)
        )
      ]
    )
  )
  if is_verbose:
    print(f"Vector Search Result: {search_result}")

  context_docs: List[str] = [
    item.payload.get("diary_entry", "") for item in search_result if item.payload
  ]
  context = "\n\n".join(context_docs)

  if is_verbose:
    print(f"Vector Search Context: {context}")

  if GENERATION_LLM == "openai":
    openai_response = await generate_using_openai(context, user_prompt, is_verbose)
    return openai_response
  elif GENERATION_LLM == "gemini":
    gemini_response = await generate_using_gemini(context, user_prompt, is_verbose)
    return gemini_response
  elif GENERATION_LLM == "ollama":
    ollama_response = await generate_using_ollama(context, user_prompt, is_verbose)
    return ollama_response
  return None
