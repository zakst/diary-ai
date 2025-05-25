from typing import TypedDict
from qdrant_client.http.models import PayloadSchemaType

class PayloadIndexes(TypedDict):
    user_uuid: PayloadSchemaType
    type: PayloadSchemaType
    source: PayloadSchemaType
    content: PayloadSchemaType
    mime_type: PayloadSchemaType
    tags: PayloadSchemaType
    created_at: PayloadSchemaType
