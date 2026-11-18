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
