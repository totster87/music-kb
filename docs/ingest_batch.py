#!/usr/bin/env python3
"""
Batch LFS download + PDF rendering for music-kb inbox.
Usage: python docs/ingest_batch.py
"""
import json, os, re, subprocess, sys, urllib.request, urllib.parse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(REPO_ROOT, "docs/inbox")
RENDERED = os.path.join(REPO_ROOT, "docs/rendered")
LFS_BATCH_URL = "https://github.com/totster87/music-kb.git/info/lfs/objects/batch"

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
}


def read_lfs_pointer(path):
    with open(path) as f:
        content = f.read()
    oid = re.search(r"oid sha256:([0-9a-f]+)", content)
    size = re.search(r"size (\d+)", content)
    if not oid:
        return None, None
    return oid.group(1), int(size.group(1)) if size else 0


def lfs_batch_download(objects):
    """objects: list of (filename, oid, size). Returns {oid: download_url}."""
    payload = json.dumps({
        "operation": "download",
        "transfers": ["basic"],
        "objects": [{"oid": oid, "size": size} for _, oid, size in objects]
    }).encode()
    req = urllib.request.Request(
        LFS_BATCH_URL,
        data=payload,
        headers={
            "Content-Type": "application/vnd.git-lfs+json",
            "Accept": "application/vnd.git-lfs+json",
        }
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    result = {}
    for obj in data.get("objects", []):
        if "actions" in obj and "download" in obj["actions"]:
            result[obj["oid"]] = obj["actions"]["download"]["href"]
    return result


def download_file(url, dest):
    print(f"  Downloading → {os.path.basename(dest)} ...", end=" ", flush=True)
    urllib.request.urlretrieve(url, dest)
    print(f"done ({os.path.getsize(dest) // 1024}KB)")


def render_pdf(pdf_path, slug):
    out_dir = os.path.join(RENDERED, slug)
    os.makedirs(out_dir, exist_ok=True)
    prefix = os.path.join(out_dir, "page")
    print(f"  Rendering {slug} ...", end=" ", flush=True)
    result = subprocess.run(
        ["pdftoppm", "-r", "150", "-png", pdf_path, prefix],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        return []
    pages = sorted(f for f in os.listdir(out_dir) if f.endswith(".png"))
    # pdftoppm names files like page-1.png or page-01.png — rename to page-001.png
    renamed = []
    for p in pages:
        m = re.search(r"-(\d+)\.png$", p)
        if m:
            num = int(m.group(1))
            new_name = f"page-{num:03d}.png"
            src = os.path.join(out_dir, p)
            dst = os.path.join(out_dir, new_name)
            if src != dst:
                os.rename(src, dst)
            renamed.append(new_name)
    print(f"{len(renamed)} pages")
    return renamed


def update_page_index(slug, pages):
    idx_path = os.path.join(REPO_ROOT, "docs/page-index.json")
    with open(idx_path) as f:
        index = json.load(f)
    nums = []
    for p in pages:
        m = re.search(r"page-(\d+)\.png", p)
        if m:
            nums.append(int(m.group(1)))
    index[slug] = sorted(nums)
    with open(idx_path, "w") as f:
        json.dump(index, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"  page-index.json updated: {slug} → {len(nums)} pages")


def git_lfs_track(slug):
    pattern = f"docs/rendered/{slug}/*.png"
    subprocess.run(
        ["git", "lfs", "track", pattern],
        cwd=REPO_ROOT, capture_output=True
    )


def main():
    inbox_pdfs = []
    for fname, slug in SLUG_MAP.items():
        path = os.path.join(INBOX, fname)
        if not os.path.exists(path):
            print(f"SKIP (not in inbox): {fname}")
            continue
        oid, size = read_lfs_pointer(path)
        if not oid:
            print(f"SKIP (not LFS pointer, already downloaded?): {fname}")
            inbox_pdfs.append((fname, slug, path, None))
            continue
        inbox_pdfs.append((fname, slug, path, oid, size))

    # Fetch download URLs for LFS objects
    lfs_objects = [(f, oid, sz) for f, slug, path, oid, *rest in inbox_pdfs
                   if len([f, slug, path, oid, *rest]) == 5
                   for sz in rest]
    # simpler:
    to_download = []
    for item in inbox_pdfs:
        if len(item) == 5:
            fname, slug, path, oid, size = item
            to_download.append((fname, oid, size, slug, path))

    if to_download:
        print(f"\nFetching LFS download URLs for {len(to_download)} files...")
        url_map = lfs_batch_download([(f, oid, sz) for f, oid, sz, _, _ in to_download])

        for fname, oid, size, slug, path in to_download:
            print(f"\n[{slug}]")
            if oid not in url_map:
                print(f"  ERROR: no download URL for {fname}")
                continue
            download_file(url_map[oid], path)
            git_lfs_track(slug)
            pages = render_pdf(path, slug)
            if pages:
                update_page_index(slug, pages)

    print("\nDone. Remember to: git add + commit + push rendered pages and page-index.json")


if __name__ == "__main__":
    main()
