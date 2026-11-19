# Engineering notes: PrelimsPal

## D03 · PostgreSQL

### Migrations (upgrade, downgrade, upgrade)

```text
Migration 1: 3194227a143e_create_documents_and_pages
Migration 2: 55504c4e6938_add_gin_index_on_metadata

Both migrations were applied successfully.
```

### The loader is idempotent

```text
Run 1: records=5 inserted=5 updated=0 unchanged=0

Run 2: records=5 inserted=0 updated=0 unchanged=5

Run 3: records=5 inserted=0 updated=1 unchanged=4
```

### EXPLAIN for ?year=2023

```text
Normal query:
Seq Scan on documents
Rows Removed by Filter: 5
Execution Time: 0.537 ms

With sequential scan disabled:
Bitmap Heap Scan on documents
Bitmap Index Scan on ix_documents_metadata_gin
Execution Time: 1.674 ms
```

**Why did the planner choose a Seq Scan on my table?**

The table contains only 5 records, so checking every row is inexpensive. A sequential scan is efficient for a small table.

**When would it switch to the GIN index?**

When the table grows and PostgreSQL estimates that using the GIN index is more efficient than scanning every row.


## D04 · Dockerfile and Image

### Docker image build

Command:
```text
docker build -t prelimspal:dev .
```

Result: Build successful.

### Image size

Command:
```text
docker images prelimspal:dev
```

Result: 300 MB (below the 400 MB target).

### Non-root user verification

Command:
```text
docker run --rm prelimspal:dev id
```

Output:
```text
uid=999(app) gid=999(app) groups=999(app)
```

Result: Container runs as the non-root `app` user.

### Docker build cache verification

Changed the health.py docstring temporarily and rebuilt the image.

Result:
```text
CACHED [builder 4/6] RUN ... uv sync --locked --no-install-project --no-dev
```

The dependency layer was reused.

First build time: approximately 1–3 minutes (record the actual time if available).

Second build time: 53.8 seconds.

The temporary code change was reverted after the cache test.

# Project Notes

## Day 03 - PostgreSQL
(existing notes...)

## Day 04 - Docker
(existing Docker notes...)

## Docker Compose verification
- PostgreSQL: healthy
- Redis: healthy
- Migrations: Exited (0)
- API: healthy
- GET /v1/documents: 200 OK
- Health check with DB stopped: status=ok
- Readiness check with DB stopped: not_ready
- Readiness after DB restart: ready
- Second loader run: records=5 inserted=0 updated=0 unchanged=5
