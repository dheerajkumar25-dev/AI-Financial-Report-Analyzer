
# summary_generator.py
# Uses Groq LLM to generate:
# 1. Financial summary
# 2. Risk analysis
# 3. Business segment insights

from groq import Groq

from utils import GROQ_API_KEY, GROQ_MODEL

MAX_CHARS = 8000


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


def _extract_business_sections(text: str) -> str:
    """
    Find relevant portions throughout the complete annual report.
    This avoids relying only on the first 8000 characters.
    """

    lines = text.splitlines()

    keywords = {
        "segment": 5,
        "business segment": 8,
        "segment information": 10,
        "segment reporting": 10,
        "operating segment": 8,
        "business overview": 7,
        "revenue from operations": 4,
        "segment revenue": 10,
        "segment results": 10,
        "segment assets": 8,
        "geographical segment": 7,
        "product portfolio": 5,
        "digital services": 6,
        "retail business": 5,
        "oil to chemicals": 6,
        "oil and gas": 5,
        "new energy": 5,
        "media business": 5,
        "growth in revenue": 3,
        "year-on-year": 2,
    }

    candidates = []

    # Scan the entire report and collect relevant line windows.
    for i, line in enumerate(lines):
        lower_line = line.lower()

        score = sum(
            weight
            for keyword, weight in keywords.items()
            if keyword in lower_line
        )

        if score > 0:
            start = max(0, i - 3)
            end = min(len(lines), i + 5)

            section = "\n".join(lines[start:end]).strip()

            if section:
                candidates.append((score, start, section))

    # If no relevant sections are detected, return the report tail.
    if not candidates:
        return text[-MAX_CHARS:]

    # Prioritize the most relevant sections.
    candidates.sort(key=lambda item: item[0], reverse=True)

    selected = []
    seen = set()
    total_chars = 0

    for score, start, section in candidates:
        normalized = section.lower()

        if normalized in seen:
            continue

        remaining = MAX_CHARS - total_chars

        if remaining <= 0:
            break

        section = section[:remaining]

        selected.append(section)
        seen.add(normalized)
        total_chars += len(section)

    return "\n\n".join(selected)


def generate_business_insights(text: str) -> str:
    relevant_text = _extract_business_sections(text)

    prompt = f"""You are a financial analyst reviewing a company's annual report.

Analyze the report excerpts below and identify the company's main
business segments and their performance.

Instructions:
1. Identify the main business segments.
2. Explain what each segment does.
3. Mention revenue, growth, or decline figures only when provided.
4. Compare segment performance wherever the report provides evidence.
5. Do not invent segment names, numbers, or growth rates.
6. If segment information is unavailable in the provided excerpts,
   clearly say that the available text does not contain enough information.

Present the findings in 4-5 clear bullet points.
Use simple language and include important figures when available.

Relevant annual report excerpts:
{relevant_text}
"""

    return _call_groq(prompt)


if __name__ == "__main__":
    print("This module needs a real GROQ_API_KEY to run.")
    print("Test it through the Streamlit app after uploading a PDF.")
