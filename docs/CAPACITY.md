# Capacity plan: PrelimsPal

Full corpus target: 12 years of papers + 60 NCERT books (12,000+ pages)

<!-- generated:start -->
## Measured on my start corpus (2026-11-24 12:14 UTC)

| What | Value |
|---|---|
| Files | 16 |
| Size on disk | 39.7 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 186 |
| Characters of text | 281,489 |
| Estimated tokens (characters / 4) | 70,372 |
| Tokens per page | 378 |
| PDFs with almost no text (scanned? OCR is Day 7) | 0 |
| Files not measured (zip, xlsx, unreadable) | 1 |

## Estimate for the full corpus (target: 12,000 pages)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 64.5 |
| Tokens | measured tokens x scale | 4.54 M |
| Raw files | measured MB x scale | 2,562 MB |
| Chunks | tokens / 400 x 1.15 overlap | 13,053 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.78 = Rs 74 |
| Vector storage | chunks x 768 numbers x 4 bytes | 40 MB |
| Text in Postgres | characters x scale x 1.2 | 22 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->

## What I conclude

1. No. The estimated one-time embedding cost for the full corpus is only $0.78 (approximately ₹74).
2. The estimated vector and text data require about 62 MB.
My Neon free plan includes 1 GB of storage, and current usage is
39.99 MB. The estimated total is approximately 102 MB, which fits
within the 1 GB limit. However, indexes and database overhead
may increase actual storage usage.
3. The token and chunk estimates are least certain because they use assumptions. I will measure actual tokens and chunks after implementing document processing.
4. Storage, tokens, chunks and embedding cost will increase approximately 10 times if the corpus grows 10 times.
   I will review database capacity, batch embedding and optimize vector indexing and retrieval.
