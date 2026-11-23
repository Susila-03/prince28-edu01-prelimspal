"""Download only sources explicitly approved for automatic use."""

import csv
import re
from pathlib import Path
from urllib.parse import urlparse

import httpx
from protego import Protego

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "data" / "sources.csv"
OUTPUT_DIR = ROOT / "data" / "raw"
USER_AGENT = "PrelimsPal/0.1"


def read_sources() -> list[dict[str, str]]:
    """Read and validate the source register."""
    with CSV_FILE.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(line for line in file if not line.lstrip().startswith("#"))

        required = {"url", "source", "licence", "title"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain url, source, licence, and title columns.")

        rows = list(reader)

    if not rows:
        raise ValueError("No source rows found.")

    for number, row in enumerate(rows, start=1):
        if not all(row.get(field, "").strip() for field in required):
            raise ValueError(f"Row {number}: missing required field or licence.")

        if not re.fullmatch(r"[a-zA-Z0-9_-]+", row["source"]):
            raise ValueError(f"Row {number}: invalid source folder name.")

        parsed = urlparse(row["url"])
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"Row {number}: a valid HTTPS URL is required.")

        if not row["licence"].startswith(("MANUAL_ONLY:", "AUTO_DOWNLOAD:")):
            raise ValueError(
                f"Row {number}: licence must start with MANUAL_ONLY: or AUTO_DOWNLOAD:."
            )

    return rows


def download_source(client: httpx.Client, row: dict[str, str]) -> bool:
    """Download one approved source after checking robots.txt."""
    url = row["url"]
    parsed = urlparse(url)

    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    try:
        robots_response = client.get(robots_url)
        robots_response.raise_for_status()

        content_type = robots_response.headers.get("content-type", "").lower()

        if "text/plain" not in content_type:
            print(f"REFUSED: robots.txt is not plain text for {url}")
            return False

        if not re.search(r"(?im)^\s*user-agent\s*:", robots_response.text):
            print(f"REFUSED: No User-agent directive in robots.txt for {url}")
            return False

    except httpx.HTTPError as error:
        print(f"REFUSED: Cannot verify robots.txt for {url}: {error}")
        return False

    rules = Protego.parse(robots_response.text)

    if not rules.can_fetch(USER_AGENT, url):
        print(f"REFUSED: robots.txt disallows {url}")
        return False

    extension = Path(parsed.path).suffix.lower()

    if extension not in {".pdf", ".html", ".htm"}:
        print(f"REFUSED: Unsupported document type: {url}")
        return False

    filename = Path(parsed.path).name

    if not filename:
        print(f"REFUSED: URL has no filename: {url}")
        return False

    destination_dir = OUTPUT_DIR / row["source"]
    destination = destination_dir / filename

    if destination.exists():
        print(f"SKIPPED: Already exists: {destination}")
        return False

    try:
        response = client.get(url)
        response.raise_for_status()
    except httpx.HTTPError as error:
        print(f"FAILED: Could not download {url}: {error}")
        return False

    content_type = response.headers.get("content-type", "").lower()

    if extension == ".pdf" and (
        "application/pdf" not in content_type or not response.content.startswith(b"%PDF-")
    ):
        print(f"REFUSED: Response is not a valid PDF: {url}")
        return False

    if extension in {".html", ".htm"} and "text/html" not in content_type:
        print(f"REFUSED: Response is not an HTML page: {url}")
        return False

    destination_dir.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)

    print(f"DOWNLOADED: {destination}")
    return True


def main() -> None:
    """Validate sources and download only approved documents."""
    try:
        rows = read_sources()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Source register error: {error}") from error

    downloaded = 0
    skipped = 0

    with httpx.Client(timeout=20.0, follow_redirects=False) as client:
        for row in rows:
            if row["licence"].startswith("MANUAL_ONLY:"):
                print(f"MANUAL ONLY: {row['title']}")
                skipped += 1
                continue

            if download_source(client, row):
                downloaded += 1
            else:
                skipped += 1

    print(f"\nFinished: downloaded={downloaded}, skipped={skipped}")


if __name__ == "__main__":
    main()
