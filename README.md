# AI Financial Report Analyzer

An AI tool that reads a company's annual report PDF and lets you: get an instant financial summary, see key metrics (Revenue, Net Profit, EPS, etc.), read a risk analysis, and ask free-form questions about the report — answered using RAG (Retrieval-Augmented Generation) grounded in the actual document text.

## Testing

This project has been tested locally on Windows using Python 3.12.

### Verified Components

- ✅ PDF extraction from financial reports
- ✅ Text preprocessing and cleaning
- ✅ Document chunking
- ✅ Semantic embeddings using Hugging Face
- ✅ FAISS vector database
- ✅ Financial metric extraction
- ✅ AI-powered summary generation
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Streamlit dashboard
- ✅ Financial charts and visualizations

> **Note:** To use AI-powered summarization and question answering, create a `.env` file and add your `GROQ_API_KEY`.
## Why these libraries

- **PyMuPDF (`fitz`)**: fast, no external system dependencies (some PDF libraries need `poppler` installed separately on Windows, which is a common setup headache).
- **HuggingFace `sentence-transformers` embeddings**: free, runs locally on your CPU, no API key or cost — versus a paid embedding API.
- **FAISS**: the standard free, local vector similarity search library — widely used, well documented, easy to explain in an interview.
- **LangChain**: used specifically for `RecursiveCharacterTextSplitter` (smart chunking) and the `FAISS` wrapper — not for heavier agent/chain abstractions, to keep the code readable.
- **Groq API**: free tier, fast inference, hosts open models (Llama 3) — no paid service needed.

## Project Structure

```
AI-Financial-Report-Analyzer/
├── app/
│   └── app.py                  # Streamlit dashboard
├── data/
│   ├── raw/                    # uploaded PDFs
│   └── processed/               # (reserved for saved intermediate text, if you extend this)
├── models/
│   └── index/                   # FAISS vector index (auto-generated)
├── reports/                     # (reserved for saved analysis reports)
├── notebooks/
│   └── exploration.ipynb        # walkthrough of the pipeline
├── src/
│   ├── utils.py                 # shared paths, config, API key loading
│   ├── pdf_extractor.py         # PDF → text (PyMuPDF)
│   ├── text_cleaner.py          # remove noise from extracted text
│   ├── chunker.py                # split text into chunks
│   ├── embeddings.py             # embeddings + FAISS vector store
│   ├── financial_metrics.py      # regex extraction of key numbers
│   ├── rag_qa.py                  # retrieval + Groq answer generation
│   ├── summary_generator.py       # LLM summary / risk / insights
│   └── charts.py                  # Plotly chart builders
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## How the pipeline works

1. **Upload** a PDF → `pdf_extractor.py` pulls out raw text.
2. **Clean** → `text_cleaner.py` removes page numbers, extra whitespace.
3. **Chunk** → `chunker.py` splits the cleaned text into ~1000-character overlapping pieces.
4. **Embed + Index** → `embeddings.py` turns each chunk into a vector (HuggingFace model) and stores them in a FAISS index.
5. **Extract metrics** → `financial_metrics.py` uses regex to pull Revenue, Net Profit, Operating Profit, EPS, Debt, Cash Flow, Expenses, Assets, Liabilities directly from the text (deterministic, not LLM-based — see design note in that file).
6. **Ask AI** → `rag_qa.py` retrieves the most relevant chunks for a question and asks Groq's LLM to answer using only that context (reduces hallucination, and lets you show exactly which chunks were used).
7. **Summary / Risk / Insights** → `summary_generator.py` sends the first ~8000 characters of cleaned text to Groq with three different prompts.
8. **Charts** → `charts.py` turns the extracted metrics into a Plotly bar chart.

### Design decision: regex for numbers, LLM for language

Numeric facts (Revenue, EPS, etc.) are extracted with regex, not by asking the LLM — this guarantees the number actually appears in the document, since LLMs can occasionally misstate figures. The LLM is used only for tasks that genuinely need language understanding: summarizing, judging risk, and free-form Q&A. This is a good thing to point out in an interview — it shows you thought about where an LLM is (and isn't) the right tool.

## Getting Started (Windows + PowerShell)

```powershell
git clone https://github.com/<your-username>/AI-Financial-Report-Analyzer.git
cd AI-Financial-Report-Analyzer

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Get a free Groq API key at [console.groq.com](https://console.groq.com), then:

```powershell
copy .env.example .env
```

Open `.env` and paste your key in place of `your_groq_api_key_here`.

Run the app:

```powershell
streamlit run app/app.py
```

This opens the dashboard in your browser (usually `http://localhost:8501`).

### Run with Docker

```powershell
docker build -t financial-analyzer .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key financial-analyzer
```

## Evaluation panel

The "Ask AI" tab includes an expandable evaluation panel per answer, showing:
- **Latency** — how long the retrieval + LLM call took
- **Retrieved chunks** — the exact text passed to the LLM as context
- **Prompt used** — the full prompt, for debugging/transparency
- **Approx. token count** — a word-count-based estimate (not an exact tokenizer count — noted in the code)

## Known limitations (worth stating upfront in an interview)

- Regex-based metric extraction won't catch every phrasing an annual report might use — it's a best-effort first pass.
- Summary/risk/insight generation only looks at the first ~8000 characters of the report, not the whole document (a full map-reduce summarization approach would be a natural next step).
- Currently supports one PDF at a time.

## Future improvements

- Support multiple reports and compare metrics year-over-year with real trend charts.
- Map-reduce summarization across the whole document, not just the first section.
- Cache embeddings so re-uploading the same PDF doesn't recompute the vector index.
- Add source-page citations to answers (the `extract_text_per_page` function in `pdf_extractor.py` is already there to support this).
- Add automated tests for the regex extraction and chunking logic.
