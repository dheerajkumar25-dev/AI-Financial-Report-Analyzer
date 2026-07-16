# charts.py
# Builds Plotly charts from the metrics dict returned by financial_metrics.py.
#
# Simplification (state this honestly if asked): a single annual report
# PDF usually gives one year's numbers, so these are single-bar "snapshot"
# charts, not multi-year trend lines. If you extend this to multiple
# reports (the brief mentions this as a future direction), you'd collect
# one metrics dict per year and plot them as a proper trend line instead.

import re

import plotly.graph_objects as go

NUMBER_ONLY = re.compile(r"[\d,]+\.?\d*")


def parse_number(value: str):
    """
    Converts a string like '4,500 crore' or 'Rs. 620' into a float.
    Returns None if no number could be parsed (e.g. value is 'Not found').
    Note: this does NOT convert crore/lakh/million to a common unit - it
    assumes all figures in one report use the same unit, which is a
    reasonable assumption within a single company's annual report.
    """
    if not value or value == "Not found":
        return None
    match = NUMBER_ONLY.search(value)
    if not match:
        return None
    return float(match.group().replace(",", ""))


def build_metrics_bar_chart(metrics: dict, title: str = "Key Financial Metrics"):
    """Takes the dict from extract_financial_metrics() and returns a Plotly bar chart."""
    labels = []
    values = []
    for metric, raw_value in metrics.items():
        number = parse_number(raw_value)
        if number is not None:
            labels.append(metric)
            values.append(number)

    fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color="#2563eb")])
    fig.update_layout(title=title, yaxis_title="Value (as reported)", xaxis_title="Metric")
    return fig


def build_single_metric_gauge(metric_name: str, raw_value: str):
    """A simple gauge-style indicator for one metric, e.g. EPS or Debt."""
    number = parse_number(raw_value) or 0
    fig = go.Figure(go.Indicator(
        mode="number",
        value=number,
        title={"text": metric_name},
    ))
    return fig


if __name__ == "__main__":
    sample_metrics = {
        "Revenue": "4,500 crore",
        "Net Profit": "620 crore",
        "Operating Profit": "890 crore",
        "EPS": "45.2",
        "Debt": "1,200 crore",
        "Cash Flow": "750 crore",
        "Expense": "3,900 crore",
        "Assets": "9,800 crore",
        "Liabilities": "4,300 crore",
    }
    print("Parsed numbers:")
    for k, v in sample_metrics.items():
        print(f"  {k}: {parse_number(v)}")
