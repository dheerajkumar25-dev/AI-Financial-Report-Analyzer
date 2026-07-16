# embeddings.py
# Turns text chunks into vectors (embeddings) and stores them in a FAISS
# index for fast similarity search. This is the "retrieval" half of RAG
# (Retrieval-Augmented Generation).
#
# Why HuggingFace embeddings? sentence-transformers/all-MiniLM-L6-v2 is
# free, runs locally (no API key, no cost), and is small/fast enough to
# run on a laptop CPU - a good, honest choice for a student project
# instead of a paid OpenAI embedding API.
#
# Why FAISS? It's Facebook AI's library for fast nearest-neighbor search
# over vectors. It runs locally, is free, and is the most common vector
# store used in beginner-to-intermediate RAG projects, so it's a safe,
# well-documented choice to explain in an interview.

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from utils import EMBEDDING_MODEL, INDEX_DIR


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def build_vector_store(chunks: list, save: bool = True):
    """Embeds a list of text chunks and builds a FAISS index from them."""
    embeddings = get_embedding_model()
    vector_store = FAISS.from_texts(chunks, embeddings)
    if save:
        vector_store.save_local(INDEX_DIR)
    return vector_store


def load_vector_store():
    """Loads a previously saved FAISS index from disk."""
    embeddings = get_embedding_model()
    return FAISS.load_local(
        INDEX_DIR, embeddings, allow_dangerous_deserialization=True
    )


def retrieve_relevant_chunks(query: str, vector_store, k: int = 4) -> list:
    """Returns the k chunks most relevant to the query, most relevant first."""
    results = vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]


if __name__ == "__main__":
    # Small end-to-end test: build an index from a few sentences and
    # check that a relevant query actually retrieves the right one.
    sample_chunks = [
        "The company's revenue for FY2024 was 500 crore rupees.",
        "The weather in Bangalore is pleasant during monsoon season.",
        "Net profit increased by 15% compared to last year.",
        "The office cafeteria serves South Indian food on Mondays.",
    ]
    store = build_vector_store(sample_chunks, save=False)
    results = retrieve_relevant_chunks("What was the company's profit?", store, k=2)
    print("Top matches for 'What was the company's profit?':")
    for r in results:
        print(" -", r)
