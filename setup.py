import os
import asyncio
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from import_data import process_and_store_data
from qdrant_utils import create_collection, create_payload_indexes

load_dotenv()

def check_required_env_vars() -> bool:
  required_vars = [
    "QDRANT_URL",
    "QDRANT_API_KEY",
    "QDRANT_COLLECTION",
    "OPEN_AI_API_KEY",
  ]

  missing_vars = [var for var in required_vars if not os.getenv(var)]

  if missing_vars:
    print("❌ Missing required environment variables:")
    for var in missing_vars:
      print(f" - {var}")
    return False
  else:
    print("✅ All required environment variables are set.")
    return True

async def validate_qdrant_credentials() -> bool:
  qdrant_url = os.getenv("QDRANT_URL")
  qdrant_api_key = os.getenv("QDRANT_API_KEY")

  client = AsyncQdrantClient(url=qdrant_url, api_key=qdrant_api_key)

  try:
    await client.get_collections()
    print("✅ Successfully connected to Qdrant.")
    return True
  except UnexpectedResponse as e:
    print(f"❌ Failed to connect to Qdrant: {e}")
    return False
  except Exception as e:
    print(f"❌ Unexpected error while connecting to Qdrant: {e}")
    return False

async def main():
  await create_collection()
  await create_payload_indexes()
  await process_and_store_data("diary_samples")
  return None

if __name__ == "__main__":
  if check_required_env_vars():
    if asyncio.run(validate_qdrant_credentials()):
      asyncio.run(main())
      print("✅ Completed importing samples.")
