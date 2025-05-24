import os
import asyncio
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Filter

load_dotenv()

QDRANT_API_KEY: str = os.environ["QDRANT_API_KEY"]
QDRANT_URL: str = os.environ["QDRANT_URL"]
QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "diaries")

client: AsyncQdrantClient = AsyncQdrantClient(api_key=QDRANT_API_KEY, url=QDRANT_URL)

async def delete_all_points():
  if not await client.collection_exists(QDRANT_COLLECTION):
    print(f"❌ Collection '{QDRANT_COLLECTION}' does not exist.")
    return

  try:
    response = await client.delete(
      collection_name=QDRANT_COLLECTION,
      points_selector=Filter(must=[])
    )
    print(f"🗑️ Deleted all points from '{QDRANT_COLLECTION}'. Result: {response}")
  except Exception as e:
    print(f"⚠️ Failed to delete points from '{QDRANT_COLLECTION}': {e}")

if __name__ == "__main__":
  asyncio.run(delete_all_points())
