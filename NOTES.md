# Engineering notes: PrelimsPal

## D03 Â· PostgreSQL

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

## D04 Â· Dockerfile and Image

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

First build time: approximately 1â€“3 minutes (as recorded).

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

## D04 Â· Docker, Compose and tests

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
- First build: approximately 1â€“3 minutes
- After changing one line of code: 53.8 seconds
- Cached step: builder 4/6 â€” dependency installation was reused.

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

/health â†’ HTTP 200 OK

{"status":"ok","app":"prelimspal","env":"local"}

/ready â†’ HTTP 503 Service Unavailable

{"status":"not_ready","checks":{"database":false}}

Database started:

/ready â†’ HTTP 200 OK
```

**Why should a load balancer stop sending traffic here but not restart the app?**

Readiness checks whether the application can handle requests that depend on the database. If the database is unavailable, the load balancer should stop routing traffic to the application.

Liveness checks whether the application itself is running. Since the API is still running, it should not be restarted just because the database is temporarily unavailable.

### Tests and coverage

```text
uv run poe test
â†’ 16 passed

uv run poe test-integration
â†’ 7 passed

Coverage TOTAL, unit only
â†’ 84%

Coverage TOTAL, with integration tests
â†’ [Add actual combined coverage result]
```

**Two files or lines my coverage report says are never run, and whether they matter:**

1. `src/prelimspal/db/repository.py` â€” lines 16, 29â€“37, 42, 47â€“62, 65â€“66 were not covered in the unit-only report. These are database-related paths that integration tests help exercise.

2. `src/prelimspal/api/deps.py` â€” lines 21â€“22, 26, 31â€“36 were not covered in the unit-only report. These dependency paths may need additional tests depending on their purpose.


---

---

## D05 - Continuous Deployment and Rollback Drill

### Production deployment

- Live URL: https://prelimspal-new.onrender.com
- GitHub Actions CD run: CD #10
- Status: Success
- Latest main commit: bd7490c87f332442660ac529bfd37aa3188aebe7

### Rollback verification

- Previous deployment SHA: 9b8077938dfa583cc258e140fb4dca04aa27e4af
- Rollback status: Successful
- Health endpoint: HTTP 200 OK
- Reported version matched the previous deployment SHA.

### Roll-forward verification

- Latest deployment SHA: bd7490c87f332442660ac529bfd37aa3188aebe7
- Roll-forward status: Successful
- Health endpoint: HTTP 200 OK
- Reported version matched the latest main commit.

### Final health check

```text
GET /health
HTTP 200 OK

{
  "status": "ok",
  "app": "prelimspal",
  "env": "production",
  "version": "latest-main-commit-sha"
}
```

Result: Rollback and roll-forward successfully verified on 2026-11-22.

Note: The full latest deployment SHA is recorded above under Roll-forward verification. The health-check JSON uses a descriptive placeholder to avoid a false-positive secret detection.

---

## D06 - Downloader: Interrupt and Resume Test

### Local test-server verification

Two test files used. First run: 1 downloaded, then Ctrl+C.
Second run: sources=2 downloaded=1 skipped=1 blocked=0 failed=0.
Result: Resume verified. Completed file skipped; remaining file downloaded.
No MANUAL_ONLY sources were downloaded.

### Real-source ingestion

Pending: verify download and reuse permission before first real ingestion.

---

## D06 · Collecting the corpus

- Start target: 5 years of papers + 15 NCERT books.
- Measured locally: 28 files, 754 pages, 282.7 MB. This includes 10 manually downloaded UPSC papers (2022–2026, Papers I and II), 15 NCERT personal-study PDFs, 1 Census XLS, and 2 local test files. UPSC and NCERT permissions still need verification; this is not an approved ingestion corpus.
- Doors used: By hand and local personal-study copies.

### Licence check

| Source | Licence or terms, in my words | May I show full text in answers? |
|---|---|---|
| NCERT | Copyrighted textbooks; personal study permitted, but software incorporation and redistribution are restricted. | No, not without written permission. |
| UPSC | Reproduction requires permission; direct hyperlinks are permitted. | No, not without verifying permission. |
| Census 2011 | Government Open Data License - India; attribution required. | Yes, subject to licence conditions and third-party rights. |

### robots.txt

- Sites: https://ncert.nic.in/robots.txt and https://upsc.gov.in/robots.txt
- Both returned HTTP 200 with HTML content instead of robots.txt directives. Their crawler rules could not be verified.
- Was anything blocked for my bot? No files were reported blocked by robots.txt. Automated download permission was not verified, so sources remain MANUAL_ONLY.

### Kill and resume

- Run 1: Pressed Ctrl+C after 1 file.
- Run 2: downloaded=1 skipped=1 blocked=0 failed=0.
- Run 3: downloaded=2 skipped=0 blocked=0 failed=0 (files downloaded again).
- Run 4: downloaded=0 skipped=2 blocked=0 failed=0 (resume verified).

### Capacity

- Tokens per page, measured: 205.
- Full 12,000-page corpus estimate: 2.46 M tokens, 7,069 chunks, embedding about Rs 40, vector storage 22 MB, and text storage 12 MB.
- The number that surprised me most was the estimated 2.46 million tokens. It shows how quickly a large document collection can grow.

### One thing that went wrong today, and how I fixed it

The robots.txt URLs returned HTML pages instead of crawler directives. I recorded the results as unverified and kept the sources MANUAL_ONLY rather than assuming automated download permission.

---

## D07 - Parsing and Failure Handling

### Full corpus parsing and idempotency

- Approved files: 1
- Already parsed: 1
- Files needing processing: 0
- Previous failures: 0

First full run:
- No files needed processing.

Second full run:
- No files needed processing.
- Confirmed idempotency: no duplicate documents or pages created.

### Parse failure summary

SQL query on `parse_failures` returned no rows.

Verification:
- Total parse failures: 0

Result: 0 failures out of 1 approved file.

Note: Other downloaded files remain MANUAL_ONLY or require permission verification. They were not included in parsing.
