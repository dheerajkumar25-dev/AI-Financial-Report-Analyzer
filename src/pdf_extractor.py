# pdf_extractor.py
# Extracts raw text from an annual report PDF using PyMuPDF (imported as `fitz`).
#
# Why PyMuPDF? It's fast, has no external system dependencies (unlike some
# PDF tools that need poppler installed separately), and handles the kind
# of multi-column, table-heavy PDFs that annual reports usually are,
# reasonably well.

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """Reads every page of a PDF and returns all text as one string."""
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages)


def extract_text_per_page(pdf_path: str) -> list:
    """Same as above, but keeps pages separate. Useful if you later want
    to show the user which page an answer came from."""
    doc = fitz.open(pdf_path)
    pages = [page.get_text() for page in doc]
    doc.close()
    return pages


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python src/pdf_extractor.py <path_to_pdf>")
    else:
        text = extract_text_from_pdf(sys.argv[1])
        print(f"Extracted {len(text)} characters from {sys.argv[1]}")
        print(text[:500])  # preview first 500 characters
