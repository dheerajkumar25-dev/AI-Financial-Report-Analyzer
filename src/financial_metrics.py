# financial_metrics.py
# Pulls out key numbers (Revenue, Net Profit, etc.) from the report text
# using regex, instead of asking the LLM for every single number.
#
# Why regex and not just ask the LLM? LLMs can occasionally misread or
# "round" numbers, which is risky for financial figures. Regex over the
# actual extracted text guarantees the number really appears in the
# document. This is also easy to explain and defend in an interview:
# "I used deterministic extraction for numeric facts, and the LLM only
# for things that need language understanding (summaries, risk analysis)."
#
# Limitation (worth mentioning honestly in an interview): annual reports
# format numbers inconsistently, so this regex approach won't catch every
# phrasing. It's a best-effort first pass, not a guaranteed-accurate
# parser - good enough for a student project, not for a real audit.

import re

# Each metric maps to a list of possible phrases used in reports.
METRIC_KEYWORDS = {
    "Revenue": ["total revenue", "revenue from operations", "total income", "revenue"],
    "Net Profit": ["net profit", "profit after tax", "net income"],
    "Operating Profit": ["operating profit", "ebitda", "operating income"],
    "EPS": ["earnings per share", "basic eps", "eps"],
    "Debt": ["total debt", "total borrowings", "long-term debt"],
    "Cash Flow": ["cash flow from operations", "operating cash flow", "net cash flow"],
    "Expense": ["total expenses", "total expenditure", "operating expenses"],
    "Assets": ["total assets"],
    "Liabilities": ["total liabilities"],
}

# Matches numbers like: 1,234.56  or  500  or  12.3 crore  or  Rs. 4,000 million
NUMBER_PATTERN = re.compile(
    r"(?:rs\.?|inr|₹)?\s*[\d][\d,]*\.?\d*\s*(?:crore|lakh|million|billion|cr\.?|mn|bn)?",
    re.IGNORECASE,
)


def extract_financial_metrics(text: str) -> dict:
    """
    Searches the report text for each metric's keywords and returns the
    first number found near that keyword. Returns 'Not found' for metrics
    it couldn't locate.
    """
    text_lower = text.lower()
    results = {}

    for metric, keywords in METRIC_KEYWORDS.items():
        value = None
        for keyword in keywords:
            idx = text_lower.find(keyword)
            if idx == -1:
                continue
            # look at a window of text right after the keyword
            window = text[idx: idx + len(keyword) + 60]
            match = NUMBER_PATTERN.search(window[len(keyword):])
            if match and match.group().strip():
                value = match.group().strip()
                break
        results[metric] = value if value else "Not found"

    return results


if __name__ == "__main__":
    sample_report = """
    The company reported total revenue of Rs. 4,500 crore in FY2024,
    up from last year. Net profit stood at 620 crore, driven by strong
    operating margins. Operating profit (EBITDA) was 890 crore.
    Basic EPS for the year was 45.2. Total debt reduced to 1,200 crore.
    Cash flow from operations was 750 crore, reflecting healthy liquidity.
    Total expenses for the year were 3,900 crore. Total assets stood at
    9,800 crore, while total liabilities were 4,300 crore.
    """
    metrics = extract_financial_metrics(sample_report)
    for k, v in metrics.items():
        print(f"{k}: {v}")
