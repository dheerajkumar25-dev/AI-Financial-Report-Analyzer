# chunker.py
# Splits cleaned text into overlapping chunks. Chunking matters because:
#   - Embedding models have a max input length
#   - Smaller chunks give more precise retrieval (you find the exact
#     paragraph that answers a question, not a whole 50-page document)
#   - Overlap between chunks avoids cutting a sentence/answer in half
#     right at a chunk boundary
#
# Uses LangChain's RecursiveCharacterTextSplitter (the standard choice for
# this - it tries to split on paragraph breaks first, then sentences, then
# words, so chunks stay as semantically coherent as possible).
# Falls back to a simple manual splitter if langchain isn't installed yet,
# so this file can still be tested on its own.

CHUNK_SIZE = 1000       # characters per chunk
CHUNK_OVERLAP = 150     # characters shared between consecutive chunks

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


def chunk_text(text: str) -> list:
    """Returns a list of text chunks (plain strings)."""
    if LANGCHAIN_AVAILABLE:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        return splitter.split_text(text)

    # Manual fallback: simple sliding window over the text
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


if __name__ == "__main__":
    sample = "This is a test sentence. " * 200  # ~5000 characters
    chunks = chunk_text(sample)
    print(f"LangChain available: {LANGCHAIN_AVAILABLE}")
    print(f"Split into {len(chunks)} chunks")
    print(f"First chunk length: {len(chunks[0])} characters")
    print(f"First chunk preview: {chunks[0][:100]}...")
