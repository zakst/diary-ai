import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from vertexai.language_models import TextEmbeddingModel
import vertexai

load_dotenv()

GOOGLE_CLOUD_PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT_ID"]
PRODUCT_API = os.environ["PRODUCT_API"]
OPEN_AI_EMBEDDING_MODEL = os.getenv("OPEN_AI_EMBEDDING_MODEL", "text-embedding-ada-002")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

openAIClient = AsyncOpenAI(api_key=os.environ["OPEN_AI_API_KEY"])

async def embed_text(text: str) -> list[float]:
  if PRODUCT_API == "openai":
    response = await openAIClient.embeddings.create(
      input=text,
      model=OPEN_AI_EMBEDDING_MODEL
    )
    return response.data[0].embedding
  else:
    vertexai.init(project=GOOGLE_CLOUD_PROJECT_ID, location="us-central1")
    model = TextEmbeddingModel.from_pretrained(GEMINI_EMBEDDING_MODEL)
    embeddings = model.get_embeddings([text])
    return embeddings[0].values