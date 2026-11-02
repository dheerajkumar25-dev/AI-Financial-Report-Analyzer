
# utils.py
# Shared paths and config used across the project.

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Project root directory
ROOT_DIR = Path(__file__).resolve().parents[1]

# Load local .env file
load_dotenv(ROOT_DIR / ".env")


def get_setting(name: str, default: str = "") -> str:
    """Read configuration from local environment or Streamlit Cloud Secrets."""

    # First check environment variables and local .env
    value = os.getenv(name, "").strip()

    if value:
        return value

    # Then check Streamlit Cloud Secrets
    try:
        return str(st.secrets.get(name, default)).strip()
    except Exception:
        return default


# Groq API configuration
GROQ_API_KEY = get_setting("GROQ_API_KEY")
GROQ_MODEL = get_setting("GROQ_MODEL", "openai/gpt-oss-20b")

# Project directories
RAW_DIR = str(ROOT_DIR / "data" / "raw")
PROCESSED_DIR = str(ROOT_DIR / "data" / "processed")
INDEX_DIR = str(ROOT_DIR / "models" / "index")
REPORTS_DIR = str(ROOT_DIR / "reports")

# Free local embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def ensure_dirs():
    """Create required project directories if they do not exist."""

    for directory in [RAW_DIR, PROCESSED_DIR, INDEX_DIR, REPORTS_DIR]:
        os.makedirs(directory, exist_ok=True)
