#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
chapterize.py — Auto-extract chapter structure and non-notation pages from a PDF.

Usage:
  python docs/chapterize.py <pdf_path> <slug>
  python docs/chapterize.py --all          # Process all PDFs in docs/

Outputs:
  - Updates docs/chapter-index.json  (chapter map per slug)
  - Updates docs/page-index.json     (notation-only page list per slug)

Scanned PDFs (no text layer) are detected automatically and flagged —
they cannot be auto-chapterized but are recorded with scanned: true.
"""

import sys
import json
import re
import fitz  # PyMuPDF
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CHAPTER_INDEX = REPO_ROOT / "docs" / "chapter-index.json"
PAGE_INDEX = REPO_ROOT / "docs" / "page-index.json"

# PDFs to process when using --all
ALL_BOOKS = {
    # slug: (pdf_path, book_type)
    # book_type: "method"       — chapter titles have description paragraphs (require_description=True)
    # book_type: "transcription" — chapter titles are song names repeating across pages (dedup approach)
    "master-studies-morello":             ("docs/Master Studies - Joe Morello.pdf",                            "method"),
    "double-bass-freedom":                ("docs/Double Bass Freedom - Virgil Donati.pdf",                     "method"),
    "stick-control":                      ("docs/Stick Control - George Lawrence Stone.pdf",                   "method"),
    "the-art-of-bop-drumming":            ("docs/The Art of Bop Drumming - John Riley.pdf",                   "method"),
    "advanced-techniques-modern-drummer": ("docs/Advanced Techniques for the Modern Drummer - Jim Chapin.pdf", "method"),
    "advanced-funk-studies":              ("docs/Advanced Funk Studies - Rick Latham.pdf",                     "method"),
    "progressive-steps-syncopation":      ("docs/Progressive Steps to Syncopation - Ted Reed.pdf",             "method"),
    "progressive-independence-rock":      ("docs/Progressive Independence Rock - Ron Spagnardi.pdf",           "method"),
    "abr-messengers-drums":               ("docs/transcriptions/August Burns Red - Messengers Drums.pdf",      "transcription"),
    "better-lovers-highly-irresponsible": ("docs/transcriptions/Better Lovers - Highly Irresponsible.pdf",    "transcription"),
}

# --- Tuneable thresholds ---
SCANNED_THRESHOLD = 0.15      # If < 15% of pages have text -> scanned
MIN_TEXT_CHARS = 20           # Minimum chars on a page to count as "has text"
HEADING_MAX_CHARS = 80        # A heading line is short
HEADING_MIN_ALPHA = 0.6       # Mostly letters (not exercise numbers like "16 > 1-:r-J")
NON_NOTATION_WORD_COUNT = 120  # Pages with > N words are likely text-only (intros, bios)
                               # Must be high — notation pages have stickings (R L R L...) and labels


def load_json(path: Path) -> dict:
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ok Saved {path.relative_to(REPO_ROOT)}")


def get_page_text(page) -> str:
    return page.get_text().strip()


def meaningful_lines(text: str) -> list[str]:
    return [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 2]


def is_scanned(doc) -> tuple[bool, float]:
    """Return (is_scanned, text_coverage_ratio)."""
    pages_with_text = sum(
        1 for i in range(len(doc))
        if len(get_page_text(doc[i])) >= MIN_TEXT_CHARS
    )
    ratio = pages_with_text / len(doc) if len(doc) > 0 else 0
    return ratio < SCANNED_THRESHOLD, ratio


def is_likely_heading(line: str) -> bool:
    """Heuristic: is this line a chapter heading rather than exercise notation?"""
    if not line or len(line) > HEADING_MAX_CHARS:
        return False
    alpha_ratio = sum(c.isalpha() or c == " " for c in line) / len(line)
    if alpha_ratio < HEADING_MIN_ALPHA:
        return False
    # Must have at least 3 actual words
    words = [w for w in line.split() if any(c.isalpha() for c in w)]
    return len(words) >= 2


def detect_running_headers(doc) -> set[str]:
    """
    Find strings that appear as the first line on many pages — these are
    running headers, watermarks, or repeated author names (e.g. 'VIRGIL DONATI',
    'www.drumnet.ru', 'BETTER LOVERS'). Strip them before chapter analysis.
    Returns a set of normalised strings to ignore.
    """
    from collections import Counter
    first_lines = []
    for i in range(len(doc)):
        lines = meaningful_lines(get_page_text(doc[i]))
        if lines:
            first_lines.append(lines[0].strip().lower())

    total = len(first_lines)
    counts = Counter(first_lines)
    # Flag anything appearing on more than 30% of pages
    return {text for text, count in counts.items() if count / total > 0.30}


def extract_chapters(doc, book_type: str = "method") -> list[dict]:
    """
    Detect chapter start pages. Strategy differs by book type:

    "method"       — method books (Morello, Donati): require a description paragraph
                     after the heading to filter out notation lines picked up as headings.

    "transcription" — song transcriptions (ABR, Better Lovers): chapter titles (song names)
                     repeat across every page of that song. Dedup consecutive equal headings;
                     no description requirement.
    """
    running_headers = detect_running_headers(doc)
    candidates = []
    require_description = (book_type == "method")

    for i in range(len(doc)):
        text = get_page_text(doc[i])
        lines = meaningful_lines(text)
        if not lines:
            continue

        # Strip running headers from the top
        filtered = [l for l in lines if l.strip().lower() not in running_headers]
        if not filtered:
            continue

        first = filtered[0]
        first_clean = re.sub(r"^[^a-zA-Z]+", "", first).strip()

        if not is_likely_heading(first_clean):
            continue

        has_description = len(filtered) > 1 and len(filtered[1]) > 30

        if require_description and not has_description:
            continue  # Method books: skip headings without prose description

        candidates.append({
            "page": i + 1,
            "heading": first_clean,
            "has_description": has_description,
        })

    if not candidates:
        return []

    # Deduplicate: consecutive pages with the same heading = continuation, not a new chapter
    deduped = [candidates[0]]
    for c in candidates[1:]:
        if c["heading"].lower() != deduped[-1]["heading"].lower():
            deduped.append(c)

    # Build chapter ranges
    chapters = []
    for idx, c in enumerate(deduped):
        end = (deduped[idx + 1]["page"] - 1) if idx + 1 < len(deduped) else len(doc)
        chapters.append({
            "title": c["heading"],
            "start": c["page"],
            "end": end,
        })

    return chapters


def extract_notation_pages(doc) -> list[int]:
    """
    Return list of page numbers (1-indexed) that are likely music notation.
    Strips running headers before word-count analysis so watermarked PDFs
    aren't incorrectly classified as text-heavy.
    """
    running_headers = detect_running_headers(doc)
    notation_pages = []

    for i in range(len(doc)):
        page = doc[i]
        raw_text = get_page_text(page)
        # Remove running header lines before counting words
        lines = raw_text.split("\n")
        filtered_lines = [l for l in lines if l.strip().lower() not in running_headers]
        text = "\n".join(filtered_lines).strip()
        words = len(text.split())

        # Check image coverage — pages that are mostly large images are likely photos
        image_list = page.get_images(full=True)
        has_large_image = False
        for img in image_list:
            # xref, smask, width, height, bpc, colorspace, alt. colorspace, name, filter, referencer
            try:
                width = img[2]
                height = img[3]
                # Large images (covering most of a typical page) are likely photos/artwork
                if width > 400 and height > 400:
                    has_large_image = True
                    break
            except (IndexError, TypeError):
                pass

        # Classification:
        if words > NON_NOTATION_WORD_COUNT and not has_large_image:
            # Text-heavy with no big image = intro/bio/preface
            continue
        elif has_large_image and words < 10:
            # Mostly image, almost no text = photo page
            continue
        else:
            # Notation page (has musical content — either pure notation or notation + labels)
            notation_pages.append(i + 1)

    return notation_pages


def process_pdf(pdf_path: Path, slug: str, chapter_index: dict, page_index: dict, book_type: str = "method"):
    if not pdf_path.exists():
        print(f"  ! PDF not found: {pdf_path} — skipping")
        chapter_index[slug] = {
            "_note": f"PDF not found at {pdf_path}. Run git lfs pull first.",
            "scanned": None,
            "chapters": []
        }
        return

    print(f"\nProcessing: {slug}")
    print(f"  PDF: {pdf_path.relative_to(REPO_ROOT)}")

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    print(f"  Pages: {total_pages}")

    scanned, text_ratio = is_scanned(doc)
    print(f"  Text coverage: {text_ratio:.0%} of pages have text -> {'SCANNED' if scanned else 'text layer present'}")

    if scanned:
        chapter_index[slug] = {
            "_note": (
                f"Scanned PDF — no text layer detected ({text_ratio:.0%} pages have text). "
                "Cannot auto-chapterize. Add chapters manually or via OCR."
            ),
            "scanned": True,
            "auto_indexed": False,
            "text_coverage": round(text_ratio, 3),
            "chapters": chapter_index.get(slug, {}).get("chapters", []),  # preserve any manual entries
        }
        print(f"  ! Flagged as scanned — chapters NOT extracted")

        # For scanned books, page-index = all pages (no text to detect non-notation)
        if slug not in page_index:
            page_index[slug] = list(range(1, total_pages + 1))
            print(f"  Page index: set to all {total_pages} pages (cannot detect photo pages in scanned PDF)")
        else:
            print(f"  Page index: keeping existing manual entries")

    else:
        # Extract chapters
        chapters = extract_chapters(doc, book_type=book_type)
        print(f"  Chapters detected: {len(chapters)}")
        for ch in chapters:
            print(f"    p.{ch['start']:3d}–{ch['end']:3d}: {ch['title']}")

        # Extract notation pages
        notation_pages = extract_notation_pages(doc)
        non_notation = [p for p in range(1, total_pages + 1) if p not in notation_pages]
        print(f"  Notation pages: {len(notation_pages)} / {total_pages}")
        if non_notation:
            print(f"  Excluded (non-notation): pages {non_notation}")

        chapter_index[slug] = {
            "scanned": False,
            "auto_indexed": True,
            "text_coverage": round(text_ratio, 3),
            "chapters": chapters,
        }
        # Safety: if auto-detection yields 0 notation pages for a non-scanned book,
        # something went wrong (likely a watermarked PDF where even stripping headers
        # leaves too much text). Fall back to all pages and flag it.
        if len(notation_pages) == 0 and total_pages > 5:
            print(f"  ! WARNING: 0 notation pages detected — falling back to all {total_pages} pages.")
            print(f"    This book may have watermarks or unusual text density. Review manually.")
            chapter_index[slug]["_notation_warning"] = (
                "Auto-detection yielded 0 notation pages — fell back to all pages. "
                "Likely a watermarked or unusual PDF. Review and edit page-index manually if needed."
            )
            notation_pages = list(range(1, total_pages + 1))

        page_index[slug] = notation_pages

    doc.close()


def main():
    args = sys.argv[1:]

    chapter_index = load_json(CHAPTER_INDEX)
    page_index = load_json(PAGE_INDEX)

    if "--all" in args:
        print("Processing all known books...\n")
        for slug, (rel_path, book_type) in ALL_BOOKS.items():
            pdf_path = REPO_ROOT / rel_path
            process_pdf(pdf_path, slug, chapter_index, page_index, book_type=book_type)
    elif len(args) >= 2:
        pdf_path = Path(args[0])
        slug = args[1]
        book_type = args[2] if len(args) >= 3 else "method"
        process_pdf(pdf_path, slug, chapter_index, page_index, book_type=book_type)
    else:
        print("Usage:")
        print("  python docs/chapterize.py <pdf_path> <slug>")
        print("  python docs/chapterize.py --all")
        sys.exit(1)

    save_json(CHAPTER_INDEX, chapter_index)
    save_json(PAGE_INDEX, page_index)
    print("\nDone.")


if __name__ == "__main__":
    main()
