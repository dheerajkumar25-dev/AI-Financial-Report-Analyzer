# text_cleaner.py
# Cleans raw PDF text before it gets chunked and embedded.
# PDF extraction often leaves messy whitespace, repeated headers/footers,
# and page numbers - this removes the obvious noise.

import re


def clean_text(text: str) -> str:
    # Collapse multiple blank lines into one
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Collapse multiple spaces/tabs into one
    text = re.sub(r"[ \t]+", " ", text)

    # Remove standalone page-number lines like "12" or "Page 12"
    text = re.sub(r"(?im)^\s*(page\s*)?\d{1,4}\s*$", "", text)

    # Strip leading/trailing whitespace on each line
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(line for line in lines if line != "")

    return text.strip()


if __name__ == "__main__":
    sample = """

    Annual   Report   2024


    Page 1

    Revenue grew by 12% this year.



    12

    Net profit increased.
    """
    print(clean_text(sample))
