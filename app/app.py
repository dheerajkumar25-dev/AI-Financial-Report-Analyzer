# app.py
# Streamlit dashboard for the AI Financial Report Analyzer.
#
# Run from the project root:
#   streamlit run app/app.py
#
# Design note: this uses st.session_state to keep the extracted text,
# vector store, and metrics available as the user moves between pages,
# instead of a class wrapping everything - Streamlit apps are usually
# simpler to read and debug as plain functions + session_state than as
# an object-oriented app, and that's the style used throughout this file.

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st

from utils import ensure_dirs, RAW_DIR
from pdf_extractor import extract_text_from_pdf
from text_cleaner import clean_text
from chunker import chunk_text
from embeddings import build_vector_store
from financial_metrics import extract_financial_metrics
from charts import build_metrics_bar_chart
from summary_generator import generate_financial_summary, generate_risk_analysis, generate_business_insights
from rag_qa import ask_question

ensure_dirs()

st.set_page_config(page_title="AI Financial Report Analyzer", page_icon="📊", layout="wide")

# ---------- session state defaults ----------
for key in ["report_text", "vector_store", "metrics", "pdf_name"]:
    if key not in st.session_state:
        st.session_state[key] = None

st.sidebar.title("📊 Financial Report Analyzer")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Upload Report", "Financial Summary", "Risk Analysis",
     "Business Insights", "Ask AI", "Charts", "Download Summary"],
)

# ============================================================
# HOME
# ============================================================
if page == "Home":
    st.title("AI Financial Report Analyzer")
    st.write(
        "Upload a company's annual report PDF and this tool will extract key "
        "financial metrics, generate an AI-written summary, flag risks, and "
        "let you ask questions directly about the report."
    )
    st.markdown("""
    **How to use this app:**
    1. Go to **Upload Report** and upload an annual report PDF.
    2. Visit **Financial Summary**, **Risk Analysis**, and **Business Insights**
       for AI-generated analysis.
    3. Use **Ask AI** to ask specific questions about the report.
    4. Check **Charts** for a visual view of key numbers.
    5. Use **Download Summary** to save everything as a text file.
    """)
    if st.session_state.pdf_name:
        st.success(f"Currently loaded report: {st.session_state.pdf_name}")
    else:
        st.info("No report uploaded yet. Start with 'Upload Report'.")

