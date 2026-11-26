from pathlib import Path

import pymupdf

OUT = Path("data/samples/parser_comparison/hard_cases")
OUT.mkdir(parents=True, exist_ok=True)


def create_pdf(name, pages, encrypted=False):
    doc = pymupdf.open()

    for content in pages:
        page = doc.new_page()
        for item in content:
            text, x, y, size = item
            page.insert_text((x, y), text, fontsize=size)

    path = OUT / name

    if encrypted:
        doc.save(
            path,
            encryption=pymupdf.PDF_ENCRYPT_AES_256,
            owner_pw="owner-password",
            user_pw="test-password",
        )
    else:
        doc.save(path)

    doc.close()
    print("Created", path)


# PDF 1: repeated headers and footers across four pages
pages = []
for number in range(1, 5):
    pages.append(
        [
            ("SYNTHETIC RESEARCH REPORT", 50, 35, 9),
            (f"Section {number}: Sample Topic", 50, 90, 18),
            (
                "This page contains synthetic research text for parser testing. "
                "It includes enough content to test extraction and page handling.",
                50,
                125,
                10,
            ),
            (f"Page {number} of 4", 50, 780, 9),
        ]
    )
create_pdf("hard_01_multipage_headers.pdf", pages)


# PDF 2: ruled table
doc = pymupdf.open()
page = doc.new_page()
page.insert_text((50, 55), "Synthetic Data Table", fontsize=18)

x_positions = [50, 190, 330, 470]
y_positions = [90, 130, 170, 210, 250]

for x in x_positions:
    page.draw_line((x, 90), (x, 250), color=(0, 0, 0))
for y in y_positions:
    page.draw_line((50, y), (470, y), color=(0, 0, 0))

cells = [
    ["Region", "Year", "Rainfall"],
    ["North", "2022", "120 mm"],
    ["South", "2023", "150 mm"],
    ["East", "2024", "135 mm"],
]
for row_index, row in enumerate(cells):
    for col_index, value in enumerate(row):
        page.insert_text(
            (x_positions[col_index] + 8, y_positions[row_index] + 25),
            value,
            fontsize=10,
        )

page.insert_text(
    (50, 290),
    "This synthetic table is included to compare table extraction between parsers.",
    fontsize=10,
)
doc.save(OUT / "hard_02_ruled_table.pdf")
doc.close()
print("Created hard_02_ruled_table.pdf")


# PDF 3: Unicode and different heading sizes
create_pdf(
    "hard_03_unicode_headings.pdf",
    [
        [
            ("Unicode and Formatting Test", 50, 70, 20),
            ("Caf\u00e9 - r\u00e9sum\u00e9", 50, 110, 15),
            (
                "This synthetic document tests Unicode characters, accented words, "
                "ligature-like text, and font-size-based heading detection.",
                50,
                150,
                10,
            ),
            ("Second Topic", 50, 210, 15),
            (
                "Another paragraph provides enough text for the parser to process "
                "this page and identify its heading structure.",
                50,
                245,
                10,
            ),
        ]
    ],
)


# PDF 4: two-column layout
create_pdf(
    "hard_04_two_columns.pdf",
    [
        [
            ("Two Column Layout", 50, 60, 18),
            ("LEFT COLUMN", 50, 100, 12),
            (
                "Left column text contains synthetic information about rainfall, "
                "population, geography, and regional measurements.",
                50,
                130,
                10,
            ),
            (
                "Additional left column content helps test reading order and "
                "text extraction from multiple blocks.",
                50,
                165,
                10,
            ),
            ("RIGHT COLUMN", 330, 100, 12),
            (
                "Right column text contains separate synthetic information about "
                "temperature, climate, environment, and observations.",
                330,
                130,
                10,
            ),
            (
                "Additional right column content helps compare how parsers "
                "handle multiple text columns.",
                330,
                165,
                10,
            ),
        ]
    ],
)


# PDF 5: encrypted PDF for error-handling tests
create_pdf(
    "hard_05_encrypted.pdf",
    [
        [
            ("Encrypted Synthetic Document", 50, 80, 18),
            (
                "This document is encrypted intentionally to test parser "
                "error handling. It contains synthetic text only.",
                50,
                120,
                10,
            ),
        ]
    ],
    encrypted=True,
)


