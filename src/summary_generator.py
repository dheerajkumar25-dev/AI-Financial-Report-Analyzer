# summary_generator.py
# Uses the Groq LLM to generate three things from the report text:
#   1. A plain-language financial summary
#   2. A risk analysis
#   3. A business segment / insights summary
#
# Simplification (worth stating honestly in an interview): a full annual
# report is far longer than any LLM's context window, so this sends only
# the first MAX_CHARS characters of cleaned text - which usually covers
# the Management Discussion & Analysis section where this information
# typically lives. A more thorough version would summarize each chunk
# separately and then combine those summaries ("map-reduce summarization")
# - listed as a future improvement in the README rather than built here,
# to keep this project at a level you can fully explain in an interview.

from groq import Groq

from utils import GROQ_API_KEY, GROQ_MODEL

MAX_CHARS = 8000  # keep the prompt a reasonable size for a free-tier API


def _call_groq(prompt: str) -> str:
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


def generate_financial_summary(text: str) -> str:
    prompt = f"""Summarize the key financial performance from this annual
report excerpt in 5-6 simple bullet points (revenue, profit, growth trends).
Use plain language a non-finance person could understand.

Report excerpt:
{text[:MAX_CHARS]}
"""
    return _call_groq(prompt)


def generate_risk_analysis(text: str) -> str:
    prompt = f"""Based on this annual report excerpt, list the top 5 business
or financial risks mentioned or implied. Be specific, not generic.

Report excerpt:
{text[:MAX_CHARS]}
"""
    return _call_groq(prompt)


def generate_business_insights(text: str) -> str:
    prompt = f"""Based on this annual report excerpt, describe the company's
main business segments and any notable growth or decline in each, in 4-5
bullet points.

Report excerpt:
{text[:MAX_CHARS]}
"""
    return _call_groq(prompt)


if __name__ == "__main__":
    print("This module needs a real GROQ_API_KEY to run.")
    print("Test it through the Streamlit app after uploading a PDF (app/app.py).")
