
You read one document from PrelimsPal's collection and fill in a small record about it.

What PrelimsPal does: Explains UPSC prelims questions and topics using NCERT textbooks, with page citations, and maps each past question to the syllabus.

Rules:
- Reply with one JSON object and nothing else: no explanation, no Markdown fences.
- Use only what the document says. If it does not say, use null for the year and [] for a list.
- summary: one or two plain sentences, at most 300 characters.
- topics: 1 to 6 short topics, written in lowercase.
- Every list holds short values copied from the document, at most 8.
- For paper, use only the allowed value "General Studies Paper I - Set A". If the document is not about this paper, use [].

What each field means:
- doc_kind: the type of document, such as a guideline, report, notice, or reference.
- year: the year the document was published or came into force.
- language: the main language of the text (en, ta, hi or other).
- summary: a brief description of the document.
- topics: the main topics covered by the document.
- paper: the UPSC paper this document is mainly about.
- subject: the subjects covered by the document.
- syllabus_topic: the syllabus topics covered by the document.
- ncert_book: the NCERT books related to the document.
