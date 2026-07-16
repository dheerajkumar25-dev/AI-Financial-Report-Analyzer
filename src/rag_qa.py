# rag_qa.py
# The "generation" half of RAG: takes a user question, retrieves the most
# relevant chunks from the FAISS index, and asks Groq's LLM to answer
# using only those chunks as context.
#
# Why Groq? It hosts fast, free-tier access to open models (Llama 3, etc.)
# with no cost for reasonable usage - a good fit for a student project
# since the brief says "no paid services".
#
# Why give the model only retrieved chunks, not the whole report? Two
# reasons: (1) the whole annual report won't fit in the model's context
# window, and (2) grounding the answer in specific retrieved text reduces
# hallucination and lets you show the user exactly which chunks were used
# - which is also the "evaluation" feature the brief asked for.

import time
from groq import Groq

from utils import GROQ_API_KEY, GROQ_MODEL
from embeddings import retrieve_relevant_chunks

PROMPT_TEMPLATE = """You are a financial analyst assistant. Answer the question
using ONLY the context below, taken from a company's annual report.
If the answer isn't in the context, say "I couldn't find this in the report."

Context:
{context}

Question: {question}

Answer:"""


def _estimate_token_count(text: str) -> int:
    """
    Rough estimate only (~0.75 words per token is a common rule of thumb
    for English text). Good enough to show relative prompt size in the
    evaluation panel - not a substitute for a real tokenizer if you need
    exact counts.
    """
    words = len(text.split())
    return int(words / 0.75)


def ask_question(query: str, vector_store, k: int = 4) -> dict:
    """
    Runs the full RAG pipeline for one question and returns the answer
    plus evaluation info: retrieved chunks, prompt used, latency, token estimate.
    """
    start_time = time.time()

    chunks = retrieve_relevant_chunks(query, vector_store, k=k)
    context = "\n\n".join(chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=query)

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,  # low temperature: we want factual, consistent answers
    )
    answer = response.choices[0].message.content

    latency = round(time.time() - start_time, 2)

    return {
        "answer": answer,
        "retrieved_chunks": chunks,
        "prompt_used": prompt,
        "latency_seconds": latency,
        "approx_token_count": _estimate_token_count(prompt),
    }


if __name__ == "__main__":
    print("This module needs a real FAISS index and a GROQ_API_KEY to run.")
    print("Test it through the Streamlit app after uploading a PDF (app/app.py).")
