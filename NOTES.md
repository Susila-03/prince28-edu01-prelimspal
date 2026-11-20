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

---

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

Result:

```text
prelimspal:dev   c535460906cf   300MB   70MB
```

Image size: 300 MB (below the 400 MB target).

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

Changed the `health.py` docstring temporarily and rebuilt the image.

Result:

```text
CACHED [builder 4/6] RUN ... uv sync --locked --no-install-project --no-dev
```

The dependency layer was reused, avoiding unnecessary dependency installation.

First build time: approximately 1–3 minutes (as recorded).

Second build time: 53.8 seconds.

The temporary code change was reverted after the cache test.

---

## Project Notes

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

---

## D04 · Docker, Compose and tests

### The image

Command:

```text
docker images prelimspal:dev
```

Output:

```text
prelimspal:dev   c535460906cf   300MB   70MB
```

Command:

```text
docker run --rm prelimspal:dev id
```

Output:

```text
uid=999(app) gid=999(app) groups=999(app)
```

- Size: 300 MB (target: under 400 MB)
- Non-root user: uid=999(app)
- First build: approximately 1–3 minutes
- After changing one line of code: 53.8 seconds
- Cached step: builder 4/6 — dependency installation was reused.

### The stack

Command:

```text
docker compose ps -a
```

Output:

```text
prelimspal-api-1       Up 19 hours (healthy)
prelimspal-db-1        Up 19 hours (healthy)
prelimspal-migrate-1   Exited (0)
prelimspal-redis-1     Up 19 hours (healthy)
```

Command:

```text
docker compose logs migrate
```

Output:

```text
INFO [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO [alembic.runtime.migration] Will assume transactional DDL.
records=5 inserted=0 updated=0 unchanged=5
INFO [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO [alembic.runtime.migration] Will assume transactional DDL.
records=5 inserted=0 updated=0 unchanged=5
```

Migration exited with code 0, meaning it completed successfully.

### Breaking the database on purpose

```text
Database stopped:

/health → HTTP 200 OK

{"status":"ok","app":"prelimspal","env":"local"}

/ready → HTTP 503 Service Unavailable

{"status":"not_ready","checks":{"database":false}}

Database started:

/ready → HTTP 200 OK
```

**Why should a load balancer stop sending traffic here but not restart the app?**

Readiness checks whether the application can handle requests that depend on the database. If the database is unavailable, the load balancer should stop routing traffic to the application.

Liveness checks whether the application itself is running. Since the API is still running, it should not be restarted just because the database is temporarily unavailable.

### Tests and coverage

```text
uv run poe test
→ 16 passed

uv run poe test-integration
→ 7 passed

Coverage TOTAL, unit only
→ 84%

Coverage TOTAL, with integration tests
→ [Add actual combined coverage result]
```

**Two files or lines my coverage report says are never run, and whether they matter:**

1. `src/prelimspal/db/repository.py` — lines 16, 29–37, 42, 47–62, 65–66 were not covered in the unit-only report. These are database-related paths that integration tests help exercise.

2. `src/prelimspal/api/deps.py` — lines 21–22, 26, 31–36 were not covered in the unit-only report. These dependency paths may need additional tests depending on their purpose.
