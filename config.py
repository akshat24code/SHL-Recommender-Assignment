import os
from dotenv import load_dotenv

load_dotenv()

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

CATALOG_PATH = "catalog/catalog.json"

INDEX_PATH = "vector_store/index.faiss"

METADATA_PATH = "vector_store/metadata.json"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

#LLM_MODEL = "gemini-2.0-flash"
LLM_MODEL = "openai/gpt-3.5-turbo"