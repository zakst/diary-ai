import os
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models

from diary_types import PayloadIndexes

load_dotenv()

QDRANT_API_KEY: str = os.environ["QDRANT_API_KEY"]
QDRANT_URL: str = os.environ["QDRANT_URL"]
QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "diaries")
TEXT_EMBEDDING_PRODUCT = os.environ["TEXT_EMBEDDING_PRODUCT"]

client: AsyncQdrantClient = AsyncQdrantClient(api_key=QDRANT_API_KEY, url=QDRANT_URL)

async def create_collection():
  if await client.collection_exists(QDRANT_COLLECTION):
    print(f"⚠️ Collection '{QDRANT_COLLECTION}' already exists. Moving on...")
  else:
    await client.create_collection(
      collection_name=QDRANT_COLLECTION,
      vectors_config=models.VectorParams(
        size = 1536 if TEXT_EMBEDDING_PRODUCT == "openai" else 768 if TEXT_EMBEDDING_PRODUCT == "ollama" else 768,
        distance=models.Distance.COSINE
      )
    )
    print(f"✅ Collection '{QDRANT_COLLECTION}' created successfully.")


async def create_payload_indexes():
  if not await does_collection_exist():
    print(f"❌ Collection '{QDRANT_COLLECTION}' does not exist. Cannot create indexes.")
    return

  payload_indexes: PayloadIndexes = {
    "user_uuid": models.PayloadSchemaType.KEYWORD,
    "type": models.PayloadSchemaType.KEYWORD,
    "source": models.PayloadSchemaType.KEYWORD,
    "content": models.PayloadSchemaType.KEYWORD,
    "mime_type": models.PayloadSchemaType.KEYWORD,
    "tags": models.PayloadSchemaType.KEYWORD,
    "created_at": models.PayloadSchemaType.INTEGER,
  }

  for field, schema in payload_indexes.items():
    try:
      await client.create_payload_index(
        collection_name=QDRANT_COLLECTION,
        field_name=field,
        field_schema=schema
      )
      print(f"✅ Indexed field '{field}' as {schema.value}")
    except Exception as e:
      print(f"⚠️ Failed to index field '{field}': {e}")

async def does_collection_exist() -> bool:
  if await client.collection_exists(QDRANT_COLLECTION):
    return True
  else:
    return False