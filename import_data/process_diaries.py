import asyncio
import os
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4
import time

import aiofiles
from openai import RateLimitError, OpenAIError

from diary_types import InternalQdrantDiaryEntry, EntryType, EntrySource
from qdrant_utils import store_diary_entry, does_collection_exist

semaphore = asyncio.Semaphore(32)

MAX_RETRIES = 5
INITIAL_BACKOFF = 2.0
BACKOFF_FACTOR = 3.0


async def store_with_retry(diary_entry: InternalQdrantDiaryEntry) -> Optional[str]:
  backoff = INITIAL_BACKOFF
  for attempt in range(1, MAX_RETRIES + 1):
    try:
      entry_id = await store_diary_entry(diary_entry)
      return entry_id
    except RateLimitError:
      print(f"⚠️ Rate limit hit on attempt {attempt + 1}, retrying in {backoff}s...")
      await asyncio.sleep(backoff)
      backoff *= 2
    except OpenAIError as e:
      print(f"❌ OpenAI error: {e}")
      return None
    except Exception as e:
      print(f"❌ Unexpected error: {e}")
      return None
  return None

async def process_and_store_entry(
    txt_file: Path,
    user_uuid: str,
    tags: list[str],
    folder_name: str
) -> Optional[str]:
  async with semaphore:
    try:
      async with aiofiles.open(txt_file, "r", encoding="utf-8") as f:
        content = await f.read()
        date_time_from_filename = basename = os.path.splitext(txt_file.name  )[0]
        content_with_datetime = f"{content}\n{date_time_from_filename}"

      diary_entry: InternalQdrantDiaryEntry = {
        "id": str(uuid4()),
        "vectorContent": content_with_datetime,
        "user_uuid": user_uuid,
        "type": EntryType.TEXT,
        "source": EntrySource.LOCAL_IMPORT,
        "content": f"{folder_name}/{txt_file.name}",
        "mime_type": "text/plain",
        "tags": tags,
        "created_at": int(time.time()),
        "updated_at": int(time.time()),
      }

      entry_id = await store_with_retry(diary_entry)
      if entry_id:
        if entry_id != "done":
          print(f"✅ Processed {folder_name} entry for {txt_file.name} with id {entry_id}")
      else:
        print(f"⚠️ Failed to store entry for {txt_file.name} after retries.")
      return entry_id

    except Exception as e:
      print(f"⚠️ Failed to process {txt_file}: {e}")
      return None


async def process_and_store_data(data_dir: str) -> Optional[list[Any]]:
  if not await does_collection_exist():
    print("❌ You must create a collection first.")
    return None
  else:
    base_path = Path(data_dir)
    if not base_path.exists() or not base_path.is_dir():
      print(f"❌ Provided path {data_dir} does not exist or is not a directory.")
      return None

    tasks = []

    for diary_samples_folder in base_path.iterdir():
      if not diary_samples_folder.is_dir():
        continue

      user_uuid = str(uuid4())
      tags = [diary_samples_folder.name]

      for txt_file in diary_samples_folder.glob("*.txt"):
        tasks.append(process_and_store_entry(txt_file, user_uuid, tags, diary_samples_folder.name))

    return await asyncio.gather(*tasks)
