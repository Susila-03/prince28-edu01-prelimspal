
## Idempotent Loader Test Results

Command:
`uv run python scripts/load_db.py`

### Test 1: First run
records=5 inserted=5 updated=0 unchanged=0

### Test 2: Second run
records=5 inserted=0 updated=0 unchanged=5

### Test 3: Modified one record
records=5 inserted=0 updated=1 unchanged=4

### Result
- New records are inserted.
- Unchanged records are skipped.
- Modified records are updated using SHA-256 fingerprints.

All three tests passed successfully.
