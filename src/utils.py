# utils.py
# Shared paths and config used across the project.

import os
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file, if present

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
INDEX_DIR = "models/index"       # where the FAISS vector store is saved
REPORTS_DIR = "reports"

# Free, local embedding model - no API key needed, runs on your machine.
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Free Groq model. Groq hosts several open models (Llama, Gemma, etc.)
# at no cost with a generous rate limit - good fit for a student project.
GROQ_MODEL = "llama-3.1-8b-instant"


def ensure_dirs():
    for d in [RAW_DIR, PROCESSED_DIR, INDEX_DIR, REPORTS_DIR]:
        os.makedirs(d, exist_ok=True)
