"""Compare parsers using only synthetic hard-case samples."""

import time
from html.parser import HTMLParser
from pathlib import Path

from prelimspal.ingest.parse import (
    finish,
    parse_html,
    parse_pdf_pymupdf,
    parse_pdf_pypdf,
    split_pages,
)

SAMPLE_DIR = Path("data/samples/parser_comparison/hard_cases")


class PlainTextExtractor(HTMLParser):
    """Extract text by stripping HTML tags."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        if data.strip():
            self.parts.append(data.strip())


def parse_html_plain(path):
    html = path.read_text(encoding="utf-8", errors="replace")
    extractor = PlainTextExtractor()
    extractor.feed(html)
    text = "\n".join(extractor.parts)

    return finish(
        "plain-tag-strip",
        "html",
        path.stem,
        split_pages(text),
    )


def measure(function, path):
    start = time.perf_counter()

    try:
        document = function(path)
        return {
            "document": document,
            "seconds": time.perf_counter() - start,
            "error": "",
        }
    except Exception as exc:
        return {
            "document": None,
            "seconds": time.perf_counter() - start,
            "error": str(exc)[:100],
        }


def metrics(result):
    document = result["document"]

    if document is None:
        return f"ERROR: {result['error']}"

    pages = document.pages
    chars = sum(len(page.text) for page in pages)
    headings = sum(len(page.headings) for page in pages)
    tables = sum(page.tables for page in pages)

    return (
        f"{len(pages)} pages, {chars} chars, "
        f"{headings} headings, {tables} tables, "
        f"{result['seconds']:.3f}s"
    )


def main():
    files = sorted(
        path
        for path in SAMPLE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in {".pdf", ".html", ".htm"}
    )

    print(f"Found {len(files)} synthetic files.")

    for path in files:
        if path.suffix.lower() == ".pdf":
            first = measure(parse_pdf_pymupdf, path)
            second = measure(parse_pdf_pypdf, path)
            names = ("PyMuPDF", "pypdf")
        else:
            first = measure(parse_html, path)
            second = measure(parse_html_plain, path)
            names = ("Trafilatura", "Plain tag stripping")

        print(f"\n{path.name}")
        print(f"  {names[0]}: {metrics(first)}")
        print(f"  {names[1]}: {metrics(second)}")

    print("\nComparison finished. NOTES.md and the database were not changed.")


if __name__ == "__main__":
    main()
