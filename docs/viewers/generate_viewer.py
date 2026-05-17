#!/usr/bin/env python3
"""
Generate HTML viewers for songs, lessons, or full books, reading from
docs/chapter-maps.json. Outputs use GitHub Pages-compatible CDN URLs (LFS media).

Commands:
  list                                List all known books with section counts.
  list <slug>                         List sections in a single book.
  show <slug>                         Show metadata for a single book.
  song <slug> <section-name>          Generate viewer for one song/section.
  combined <section-name> [<slug>...] Generate combined viewer across multiple
                                      books for the same section name. If slugs
                                      omitted, uses `companion_books` from JSON.
  book <slug>                         Generate viewer for the whole book.
  verify <slug> <section-name>        Print the first rendered page URL — open
                                      it manually to confirm chapter mapping.

Examples:
  python generate_viewer.py song abr-messengers "Truth Of A Liar"
  python generate_viewer.py combined "Composure"
  python generate_viewer.py book vai-10-hour-workout
  python generate_viewer.py verify abr-messengers "Composure"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.dirname(SCRIPT_DIR)
CHAPTER_MAPS_PATH = os.path.join(DOCS_DIR, "chapter-maps.json")
VIEWERS_DIR = SCRIPT_DIR


def load_maps() -> dict[str, Any]:
    with open(CHAPTER_MAPS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def cdn_url(maps: dict, slug: str, page: int) -> str:
    return f"{maps['$cdn_base']}/{slug}/page-{page:03d}.png"


_SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to"}


def slugify(name: str) -> str:
    safe = re.sub(r"[^\w\s\-—]", "", name)
    parts = re.split(r"[\s—]+", safe.strip())
    out = []
    for i, w in enumerate(parts):
        if not w:
            continue
        if i > 0 and w.lower() in _SMALL_WORDS:
            out.append(w.lower())
        else:
            out.append(w)
    return "-".join(out)


def find_section(book: dict, section_name: str) -> dict:
    target = section_name.casefold()
    for s in book.get("sections", []):
        if s["name"].casefold() == target:
            return s
        if target in s["name"].casefold():
            return s
    raise SystemExit(
        f"Section '{section_name}' not found in book. Available: "
        + ", ".join(s["name"] for s in book.get("sections", []))
    )


CSS = """  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #111; font-family: -apple-system, sans-serif; color: #ddd; line-height: 1.6; }
  header { position: sticky; top: 0; background: #0a0a0a; padding: 14px 20px;
            border-bottom: 1px solid #222; z-index: 10; }
  header h1 { font-size: 1rem; color: #fff; }
  header p { font-size: 0.75rem; color: #666; margin-top: 2px; }
  .content { max-width: 860px; margin: 0 auto; padding: 20px 16px; }
  .section-label { font-size: 0.75rem; font-weight: 600; color: #888;
                   text-transform: uppercase; letter-spacing: 0.08em;
                   margin: 24px 0 8px; }
  .section-label:first-child { margin-top: 0; }
  .swipe-wrap { position: relative; margin: 0 0 4px; }
  .swipe { display: flex; overflow-x: auto; scroll-snap-type: x mandatory;
            -webkit-overflow-scrolling: touch; scrollbar-width: none;
            border-radius: 8px; background: #161616; box-shadow: 0 2px 12px rgba(0,0,0,0.4); }
  .swipe::-webkit-scrollbar { display: none; }
  .swipe > .slide { flex: 0 0 100%; min-width: 100%; scroll-snap-align: start;
                    scroll-snap-stop: always; background: #1a1a1a; }
  .slide .page-label { padding: 7px 16px; font-size: 0.7rem; color: #555;
                       background: #111; border-bottom: 1px solid #222; }
  .slide img { width: 100%; display: block; min-height: 200px; background: #1a1a1a; }
  .swipe-counter { position: absolute; top: 8px; right: 10px;
                   background: rgba(0,0,0,0.65); color: #ddd; font-size: 0.72rem;
                   font-weight: 600; padding: 3px 8px; border-radius: 10px;
                   pointer-events: none; letter-spacing: 0.03em; }
  .swipe-hint { text-align: center; font-size: 0.7rem; color: #555;
                margin-top: 4px; letter-spacing: 0.05em; margin-bottom: 4px; }"""

JS = """(function() {
  document.querySelectorAll('.swipe-wrap').forEach(function(wrap) {
    var track = wrap.querySelector('.swipe');
    var counter = wrap.querySelector('.swipe-counter');
    if (!track || !counter) return;
    var total = track.children.length;
    function update() {
      var idx = Math.round(track.scrollLeft / track.clientWidth) + 1;
      if (idx < 1) idx = 1; if (idx > total) idx = total;
      counter.textContent = idx + ' / ' + total;
    }
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });
})();"""


def build_carousel(maps: dict, slug: str, start: int, end: int, label_template: str = "Page {p}") -> str:
    slides = []
    for p in range(start, end + 1):
        url = cdn_url(maps, slug, p)
        label = label_template.format(p=p)
        slides.append(
            f'<div class="slide"><div class="page-label">{label}</div>'
            f'<img src="{url}" alt="{label}" loading="lazy"></div>'
        )
    count = end - start + 1
    return (
        '<div class="swipe-wrap">\n'
        '<div class="swipe">\n'
        + "\n".join(slides)
        + "\n</div>\n"
        f'<div class="swipe-counter">1 / {count}</div>\n'
        "</div>\n"
        '<div class="swipe-hint">← swipe →</div>\n'
    )


def render_html(title: str, subtitle: str, body: str) -> str:
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>{title}</title>\n"
        f"<style>\n{CSS}\n</style>\n</head>\n<body>\n"
        f'<header>\n  <h1>{title}</h1>\n  <p>{subtitle}</p>\n</header>\n'
        f'<div class="content">\n{body}</div>\n'
        f"<script>\n{JS}\n</script>\n</body>\n</html>\n"
    )


def subtitle_for(book: dict) -> str:
    bits = [book.get("instrument", "").title()]
    if book.get("author"):
        bits.append(book["author"])
    return " · ".join(b for b in bits if b)


def write_viewer(filename: str, html: str) -> str:
    path = os.path.join(VIEWERS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ---------- commands ----------

def cmd_list(maps: dict, slug: str | None) -> None:
    if slug is None:
        for s, b in maps["books"].items():
            sec_count = len(b.get("sections", []))
            print(f"  {s:42s} {b.get('pages_rendered',0):>4} pg  {b.get('type','?'):14s}  {sec_count} sections")
        return
    book = maps["books"][slug]
    print(f"{book['title']} ({slug}) — {book.get('pages_rendered','?')} pages")
    if book.get("offset") is not None:
        print(f"  offset: +{book['offset']} (book p + {book['offset']} = rendered p)")
    for s in book.get("sections", []):
        r = s["rendered"]
        bk = s.get("book")
        bk_str = f"  (book p.{bk[0]}–{bk[1]})" if bk else ""
        print(f"  p.{r[0]:>3}–{r[1]:<3}  {s['name']}{bk_str}")


def cmd_show(maps: dict, slug: str) -> None:
    print(json.dumps(maps["books"][slug], indent=2, ensure_ascii=False))


def viewer_prefix(book: dict) -> str:
    return book.get("viewer_prefix") or book.get("author") or book["title"]


def cmd_song(maps: dict, slug: str, section_name: str) -> None:
    book = maps["books"][slug]
    section = find_section(book, section_name)
    start, end = section["rendered"]
    title = f"{viewer_prefix(book)} — {section['name']}"
    body = build_carousel(maps, slug, start, end)
    html = render_html(title, subtitle_for(book), body)
    fname = f"{slugify(viewer_prefix(book))}-{slugify(section['name'])}.html"
    path = write_viewer(fname, html)
    print(f"Wrote {path}  ({end - start + 1} pages, p.{start}–{end})")


def cmd_combined(maps: dict, section_name: str, slugs: list[str]) -> None:
    if not slugs:
        slugs = maps.get("companion_books", {}).get(section_name, [])
        if not slugs:
            raise SystemExit(
                f"No slugs given and no companion_books entry for '{section_name}'."
            )
    parts = []
    first_book = maps["books"][slugs[0]]
    for slug in slugs:
        book = maps["books"][slug]
        section = find_section(book, section_name)
        s, e = section["rendered"]
        label = book.get("instrument", "").title() or book["title"]
        parts.append(f'<div class="section-label">{label} — pp.{s}–{e}</div>\n')
        parts.append(build_carousel(maps, slug, s, e, label_template=f"{label} p.{{p}}"))
    title = f"{viewer_prefix(first_book)} — {section_name}"
    instruments = " · ".join(maps["books"][s].get("instrument", "").title() for s in slugs)
    subtitle = f"{first_book.get('author','')} · {instruments}".strip(" ·")
    html = render_html(title, subtitle, "\n".join(parts))
    fname = f"{slugify(viewer_prefix(first_book))}-{slugify(section_name)}.html"
    path = write_viewer(fname, html)
    print(f"Wrote {path}  ({len(slugs)} carousels)")


def cmd_book(maps: dict, slug: str) -> None:
    book = maps["books"][slug]
    pages = book.get("pages_rendered", 0)
    if pages <= 0:
        raise SystemExit(f"{slug} has no pages rendered.")
    body = build_carousel(maps, slug, 1, pages)
    title = book["title"]
    html = render_html(title, subtitle_for(book), body)
    fname = f"{slugify(book['title'])}.html"
    path = write_viewer(fname, html)
    print(f"Wrote {path}  ({pages} pages)")


def cmd_verify(maps: dict, slug: str, section_name: str) -> None:
    book = maps["books"][slug]
    section = find_section(book, section_name)
    start = section["rendered"][0]
    url = cdn_url(maps, slug, start)
    print(f"{book['title']} — {section['name']}")
    print(f"  First rendered page: p.{start}")
    print(f"  {url}")
    print("Open it to confirm the chapter mapping is correct.")


def main() -> None:
    ap = argparse.ArgumentParser(prog="generate_viewer.py", add_help=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").add_argument("slug", nargs="?")
    sub.add_parser("show").add_argument("slug")
    p = sub.add_parser("song"); p.add_argument("slug"); p.add_argument("section_name")
    p = sub.add_parser("combined"); p.add_argument("section_name"); p.add_argument("slugs", nargs="*")
    sub.add_parser("book").add_argument("slug")
    p = sub.add_parser("verify"); p.add_argument("slug"); p.add_argument("section_name")
    args = ap.parse_args()
    maps = load_maps()
    if args.cmd == "list":     cmd_list(maps, args.slug)
    elif args.cmd == "show":   cmd_show(maps, args.slug)
    elif args.cmd == "song":   cmd_song(maps, args.slug, args.section_name)
    elif args.cmd == "combined": cmd_combined(maps, args.section_name, args.slugs)
    elif args.cmd == "book":   cmd_book(maps, args.slug)
    elif args.cmd == "verify": cmd_verify(maps, args.slug, args.section_name)


if __name__ == "__main__":
    main()
