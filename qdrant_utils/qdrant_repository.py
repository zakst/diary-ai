import os
from uuid import uuid4

import openai
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import time
from types import DiaryEntry
from types import EntryType

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "diaries")

client = QdrantClient(api_key=QDRANT_API_KEY, url=QDRANT_URL)


def embed_text(text: str) -> list[float]:
  response = openai.Embedding.create(
    input=text,
    model="text-embedding-ada-002"
  )
  return response['data'][0]['embedding']


def store_diary_entry(diary_entry: DiaryEntry) -> str:
  if diary_entry["tags"] is None:
    tags = []
  else:
    tags = diary_entry["tags"]

  vector = embed_text(diary_entry["content"])

  entry_id = str(uuid4())

  payload = {
    "user_uuid": diary_entry["user_uuid"],
    "type": EntryType.TEXT,
    "source": diary_entry["source"],
    "content": diary_entry["content"],
    "mime_type": diary_entry["mime_type"],
    "tags": tags,
    "created_at": int(time.time()),
    "updated_at": int(time.time()),
  }

  client.upsert(
    collection_name=QDRANT_COLLECTION,
    points=[
      models.PointStruct(id=entry_id, vector=vector, payload=payload)
    ]
  )

  print(f"✅ Stored diary entry with id: {entry_id}")
  return entry_id
