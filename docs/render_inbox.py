#!/usr/bin/env python3
"""
Render inbox PDFs to per-page PNGs using PyMuPDF (fitz).
Cross-platform (Windows/Mac/Linux). No poppler dependency.

Setup (one time):
    pip install pymupdf

Run from repo root:
    python docs/render_inbox.py
"""
import os
import sys
import subprocess

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(REPO, "docs", "inbox")
RENDERED = os.path.join(REPO, "docs", "rendered")

SLUG_MAP = {
    "331734875-Jungle-Drum-n-Bass-pdf.pdf":                   "jungle-drum-n-bass",
    "481222696-Rod-Morgenstein-Drum-Set-Warm-Ups.pdf":         "rod-morgenstein-drum-set-warm-ups",
    "673871533-120-Right-Hand-Studies-by-Mauro-Giuliani.pdf":  "120-right-hand-studies-giuliani",
    "927941105-Scale-Studies-for-Jazz-Guitar-Rick-Stone.pdf":  "scale-studies-jazz-guitar-stone",
    "converge-axe to fall.pdf":                                "converge-axe-to-fall",
    "converge-concubine.pdf":                                  "converge-concubine",
    "converge-dark horse.pdf":                                 "converge-dark-horse",
    "converge-drop out.pdf":                                   "converge-drop-out",
    "converge-first light.pdf":                                "converge-first-light",
    "converge-hum of hurt.pdf":                                "converge-hum-of-hurt",
    "converge-to feel something.pdf":                          "converge-to-feel-something",
    "converge-under duress.pdf":                               "converge-under-duress",
    "converge-versus.pdf":                                     "converge-versus",
    "converge-worms will feed.pdf":                            "converge-worms-will-feed",
    "steve-vai-10-hour-guitar-workout.pdf":                    "vai-10-hour-workout",
}

DPI = 150
ZOOM = DPI / 72  # PDF default is 72 DPI

results = {}

for fname, slug in SLUG_MAP.items():
    pdf_path = os.path.join(INBOX, fname)
    out_dir = os.path.join(RENDERED, slug)

    if not os.path.exists(pdf_path):
        print(f"SKIP (not found): {fname}")
        continue

    size = os.path.getsize(pdf_path)
    if size < 500:
        print(f"SKIP (LFS pointer — run 'git lfs pull' first): {fname}")
        continue

    # Skip if already rendered (any page-*.png in output dir).
    # Delete the output dir or pass --force to re-render.
    if os.path.isdir(out_dir):
        existing = [f for f in os.listdir(out_dir) if f.startswith("page-") and f.endswith(".png")]
        if existing and "--force" not in sys.argv:
            print(f"SKIP (already rendered, {len(existing)} pages): {slug}")
            continue

    print(f"\n{fname}")
    print(f"  → {slug} ({size // 1024} KB)")
    os.makedirs(out_dir, exist_ok=True)

    # Track in LFS
    try:
        subprocess.run(
            ["git", "lfs", "track", f"docs/rendered/{slug}/*.png"],
            cwd=REPO, capture_output=True, check=False
        )
    except Exception:
        pass

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"  FAILED to open: {e}")
        results[slug] = (0, 0)
        continue

    total = len(doc)
    print(f"  pages: {total}")
    matrix = fitz.Matrix(ZOOM, ZOOM)

    success = 0
    failed = []
    for i in range(total):
        try:
            page = doc[i]
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            out_path = os.path.join(out_dir, f"page-{i+1:03d}.png")
            pix.save(out_path)
            success += 1
        except Exception as e:
            failed.append(i + 1)
            print(f"    page {i+1} failed: {e}")

    doc.close()
    print(f"  rendered: {success}/{total}")
    if failed:
        print(f"  failed pages: {failed}")
    results[slug] = (success, total)

print("\n" + "=" * 50)
print("Summary:")
for slug, (success, total) in results.items():
    status = "OK" if success == total else f"PARTIAL ({success}/{total})" if success > 0 else "FAILED"
    print(f"  [{status}] {slug}")

print("\nNow run:")
print("  git add docs/rendered/ .gitattributes")
print("  git commit -m 'Render inbox PDFs to pages'")
print("  git push")
