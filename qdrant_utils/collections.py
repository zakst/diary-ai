import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

from types import PayloadIndexes

load_dotenv()

QDRANT_API_KEY: str = os.environ["QDRANT_API_KEY"]
QDRANT_URL: str = os.environ["QDRANT_URL"]
QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "diaries")

client: QdrantClient = QdrantClient(api_key=QDRANT_API_KEY, url=QDRANT_URL)

def create_collection():
  if client.collection_exists(QDRANT_COLLECTION):
    print(f"⚠️ Collection '{QDRANT_COLLECTION}' already exists. Moving on...")
  else:
    client.create_collection(
      collection_name=QDRANT_COLLECTION,
      vectors_config=models.VectorParams(
        size=1536,
        distance=models.Distance.COSINE
      )
    )
    print(f"✅ Collection '{QDRANT_COLLECTION}' created successfully.")

def create_payload_indexes():
  if client.collection_exists(QDRANT_COLLECTION):
    print(f"⚠️ Collection '{QDRANT_COLLECTION}' already exists. Indexing should have been created.")
  else:
    payload_indexes: PayloadIndexes = {
      "user_uuid": models.PayloadSchemaType.KEYWORD,
      "type": models.PayloadSchemaType.KEYWORD, # default: text
      "source": models.PayloadSchemaType.KEYWORD, # local_import
      "content": models.PayloadSchemaType.KEYWORD, # summary of the diary entry
      "mime_type": models.PayloadSchemaType.KEYWORD,
      "tags": models.PayloadSchemaType.KEYWORD,
      "created_at": models.PayloadSchemaType.INTEGER,
    }

    for field, schema in payload_indexes.items():
      try:
        client.create_payload_index(
          collection_name=QDRANT_COLLECTION,
          field_name=field,
          field_schema=schema
        )
        print(f"✅ Indexed field '{field}' as {schema.value}")
      except Exception as e:
        print(f"⚠️ Failed to index field '{field}': {e}")