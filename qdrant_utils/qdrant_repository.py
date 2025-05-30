import os
from uuid import uuid4

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

from diary_types import InternalQdrantDiaryEntry
from diary_types import EntryType
from qdrant_client.models import Filter, FieldCondition, MatchValue

from embeddings import embed_text

load_dotenv()

QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "diaries")

client = AsyncQdrantClient(api_key=QDRANT_API_KEY, url=QDRANT_URL)

async def diary_entry_exists_by_content(content: str) -> bool:
  response = await client.scroll(
    collection_name=QDRANT_COLLECTION,
    limit=1,
    with_payload=False,
    scroll_filter=Filter(
      must=[
        FieldCondition(
          key="content",
          match=MatchValue(value=content)
        )
      ]
    )
  )
  return len(response[0]) > 0


def sanitize_text(text: str) -> str:
  return (
    text.replace("’", "'")
    .replace("‘", "'")
    .replace("“", '"')
    .replace("”", '"')
  )

async def store_diary_entry(diary_entry: InternalQdrantDiaryEntry) -> str:
  if await diary_entry_exists_by_content(diary_entry["content"]):
    print(f"⏩ Entry already exists: {diary_entry['content']}")
    return "done"
  else:
    tags = diary_entry["tags"] if diary_entry["tags"] is not None else []
    vector = await embed_text(diary_entry["vectorContent"])
    entry_id = str(uuid4())

    payload = {
      "user_uuid": diary_entry["user_uuid"],
      "type": EntryType.TEXT,
      "source": diary_entry["source"],
      "content": diary_entry["content"],
      "diary_entry": sanitize_text(diary_entry["vectorContent"]),
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
    return entry_id
