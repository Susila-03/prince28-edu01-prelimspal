from pathlib import Path

import pymupdf

out = Path("data/samples/parser_comparison/hard_cases")

# Repair PDF 1: keep repeated headers and footers,
# but make the body content different on every page.
doc = pymupdf.open()

for number in range(1, 5):
    page = doc.new_page()
    page.insert_text((50, 35), "SYNTHETIC RESEARCH REPORT", fontsize=9)
    page.insert_text((50, 85), f"Section {number}: Sample Topic", fontsize=18)

    for paragraph in range(1, 5):
        text = (
            f"Page {number}, paragraph {paragraph}: "
            f"This unique synthetic passage tests text extraction, "
            f"page handling, repeated headers, and footer removal. "
            f"The observations for section {number} are different."
        )
        page.insert_text(
            (50, 125 + paragraph * 35),
            text,
            fontsize=10,
        )

    page.insert_text((50, 780), f"Page {number} of 4", fontsize=9)

doc.save(out / "hard_01_multipage_headers.pdf")
doc.close()


# Repair HTML 9: use varied paragraphs to avoid duplicate-text removal.
paragraphs = []
for section in range(1, 4):
    for number in range(1, 9):
        paragraphs.append(
            f"<p>Section {section}, paragraph {number}: "
            f"This synthetic passage examines document extraction, "
            f"heading structure, page splitting, and text quality. "
            f"Each paragraph contains different content for reliable "
            f"parser comparison. Measurement group {section * 100 + number}.</p>"
        )

html = (
    "<!DOCTYPE html><html><head><title>Long Synthetic Article</title>"
    "</head><body><article><h1>Long Document Testing</h1>"
    "<h2>Section One</h2>"
    + "".join(paragraphs[:8])
    + "<h2>Section Two</h2><h3>Subsection A</h3>"
    + "".join(paragraphs[8:16])
    + "<h2>Section Three</h2>"
    + "".join(paragraphs[16:])
    + "</article></body></html>"
)

(out / "hard_09_long_sections.html").write_text(html, encoding="utf-8")

print("Repaired PDF 1 and HTML 9.")