# ============================================================
# UPLOAD REPORT
# ============================================================
elif page == "Upload Report":
    st.title("Upload Annual Report")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        save_path = os.path.join(RAW_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Saved: {save_path}")

        if st.button("Process this report", type="primary"):
            with st.spinner("Extracting text from PDF..."):
                raw_text = extract_text_from_pdf(save_path)
                cleaned = clean_text(raw_text)

            st.write(f"Extracted {len(cleaned)} characters of clean text.")

            with st.spinner("Chunking text and building the vector index (this can take a minute)..."):
                chunks = chunk_text(cleaned)
                vector_store = build_vector_store(chunks)

            with st.spinner("Extracting key financial metrics..."):
                metrics = extract_financial_metrics(cleaned)

            st.session_state.report_text = cleaned
            st.session_state.vector_store = vector_store
            st.session_state.metrics = metrics
            st.session_state.pdf_name = uploaded_file.name

            st.success(f"Done! Split into {len(chunks)} chunks and indexed.")
            st.subheader("Quick preview of extracted metrics")
            st.json(metrics)

# ============================================================
# FINANCIAL SUMMARY
# ============================================================
elif page == "Financial Summary":
    st.title("Financial Summary")
    if not st.session_state.report_text:
        st.warning("Upload and process a report first (see 'Upload Report').")
    else:
        if st.button("Generate Summary", type="primary"):
            with st.spinner("Asking the AI to summarize..."):
                summary = generate_financial_summary(st.session_state.report_text)
                st.session_state.financial_summary = summary
        if "financial_summary" in st.session_state and st.session_state.get("financial_summary"):
            st.markdown(st.session_state.financial_summary)

# ============================================================
# RISK ANALYSIS
# ============================================================
elif page == "Risk Analysis":
    st.title("Risk Analysis")
    if not st.session_state.report_text:
        st.warning("Upload and process a report first (see 'Upload Report').")
    else:
        if st.button("Generate Risk Analysis", type="primary"):
            with st.spinner("Analyzing risks..."):
                risks = generate_risk_analysis(st.session_state.report_text)
                st.session_state.risk_analysis = risks
        if st.session_state.get("risk_analysis"):
            st.markdown(st.session_state.risk_analysis)

# ============================================================
# BUSINESS INSIGHTS
# ============================================================
elif page == "Business Insights":
    st.title("Business Segment Insights")
    if not st.session_state.report_text:
        st.warning("Upload and process a report first (see 'Upload Report').")
    else:
        if st.button("Generate Business Insights", type="primary"):
            with st.spinner("Analyzing business segments..."):
                insights = generate_business_insights(st.session_state.report_text)
                st.session_state.business_insights = insights
        if st.session_state.get("business_insights"):
            st.markdown(st.session_state.business_insights)

# ============================================================
# ASK AI
# ============================================================
elif page == "Ask AI":
    st.title("Ask AI About This Report")
    if not st.session_state.vector_store:
        st.warning("Upload and process a report first (see 'Upload Report').")
    else:
        question = st.text_input("Your question", placeholder="e.g. What was the revenue growth this year?")
        if st.button("Ask", type="primary") and question:
            with st.spinner("Retrieving relevant sections and generating an answer..."):
                result = ask_question(question, st.session_state.vector_store)

            st.subheader("Answer")
            st.write(result["answer"])

            with st.expander("Evaluation details (for transparency / debugging)"):
                st.write(f"**Latency:** {result['latency_seconds']} seconds")
                st.write(f"**Approx. token count (prompt):** {result['approx_token_count']}")
                st.write("**Retrieved chunks used as context:**")
                for i, chunk in enumerate(result["retrieved_chunks"], 1):
                    st.text_area(f"Chunk {i}", chunk, height=100)
                st.write("**Full prompt sent to the LLM:**")
                st.code(result["prompt_used"])

# ============================================================
# CHARTS
# ============================================================
elif page == "Charts":
    st.title("Financial Metrics Charts")
    if not st.session_state.metrics:
        st.warning("Upload and process a report first (see 'Upload Report').")
    else:
        st.plotly_chart(build_metrics_bar_chart(st.session_state.metrics), use_container_width=True)
        st.subheader("Raw extracted values")
        st.json(st.session_state.metrics)

# ============================================================
# DOWNLOAD SUMMARY
# ============================================================
elif page == "Download Summary":
    st.title("Download Full Summary")
    if not st.session_state.report_text:
        st.warning("Upload and process a report first (see 'Upload Report').")
    else:
        parts = [f"AI FINANCIAL REPORT ANALYSIS - {st.session_state.pdf_name}", "=" * 60, ""]

        if st.session_state.metrics:
            parts.append("KEY FINANCIAL METRICS")
            for k, v in st.session_state.metrics.items():
                parts.append(f"  {k}: {v}")
            parts.append("")

        if st.session_state.get("financial_summary"):
            parts.append("FINANCIAL SUMMARY")
            parts.append(st.session_state.financial_summary)
            parts.append("")

        if st.session_state.get("risk_analysis"):
            parts.append("RISK ANALYSIS")
            parts.append(st.session_state.risk_analysis)
            parts.append("")

        if st.session_state.get("business_insights"):
            parts.append("BUSINESS INSIGHTS")
            parts.append(st.session_state.business_insights)

        full_report = "\n".join(parts)
        st.text_area("Preview", full_report, height=400)
        st.download_button(
            "Download as .txt",
            data=full_report.encode("utf-8"),
            file_name="financial_report_summary.txt",
            mime="text/plain",
        )
