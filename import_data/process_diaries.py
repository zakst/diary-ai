import time
import asyncio
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import aiofiles

from types import InternalQdrantDiaryEntry, EntryType, EntrySource
from qdrant_utils import store_diary_entry


async def process_and_store_entry(txt_file: Path, user_uuid: str, tags: list[str], folder_name: str) -> Optional[str]:
  try:
    async with aiofiles.open(txt_file, "r", encoding="utf-8") as f:
      content = await f.read()

    diary_entry: InternalQdrantDiaryEntry = {
      "id": str(uuid4()),
      "vectorContent": content,
      "user_uuid": user_uuid,
      "type": EntryType.TEXT,
      "source": EntrySource.LOCAL_IMPORT,
      "content": f"{folder_name}/{txt_file.name}",
      "mime_type": "text/plain",
      "tags": tags,
      "created_at": int(time.time()),
      "updated_at": int(time.time()),
    }

    entry_id = await store_diary_entry(diary_entry)
    print(f"✅ Processed {folder_name} entry for {txt_file.name} with id {entry_id}")
    return entry_id

  except Exception as e:
    print(f"⚠️ Failed to process {txt_file}: {e}")
    return None


async def process_and_store_data(data_dir: str) -> Optional[list[Any]]:
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
      tasks.append(
        process_and_store_entry(txt_file, user_uuid, tags, diary_samples_folder.name)
      )

  return await asyncio.gather(*tasks)
