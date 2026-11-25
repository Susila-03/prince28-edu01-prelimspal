"""Parse approved downloaded corpus files and save them to PostgreSQL."""

import argparse
import asyncio
import json
import time
from collections import Counter
from pathlib import Path

from prelimspal.config import get_settings
from prelimspal.db.session import make_engine, make_sessionmaker
from prelimspal.ingest.fetch import read_sources
from prelimspal.ingest.parse import ParseError, parse_file
from prelimspal.ingest.store import (
    document_id,
    failed_paths,
    parsed_ids,
    save_document,
    save_failure,
)

ROOT = Path(__file__).resolve().parents[1]


def load_records() -> list[dict]:
    """Load only downloaded files whose URLs are approved in sources.csv."""
    approved = {
        source.url: source
        for source in read_sources(ROOT / "data" / "sources.csv")
        if source.ingestion_permission == "APPROVED_FOR_INGESTION"
    }

    manifest_path = ROOT / "data" / "manifest.jsonl"
    latest = {}

    if not manifest_path.exists():
        return []

    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        latest[record["url"]] = record

    records = []

    for url, record in latest.items():
        source = approved.get(url)

        if source is None or record.get("status") != "downloaded":
            continue

        path = ROOT / record["path"]

        if not path.is_file():
            continue

        record["source"] = source.source
        record["licence"] = source.licence
        record["title"] = source.title or record.get("title", "")

        records.append(record)

    return records


async def run(limit: int | None, retry_failed: bool) -> None:
    records = load_records()

    if not records:
        print("No approved downloaded files are available for parsing.")
        print("Review data/sources.csv and approve only eligible sources.")
        return

    settings = get_settings()
    engine = make_engine(settings)
    sessions = make_sessionmaker(engine)

    started = time.perf_counter()
    parsed = 0
    pages = 0
    failed = 0
    reasons = Counter()

    try:
        async with sessions() as session:
            existing = await parsed_ids(session)
            previous_failures = await failed_paths(session)

            already_parsed = sum(document_id(record["sha256"]) in existing for record in records)
            failed_before = sum(record["path"] in previous_failures for record in records)

            if retry_failed:
                pending = [record for record in records if record["path"] in previous_failures]
            else:
                pending = [
                    record
                    for record in records
                    if document_id(record["sha256"]) not in existing
                    and record["path"] not in previous_failures
                ]

            if limit is not None:
                pending = pending[:limit]

            print(f"approved_files={len(records)}")
            print(f"already_parsed={already_parsed}")
            print(f"failed_before={failed_before}")
            print(f"files_to_process={len(pending)}")

            if not pending:
                print("No files need processing.")
                return

            for index, record in enumerate(pending, start=1):
                path = ROOT / record["path"]

                try:
                    result = parse_file(path)
                    await save_document(session, record, result)
                    parsed += 1
                    pages += len(result.pages)

                except ParseError as error:
                    await save_failure(session, record, error)
                    failed += 1
                    reasons[error.reason] += 1

                if index % 50 == 0 or index == len(pending):
                    print(f"progress={index}/{len(pending)} parsed={parsed} failed={failed}")

        elapsed = time.perf_counter() - started

        print(
            f"files={len(pending)} parsed={parsed} "
            f"failed={failed} pages={pages} seconds={elapsed:.1f}"
        )

        if reasons:
            print(
                "failure reasons:",
                ", ".join(f"{reason}={count}" for reason, count in sorted(reasons.items())),
            )

    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse approved corpus files.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of files to process.",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Retry previously failed approved files.",
    )
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")

    asyncio.run(run(args.limit, args.retry_failed))


if __name__ == "__main__":
    main()
