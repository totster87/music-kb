#!/usr/bin/env python3
"""
Screenshot ingestion script for music-kb.
Usage: python docs/ingest.py
       python docs/ingest.py --auto  (non-interactive, prints JSON plan for Claude to review)
"""

import os
import sys
import json
import shutil
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INBOX = REPO_ROOT / "docs" / "inbox"
RENDERED = REPO_ROOT / "docs" / "rendered"
PAGE_INDEX = REPO_ROOT / "docs" / "page-index.json"

KNOWN_SLUGS = [
    "abr-messengers-drums",
    "abr-messengers",
    "master-studies-morello",
    "progressive-independence-rock",
    "stick-control",
    "double-bass-freedom",
    "the-art-of-bop-drumming",
    "advanced-techniques-modern-drummer",
    "advanced-funk-studies",
    "progressive-steps-syncopation",
    "better-lovers-highly-irresponsible",
    "better-lovers-play-it-properly",
    "the-roots-you-got-me",
]

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def load_page_index():
    if PAGE_INDEX.exists():
        with open(PAGE_INDEX) as f:
            return json.load(f)
    return {}


def save_page_index(index):
    with open(PAGE_INDEX, "w") as f:
        json.dump(index, f, indent=2)
    print(f"  ✓ Updated {PAGE_INDEX.relative_to(REPO_ROOT)}")


def find_inbox_images():
    if not INBOX.exists():
        return []
    return [f for f in INBOX.iterdir() if f.suffix.lower() in IMAGE_EXTS]


def next_page_number(slug_dir: Path) -> int:
    existing = sorted(slug_dir.glob("page-*.png"))
    if not existing:
        return 1
    nums = []
    for f in existing:
        m = re.search(r"page-(\d+)", f.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1


def ingest_file(src: Path, slug: str, page_num: int, title: str = "") -> Path:
    slug_dir = RENDERED / slug
    slug_dir.mkdir(parents=True, exist_ok=True)
    dest = slug_dir / f"page-{page_num:03d}.png"

    # Convert to PNG if needed (requires Pillow)
    if src.suffix.lower() in {".jpg", ".jpeg", ".webp"}:
        try:
            from PIL import Image
            img = Image.open(src)
            img.save(dest, "PNG")
            print(f"  ✓ Converted {src.name} → {dest.relative_to(REPO_ROOT)}")
        except ImportError:
            shutil.copy2(src, dest)
            os.rename(dest, dest.with_suffix(src.suffix))
            dest = dest.with_suffix(src.suffix)
            print(f"  ✓ Copied {src.name} → {dest.relative_to(REPO_ROOT)} (Pillow not installed, kept original format)")
    else:
        shutil.copy2(src, dest)
        print(f"  ✓ Moved {src.name} → {dest.relative_to(REPO_ROOT)}")

    # Remove from inbox
    src.unlink()
    return dest


def update_index(index: dict, slug: str, page_num: int) -> dict:
    if slug not in index:
        index[slug] = []
    if page_num not in index[slug]:
        index[slug].append(page_num)
        index[slug].sort()
    return index


def list_inbox():
    images = find_inbox_images()
    if not images:
        print("Inbox is empty.")
        return []
    print(f"\nFound {len(images)} image(s) in inbox:")
    for i, f in enumerate(images):
        size_kb = f.stat().st_size // 1024
        print(f"  [{i+1}] {f.name} ({size_kb} KB)")
    return images


def prompt_slug(filename: str) -> str:
    print(f"\nKnown slugs:")
    for i, s in enumerate(KNOWN_SLUGS):
        print(f"  {i+1:2d}. {s}")
    print(f"   n. Enter a new slug")
    choice = input(f"Slug for '{filename}' (number or name): ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(KNOWN_SLUGS):
            return KNOWN_SLUGS[idx]
    return choice.lower().replace(" ", "-")


def prompt_page(slug: str, src: Path) -> int:
    slug_dir = RENDERED / slug
    suggested = next_page_number(slug_dir)
    val = input(f"Page number for this image (suggested: {suggested}): ").strip()
    return int(val) if val.isdigit() else suggested


def run_interactive():
    images = list_inbox()
    if not images:
        return

    index = load_page_index()
    committed = []

    for src in images:
        print(f"\n{'─'*50}")
        print(f"Processing: {src.name}")
        slug = prompt_slug(src.name)
        page_num = prompt_page(slug, src)
        dest = ingest_file(src, slug, page_num)
        index = update_index(index, slug, page_num)
        committed.append((slug, page_num, dest))

    save_page_index(index)

    print(f"\n{'─'*50}")
    print(f"✓ Ingested {len(committed)} file(s):")
    for slug, page, dest in committed:
        cdn = f"https://media.githubusercontent.com/media/totster87/music-kb/main/{dest.relative_to(REPO_ROOT)}".replace("\\", "/")
        print(f"  {slug}/page-{page:03d}.png")
        print(f"  CDN: {cdn}")

    print("\nNext: git add + commit + push these files.")


def run_auto():
    """Non-interactive mode: just list what's in the inbox as JSON for Claude."""
    images = find_inbox_images()
    result = []
    for f in images:
        result.append({
            "filename": f.name,
            "size_kb": f.stat().st_size // 1024,
            "path": str(f)
        })
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if "--auto" in sys.argv:
        run_auto()
    else:
        run_interactive()
