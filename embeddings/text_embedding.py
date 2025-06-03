import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from sentence_transformers import SentenceTransformer
from vertexai.language_models import TextEmbeddingModel
import vertexai

load_dotenv()

GOOGLE_CLOUD_PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT_ID"]
TEXT_EMBEDDING_PRODUCT = os.environ["TEXT_EMBEDDING_PRODUCT"]
OPEN_AI_EMBEDDING_MODEL = os.getenv("OPEN_AI_EMBEDDING_MODEL", "text-embedding-ada-002")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "all-mpnet-base-v2")

openAIClient = AsyncOpenAI(api_key=os.environ["OPEN_AI_API_KEY"])

async def embed_text(text: str) -> list[float]:
  if TEXT_EMBEDDING_PRODUCT == "openai":
    response = await openAIClient.embeddings.create(
      input=text,
      model=OPEN_AI_EMBEDDING_MODEL
    )
    return response.data[0].embedding
  elif TEXT_EMBEDDING_PRODUCT == "ollama":
    response = await SentenceTransformer(OLLAMA_EMBEDDING_MODEL)
    return response.encode(text).tolist()
  else:
    vertexai.init(project=GOOGLE_CLOUD_PROJECT_ID, location="us-central1")
    model = TextEmbeddingModel.from_pretrained(GEMINI_EMBEDDING_MODEL)
    embeddings = model.get_embeddings([text])
    return embeddings[0].values