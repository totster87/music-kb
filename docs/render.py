#!/usr/bin/env python3
"""
render.py — Render a PDF to per-page PNGs and update page-index.json.

Usage:
  python docs/render.py <pdf_path> <slug>
  python docs/render.py "docs/Evolution of Blast Beats - Derek Roddy.pdf" evolution-of-blast-beats

  # Render only specific pages:
  python docs/render.py <pdf_path> <slug> --pages 1-50
  python docs/render.py <pdf_path> <slug> --pages 10,15,22

After running:
  git lfs track "docs/rendered/<slug>/*.png"   # if new slug
  git add docs/rendered/<slug>/ docs/.gitattributes docs/page-index.json
  git commit -m "Render <slug>"
  git push

Then say "chapterize <slug>" in Claude to extract chapter structure.
"""

import sys
import json
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
RENDERED = REPO_ROOT / "docs" / "rendered"
PAGE_INDEX = REPO_ROOT / "docs" / "page-index.json"

DPI = 150  # Good balance of quality vs file size for iPhone viewing


def parse_pages(spec: str, total: int) -> list[int]:
    """Parse a page spec like '1-50' or '10,15,22' into a list of 1-indexed page numbers."""
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a), int(b) + 1))
        else:
            pages.add(int(part))
    return sorted(p for p in pages if 1 <= p <= total)


def render_pdf(pdf_path: Path, slug: str, page_filter: list[int] | None = None):
    out_dir = RENDERED / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    total = len(doc)
    targets = page_filter if page_filter else list(range(1, total + 1))

    print(f"  PDF: {pdf_path.name}  ({total} pages total)")
    print(f"  Slug: {slug}")
    print(f"  Output: {out_dir.relative_to(REPO_ROOT)}")
    print(f"  Rendering {len(targets)} page(s) at {DPI} dpi...")
    print()

    rendered = []
    mat = fitz.Matrix(DPI / 72, DPI / 72)

    for page_num in targets:
        page = doc[page_num - 1]
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        out_path = out_dir / f"page-{page_num:03d}.png"
        pix.save(str(out_path))
        rendered.append(page_num)
        print(f"  [{page_num:3d}/{total}] {out_path.name}")

    doc.close()

    # Update page-index.json
    index = {}
    if PAGE_INDEX.exists():
        with open(PAGE_INDEX) as f:
            index = json.load(f)

    existing = set(index.get(slug, []))
    existing.update(rendered)
    index[slug] = sorted(existing)

    with open(PAGE_INDEX, "w") as f:
        json.dump(index, f, indent=2)

    print()
    print(f"  ok Rendered {len(rendered)} pages")
    print(f"  ok Updated page-index.json ({len(index[slug])} total pages for {slug})")
    print()
    print("Next steps:")
    print(f'  git lfs track "docs/rendered/{slug}/*.png"')
    print(f"  git add docs/rendered/{slug}/ docs/.gitattributes docs/page-index.json")
    print(f'  git commit -m "Render {slug} ({len(rendered)} pages)"')
    print("  git push")
    print()
    print("Then chapterize:")
    print(f"  python docs/chapterize.py <pdf_path> {slug}")


def main():
    parser = argparse.ArgumentParser(description="Render PDF pages to PNGs")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("slug", help="Book slug (e.g. evolution-of-blast-beats)")
    parser.add_argument("--pages", help="Page range or list, e.g. '1-50' or '5,10,15'", default=None)
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)

    page_filter = None
    if args.pages:
        doc = fitz.open(str(pdf_path))
        total = len(doc)
        doc.close()
        page_filter = parse_pages(args.pages, total)
        print(f"  Filtering to {len(page_filter)} pages: {args.pages}")

    render_pdf(pdf_path, args.slug, page_filter)


if __name__ == "__main__":
    main()
