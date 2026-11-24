# Capacity plan: PrelimsPal

Full corpus target: 12 years of papers + 60 NCERT books (12,000+ pages)

<!-- generated:start -->
## Measured on my start corpus (2026-11-24 13:48 UTC)

| What | Value |
|---|---|
| Files | 28 |
| Size on disk | 282.7 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 754 |
| Characters of text | 617,969 |
| Estimated tokens (characters / 4) | 154,492 |
| Tokens per page | 205 |
| PDFs with almost no text (scanned? OCR is Day 7) | 9 |
| Files not measured (zip, xlsx, unreadable) | 1 |

## Estimate for the full corpus (target: 12,000 pages)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 15.9 |
| Tokens | measured tokens x scale | 2.46 M |
| Raw files | measured MB x scale | 4,499 MB |
| Chunks | tokens / 400 x 1.15 overlap | 7,069 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.42 = Rs 40 |
| Vector storage | chunks x 768 numbers x 4 bytes | 22 MB |
| Text in Postgres | characters x scale x 1.2 | 12 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->

## What I conclude

1. The estimated one-time embedding cost for the full 12,000-page corpus is $0.42 (approximately Rs 40), based on the current assumptions.

2. The estimated vector and text data require about 34 MB. My Neon free plan includes 1 GB of storage, and current usage is 39.99 MB. The estimated total is approximately 74 MB, which fits within the 1 GB limit. However, indexes and database overhead may increase actual storage usage.

3. The token and chunk estimates are least certain because they use assumptions. I will measure actual tokens and chunks after implementing document processing.

4. Storage, tokens, chunks and embedding cost will increase approximately 10 times if the corpus grows 10 times. I will review database capacity, batch embedding and optimize vector indexing and retrieval.
