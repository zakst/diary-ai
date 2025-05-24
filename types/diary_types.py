from enum import Enum
from typing import TypedDict, List

class EntryType(str, Enum):
    TEXT = "text"

class EntrySource(str, Enum):
    LOCAL_IMPORT = "local_import"

class DiaryEntry(TypedDict):
    user_uuid: str
    type: EntryType
    source: EntrySource
    content: str
    mime_type: str
    tags: List[str]
    created_at: int
    updated_at: int

class InternalQdrantDiaryEntry(DiaryEntry):
    id: str
    vectorContent: str
