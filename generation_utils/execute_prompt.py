import os
from typing import List
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, SearchParams
from qdrant_utils.qdrant_repository import embed_text

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

qdrant_client = AsyncQdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def process_prompt(user_prompt: str, selected_user: str) -> str:
    query_vector = await embed_text(user_prompt)

    search_result = await qdrant_client.search(
      collection_name=QDRANT_COLLECTION,
      query_vector=query_vector,
      limit=5,
      search_params=SearchParams(hnsw_ef=128),
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

    context_docs: List[str] = [
        item.payload.get("content", "") for item in search_result if item.payload
    ]
    context = "\n\n".join(context_docs)

    full_prompt = (
        f"You are a helpful assistant. Use the context below to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {user_prompt}"
    )

    response = await openai_client.chat.completions.create(
      model="gpt-4",
      messages=[
        ChatCompletionMessageParam(
          role="system",
          content=(
            "You are an assistant that answers user questions based on diary entries retrieved using a vector search system. "
            "Only use the provided context to generate responses. Be concise, informative, and assume the user is reading diary content."
          )
        ),
        ChatCompletionMessageParam(
          role="user",
          content=full_prompt
        )
      ]

    )

    return response.choices[0].message.content.strip()
