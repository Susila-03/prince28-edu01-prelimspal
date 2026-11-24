
# PrelimsPal - Source Register

This document records the sources used by PrelimsPal for study material, questions, and reference content.

## 1. Official UPSC Sources

| Source | Content used | Format | Usage notes |
|---|---|---|---|
| UPSC official website - https://upsc.gov.in/ | Civil Services Examination notifications and previous-year question papers | PDF / Web | Use official documents and link to the original source. |
| UPSC Civil Services Examination syllabus | Prelims and Mains syllabus | PDF / Web | Refer to the official syllabus. Do not alter its meaning. |

## 2. NCERT Sources

| Source | Content used | Format | Usage notes |
|---|---|---|---|
| NCERT Class XI Geography - Chapter 4: Climate | Geography study reference | PDF | Copyrighted educational material. Use for personal study and provide proper attribution. Do not redistribute the full chapter. |

## 3. Other Reference Documents

| Source | Content used | Format | Usage notes |
|---|---|---|---|
| Indian Constitution - Chapter 2 | Constitution study reference | PDF | Verify the original publisher and source. Respect copyright and attribution requirements. |
| UPSC CSE 2026 Notification | Examination details and eligibility reference | PDF | Refer to the official UPSC notification and link to the original document. |

## 4. Source Management Rules

1. Prefer official government and educational sources.
2. Record the source title, publisher, URL, and access date.
3. Record page numbers when extracting information.
4. Clearly distinguish original source content from PrelimsPal summaries.
5. Do not upload or redistribute copyrighted books or documents without permission.
6. Check the licence or terms of use before reusing material.
7. Keep downloaded source PDFs in `data/sources/`.
8. Review source links periodically to ensure they remain valid.

## 5. Verification Status

- [ ] Verify the original URLs for all downloaded PDFs.
- [ ] Record publication details and access dates.
- [ ] Check the usage terms for each source.
- [ ] Confirm that no copyrighted material is redistributed without permission.

## 6. NCERT Website Verification (23 November 2026)

- Website: https://ncert.nic.in/
- robots.txt URL: https://ncert.nic.in/robots.txt
- HTTP status: 200
- Response content type: text/html; charset=utf-8
- Expected robots.txt directive (`User-agent:`): Not found.
- Verification result: robots.txt could not be verified because the URL returned an HTML webpage instead of robots.txt directives.
- Automated download permission: Not verified.
- Project decision: Keep NCERT documents marked `MANUAL_ONLY`.
- Copyright and reuse: Do not assume website ownership grants permission to redistribute or incorporate textbook content into software. Check applicable textbook terms and obtain permission where required.


## 7. NCERT Copyright and Textbook Terms

Official references:
- Website policies: https://www.ncert.nic.in/website-policies.php?ln=en
- Textbook copyright notice: https://ncert.nic.in/textbook.php
- Copyright infringement press release: https://www.ncert.nic.in/pdf/announcement/notices/Press_Release_Copyright_Infringement-NCERT.pdf

Findings:
- NCERT website material may be reproduced with proper acknowledgement, subject to third-party rights.
- NCERT textbooks may be downloaded for personal study or reference.
- Textbook republication, redistribution, and incorporation into software or digital content packages are prohibited under the published textbook terms.
- Written permission is required for linking to NCERT textbook downloads under those terms.
- Project decision: Do not automatically download or incorporate NCERT textbook PDFs into PrelimsPal. Keep NCERT rows MANUAL_ONLY and use permitted references or obtain written permission before reuse.


## 8. UPSC Website Verification (23 November 2026)

- Website: https://upsc.gov.in/
- robots.txt URL: https://upsc.gov.in/robots.txt
- HTTP status: 200
- Response content type: text/html; charset=utf-8
- Expected robots.txt directive (`User-agent:`): Not found.
- Verification result: robots.txt could not be verified because the URL returned an HTML webpage instead of robots.txt directives.
- Automated download permission: Not verified.
- Project decision: Keep UPSC documents marked `MANUAL_ONLY`.
- Copyright and reuse: Verify UPSC reproduction conditions and obtain required permission before reusing documents.

