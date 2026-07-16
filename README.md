# AI Financial Report Analyzer

An AI-powered application that analyzes a company's annual report PDF to generate financial summaries, extract key financial metrics, perform risk analysis, and answer natural language questions using Retrieval-Augmented Generation (RAG).

---

## Features

- 📄 Upload annual report PDFs for analysis
- 🤖 AI-powered financial summary generation
- 📊 Automatic extraction of key financial metrics
- ⚠️ Financial risk analysis and business insights
- 💬 Ask questions using Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search using FAISS and Hugging Face embeddings
- 📈 Interactive financial charts and visualizations
- 🌐 Modern Streamlit web dashboard
- 🐳 Docker support for containerized deployment

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| AI / LLM | LangChain, Groq API |
| Embeddings | Hugging Face Sentence Transformers |
| Vector Database | FAISS |
| PDF Processing | PyMuPDF |
| Visualization | Plotly |
| Frontend | Streamlit |
| Deployment | Docker |

---

## Screenshots

### Home Page

> Add screenshot here

### Upload Report

> Add screenshot here

### Financial Summary

> Add screenshot here

### Ask AI

> Add screenshot here

---

## Testing

This project has been tested locally on **Windows (Python 3.12)**.

### Verified Components

- ✅ PDF extraction
- ✅ Text preprocessing and cleaning
- ✅ Document chunking
- ✅ Semantic embeddings using Hugging Face
- ✅ FAISS vector database
- ✅ Financial metric extraction
- ✅ AI-powered summary generation
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Streamlit dashboard
- ✅ Financial charts and visualizations

> **Note:** Create a `.env` file and add your `GROQ_API_KEY` before running AI-powered summarization and question answering.

---

# Project Pipeline

```
Annual Report PDF
        │
        ▼
 PDF Extraction
        │
        ▼
 Text Cleaning
        │
        ▼
 Document Chunking
        │
        ▼
 Embeddings
        │
        ▼
 FAISS Vector Store
        │
        ▼
      Groq LLM
   ┌───────────────┐
   ▼               ▼
Summary         Question Answering
   │               │
   └──────► Streamlit Dashboard
```

### Workflow

1. Upload a financial report PDF.
2. Extract text using **PyMuPDF**.
3. Clean and preprocess the extracted text.
4. Split the text into overlapping chunks.
5. Generate semantic embeddings using Hugging Face.
6. Store embeddings inside a FAISS vector database.
7. Extract financial metrics using deterministic regex.
8. Generate AI summaries, risk analysis, and business insights.
9. Answer user questions through Retrieval-Augmented Generation.
10. Visualize extracted financial metrics with Plotly charts.

---

# Design Decisions

Instead of relying on an LLM for everything, the project combines deterministic extraction with Generative AI.

- Financial metrics (Revenue, EPS, Net Profit, Assets, Liabilities, etc.) are extracted using **regular expressions**, ensuring numerical values come directly from the report.
- Language-intensive tasks such as **summarization**, **risk analysis**, and **question answering** use **Groq LLM** with Retrieval-Augmented Generation (RAG).
- FAISS retrieves only the most relevant document chunks before sending them to the LLM, reducing hallucinations and improving response accuracy.

---

## Why These Libraries

- **PyMuPDF (`fitz`)** — Fast and lightweight PDF processing without additional system dependencies.
- **Sentence Transformers** — Free local embedding generation using Hugging Face models.
- **FAISS** — Efficient semantic similarity search for Retrieval-Augmented Generation.
- **LangChain** — Used for document chunking and FAISS integration while keeping the code modular.
- **Groq API** — High-speed inference for open-source LLMs with a free developer tier.

---

## Project Structure

```text
AI-Financial-Report-Analyzer/
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── index/
│
├── reports/
│
├── notebooks/
│   └── exploration.ipynb
│
├── src/
│   ├── utils.py
│   ├── pdf_extractor.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── financial_metrics.py
│   ├── summary_generator.py
│   ├── rag_qa.py
│   └── charts.py
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## Getting Started

### Clone Repository

```bash
git clone https://github.com/dheerajkumar25-dev/AI-Financial-Report-Analyzer.git

cd AI-Financial-Report-Analyzer
```

### Create Virtual Environment

```powershell
python -m venv venv

.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Configure Environment Variables

Copy:

```powershell
copy .env.example .env
```

Open `.env` and add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run Application

```powershell
streamlit run app/app.py
```

The application will launch at:

```
http://localhost:8501
```

---

## Docker

Build the image:

```powershell
docker build -t financial-analyzer .
```

Run the container:

```powershell
docker run -p 8501:8501 -e GROQ_API_KEY=your_key financial-analyzer
```

---

## Evaluation

The **Ask AI** module provides an evaluation panel containing:

- Response latency
- Retrieved document chunks
- Generated prompt
- Approximate token count

These details improve transparency and make debugging easier.

---

## Known Limitations

- Regex-based metric extraction may not capture every reporting format used by companies.
- Summarization currently processes the first section of the report rather than the entire document.
- Only one PDF can be analyzed at a time.
- Requires an internet connection for Groq API responses.

---

## Future Improvements

- Multi-document comparison and year-over-year financial analysis
- Full-document map-reduce summarization
- Embedding cache for faster repeated analysis
- Source-page citations for AI responses
- Automated unit tests for extraction and chunking modules
- Export reports as PDF

---

## License

This project is intended for educational and portfolio purposes.