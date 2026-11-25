"""Compare PDF and HTML parsers on the 10 largest local files."""

import argparse
import time
from html.parser import HTMLParser
from pathlib import Path

from prelimspal.ingest.parse import (
    ParseError,
    finish,
    parse_html,
    parse_pdf_pymupdf,
    parse_pdf_pypdf,
    split_pages,
)


class PlainTextExtractor(HTMLParser):
    """Extract text by stripping HTML tags."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        if data.strip():
            self.parts.append(data.strip())


def parse_html_plain(path: Path):
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
        elapsed = time.perf_counter() - start

        return {
            "document": document,
            "seconds": elapsed,
            "error": "",
        }
    except (ParseError, Exception) as exc:
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
        f"{result['seconds']:.2f}s"
    )


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--confirm-permission",
        action="store_true",
        help="Confirm permission to extract text from the selected documents.",
    )
    argument_parser.add_argument(
        "paths",
        nargs="*",
        help="Optional PDF or HTML file paths.",
    )
    args = argument_parser.parse_args()

    if args.paths:
        files = [Path(p) for p in args.paths]
    else:
        files = sorted(
            [
                p
                for p in Path("data/raw").rglob("*")
                if p.is_file() and p.suffix.lower() in {".pdf", ".html", ".htm"}
            ],
            key=lambda p: p.stat().st_size,
            reverse=True,
        )[:10]

    if not files:
        print("No PDF or HTML files found.")
        return

    print("Selected files:")
    for path in files:
        print(f"  {path}")

    if not args.confirm_permission:
        print(
            "\nFiles listed only. No documents were parsed.\n"
            "Run again with --confirm-permission only after "
            "obtaining permission."
        )
        return

    rows = []

    for path in files:
        if not path.is_file():
            print(f"Skipping missing file: {path}")
            continue

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            first = measure(parse_pdf_pymupdf, path)
            second = measure(parse_pdf_pypdf, path)
            parser_names = ("PyMuPDF", "pypdf")
        elif suffix in {".html", ".htm"}:
            first = measure(parse_html, path)
            second = measure(parse_html_plain, path)
            parser_names = ("Trafilatura", "Plain tag stripping")
        else:
            continue

        print(f"\n{path.name}")
        print(f"  {parser_names[0]}: {metrics(first)}")
        print(f"  {parser_names[1]}: {metrics(second)}")

        rows.append(
            f"| {path.name} | {parser_names[0]}: {metrics(first)} "
            f"| {parser_names[1]}: {metrics(second)} | To review |"
        )

    if rows:
        notes = Path("NOTES.md")
        with notes.open("a", encoding="utf-8") as file:
            file.write("\n\n## Parser comparison\n\n")
            file.write("| File | Parser 1 | Parser 2 | Better parser and why |\n")
            file.write("|---|---|---|---|\n")
            file.write("\n".join(rows))
            file.write("\n")

        print("\nComparison table added to NOTES.md.")


if __name__ == "__main__":
    main()