## 9. UPSC Copyright and Website Terms

Official reference:
- Website policies: https://upsc.gov.in/website-policies/

Findings:
- UPSC website material may be reproduced free of charge after obtaining proper permission.
- Reproduced material must be accurate and prominently acknowledge UPSC as the source.
- Third-party copyrighted material requires permission from its respective copyright holder.
- Direct hyperlinks to UPSC website content are permitted without prior permission.
- Website pages must not be displayed inside frames on another website.
- Project decision: Keep UPSC documents MANUAL_ONLY. Do not automatically download or incorporate UPSC documents into PrelimsPal without verifying permission and applicable terms.

## 10. IMD Website Verification (23 November 2026)

- Website: https://mausam.imd.gov.in/
- robots.txt URL: https://mausam.imd.gov.in/robots.txt
- HTTP status: 404 Not Found.
- Verification result: robots.txt file was not found at the requested URL.
- Automated download permission: Not verified.
- Project decision: Keep IMD documents marked MANUAL_ONLY.
- Copyright and reuse: Verify IMD document-specific reuse conditions and obtain permission where required.

## 11. IMD Copyright and Reuse Terms

Official references:
- IMD website disclaimer: https://mausam.imd.gov.in/responsive/disclaimer.php
- IMD Data Service Portal: https://dsp.imdpune.gov.in/home_freedataaccess.php

Findings:
- The main website disclaimer does not provide general permission to reproduce IMD documents.
- IMD publications may carry individual copyright notices. Check each document separately.
- The IMD Data Service Portal states that commercial reproduction requires permission from the competent authority.
- Automated download and software reuse permission for the selected IMD PDFs: Not verified.
- Project decision: Keep IMD rows MANUAL_ONLY. Obtain applicable permission before incorporating IMD documents or their content into PrelimsPal.

## 12. India Budget Website Verification (23 November 2026)

- Website: https://www.indiabudget.gov.in/
- robots.txt URL: https://www.indiabudget.gov.in/robots.txt
- HTTP status: 404 Not Found.
- Verification result: robots.txt file was not found at the requested URL.
- Automated download permission: Not verified.
- Project decision: Keep India Budget documents marked MANUAL_ONLY.
- Copyright and reuse: Verify the Economic Survey document-specific copyright and reuse conditions before incorporating content into PrelimsPal.

## 13. India Budget Copyright and Reuse Terms

Official references:
- Website copyright policy: https://www.indiabudget.gov.in/website-policies.php
- Economic Survey terms of use: https://www.indiabudget.gov.in/economicsurvey/termsofuse.php

Findings:
- India Budget website content must not be reproduced partially or fully without due permission from the Ministry of Finance.
- If content is referred to in another publication, the source must be appropriately acknowledged.
- Direct links to information hosted on the India Budget website are permitted without prior permission.
- Copyrighted material on linked external websites requires permission from its respective owner.
- Automated download and software reuse permission for the selected Economic Survey PDF: Not verified.
- Project decision: Keep India Budget rows MANUAL_ONLY. Obtain permission before incorporating its documents or content into PrelimsPal.

## 14. NCERT Document URL Verification (23 November 2026)

Verification method: HTTP GET using PowerShell Invoke-WebRequest. Documents were inspected in memory and not saved.

| Document URL | HTTP status | Content-Type | Result |
|---|---:|---|---|
| kegy104.pdf | 200 | application/pdf | PDF confirmed |
| keps202.pdf | 200 | application/pdf | PDF confirmed |
| keps201.pdf | 200 | application/pdf | PDF confirmed |
| lehs104.pdf | 200 | application/pdf | PDF confirmed |
| lehs101.pdf | 200 | application/pdf | PDF confirmed |
| keec103.pdf | 200 | application/pdf | PDF confirmed |

- PDF signature checked: %PDF-
- Result: All six URLs returned PDF documents.
- Copyright decision: URL availability does not grant software reuse permission. Keep all NCERT rows MANUAL_ONLY.