# HTML 6: article with navigation, footer, scripts, and styles
html_6 = """<!DOCTYPE html>
<html>
<head>
<title>Synthetic Article With Noise</title>
<style>.banner { color: red; }</style>
<script>var trackingCode = "ignore this";</script>
</head>
<body>
<nav>Home | About | Contact | Menu</nav>
<div class="banner">Advertisement and promotional content</div>
<main>
<article>
<h1>Understanding Synthetic Data</h1>
<p>This article contains synthetic information for testing clean article extraction.</p>
<h2>Introduction</h2>
<p>Structured content helps evaluate how extraction tools
distinguish useful text from page clutter.</p>
<p>The content is generated locally and does not reproduce any published article.</p>
</article>
</main>
<footer>Copyright notice | Privacy | Terms</footer>
</body>
</html>"""
(OUT / "hard_06_article_noise.html").write_text(html_6, encoding="utf-8")


# HTML 7: table-heavy content
html_7 = """<!DOCTYPE html>
<html>
<head><title>Synthetic Table Test</title></head>
<body>
<article>
<h1>Regional Measurements</h1>
<p>This synthetic page contains a table with headers and multiple data rows.</p>
<table>
<thead><tr><th>Region</th><th>Year</th><th>Rainfall</th></tr></thead>
<tbody>
<tr><td>North</td><td>2022</td><td>120 mm</td></tr>
<tr><td>South</td><td>2023</td><td>150 mm</td></tr>
<tr><td>East</td><td>2024</td><td>135 mm</td></tr>
<tr><td>West</td><td>2025</td><td>160 mm</td></tr>
</tbody>
</table>
<p>The table is followed by explanatory synthetic text for comparison.</p>
</article>
</body>
</html>"""
(OUT / "hard_07_complex_table.html").write_text(html_7, encoding="utf-8")


# HTML 8: imperfect nesting and encoded characters
html_8 = """<!DOCTYPE html>
<html>
<head><title>Malformed Synthetic HTML</title></head>
<body>
<article>
<h1>HTML Recovery Test
<p>This paragraph tests recovery from imperfect HTML nesting.
<p>Entities include &amp;, &lt;, &gt;, and caf&eacute;.
<div><p>Nested content contains synthetic information about parsing and document structure.</div>
<p>Additional text ensures the page has enough meaningful content for extraction.
</article>
</body>
</html>"""
(OUT / "hard_08_malformed_nested.html").write_text(html_8, encoding="utf-8")


# HTML 9: long article with sections, lists, and links
paragraph = (
    "This is a synthetic paragraph created to test long-document extraction, "
    "section boundaries, text splitting, and consistent parser output. "
)

long_parts = [
    "<!DOCTYPE html><html><head><title>Long Synthetic Article</title></head><body>",
    "<article><h1>Long Document Testing</h1>",
    "<h2>Section One</h2>",
]
long_parts.extend(f"<p>{paragraph * 3}</p>" for _ in range(8))
long_parts.append("<h2>Section Two</h2><h3>Subsection A</h3>")
long_parts.extend(f"<p>{paragraph * 3}</p>" for _ in range(8))
long_parts.append(
    "<ul><li>First synthetic item</li><li>Second synthetic item</li>"
    "<li>Third synthetic item</li></ul>"
)
long_parts.append('<p><a href="https://example.com">Synthetic example link</a></p>')
long_parts.append("</article></body></html>")
(OUT / "hard_09_long_sections.html").write_text("\n".join(long_parts), encoding="utf-8")


# HTML 10: repeated clutter and hidden content
html_10 = """<!DOCTYPE html>
<html>
<head>
<title>Synthetic Clutter Test</title>
<style>.hidden { display: none; }</style>
<script>console.log("synthetic tracking script");</script>
</head>
<body>
<header>Repeated site header | Home | Search | Account</header>
<nav>Home | Topics | Reports | Help</nav>
<div>Advertisement | Subscribe | Special offer</div>
<article>
<h1>Environmental Observations</h1>
<p>This synthetic article discusses observations about temperature and air quality.</p>
<h2>Observations</h2>
<p>Measurements are collected at different times to understand changes in the environment.</p>
<p>Researchers can compare observations across rooms and identify unusual patterns.</p>
<p>This content is fictional and exists only for parser testing.</p>
</article>
<div class="hidden">Hidden synthetic content should not appear in clean extraction.</div>
<aside>Related links | Popular articles | More advertisements</aside>
<footer>Repeated site footer | Privacy | Terms | Contact</footer>
</body>
</html>"""
(OUT / "hard_10_script_noise.html").write_text(html_10, encoding="utf-8")


print("\nFinished creating 10 synthetic hard-case samples.")
