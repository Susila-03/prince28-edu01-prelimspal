import asyncio

from sqlalchemy import text

from prelimspal.config import get_settings
from prelimspal.db.session import make_engine


async def main():
    engine = make_engine(get_settings())
    async with engine.connect() as conn:
        queries = {
            "DOCUMENTS": """
                SELECT doc_type, COUNT(*) AS documents
                FROM documents GROUP BY doc_type ORDER BY doc_type
            """,
            "PAGES": """
                SELECT COUNT(*) AS total_pages FROM pages
            """,
            "INGEST STATUS": """
                SELECT status, COUNT(*) AS files
                FROM ingest_items GROUP BY status ORDER BY status
            """,
            "PARSE FAILURES": """
                SELECT path, reason, detail FROM parse_failures ORDER BY path
            """,
            "INGESTED DOCUMENTS": """
                SELECT title, doc_type, external_id
                FROM documents ORDER BY title
            """,
            "INGEST ITEMS": """
                SELECT id, status, record->>'path' AS path,
                       record->>'url' AS url, attempts, error
                FROM ingest_items ORDER BY id
            """,
        }

        for title, query in queries.items():
            print(f"\n===== {title} =====")
            result = await conn.execute(text(query))
            for row in result:
                print(dict(row._mapping))

    await engine.dispose()


asyncio.run(main())
