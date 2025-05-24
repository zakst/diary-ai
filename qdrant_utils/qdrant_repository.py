import os
from uuid import uuid4

import openai
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

from types import InternalQdrantDiaryEntry
from types import EntryType

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "diaries")

client = AsyncQdrantClient(api_key=QDRANT_API_KEY, url=QDRANT_URL)


async def embed_text(text: str) -> list[float]:
  response = await openai.Embedding.acreate(
    input=text,
    model="text-embedding-ada-002"
  )
  return response['data'][0]['embedding']


async def store_diary_entry(diary_entry: InternalQdrantDiaryEntry) -> str:
  tags = diary_entry["tags"] if diary_entry["tags"] is not None else []

  vector = await embed_text(diary_entry["vectorContent"])
  entry_id = str(uuid4())

  payload = {
    "user_uuid": diary_entry["user_uuid"],
    "type": EntryType.TEXT,
    "source": diary_entry["source"],
    "content": diary_entry["content"],
    "mime_type": diary_entry["mime_type"],
    "tags": tags,
    "created_at": diary_entry["created_at"],
    "updated_at": diary_entry["updated_at"],
  }

  await client.upsert(
    collection_name=QDRANT_COLLECTION,
    points=[
      models.PointStruct(id=entry_id, vector=vector, payload=payload)
    ]
  )

  print(f"✅ Stored diary entry with id: {entry_id}")
  return entry_id
