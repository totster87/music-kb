#!/usr/bin/env python3
"""Retrofit all HTML viewers with swipe carousels.

Two patterns handled:
1. Routine viewers — `<div class="score-section">` containing N>1 `<img class="score-img">`:
   each section becomes one carousel. Single-image sections stay as-is.
2. Book viewers — sequence of `<div class="page-block">` siblings:
   all page-blocks in the same parent get wrapped in one carousel.

The carousel pattern uses CSS scroll-snap (native iOS swipe) with a JS-driven
"X / N" page counter underneath each carousel.

Idempotent: safe to re-run. Skips files that already have a `.carousel` element.
"""
import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parents[2]
VIEWERS = REPO / "docs" / "viewers"

CAROUSEL_CSS = """
/* swipe carousel — added by add_swipe_carousels.py */
.swipe-wrap { position: relative; margin: 8px 0 4px; }
.swipe {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  border-radius: 6px;
  background: #161616;
}
.swipe::-webkit-scrollbar { display: none; }
.swipe > .slide {
  flex: 0 0 100%;
  min-width: 100%;
  scroll-snap-align: start;
  scroll-snap-stop: always;
}
.swipe > .slide img { width: 100%; display: block; }
.swipe-counter {
  position: absolute;
  top: 8px; right: 10px;
  background: rgba(0,0,0,0.65);
  color: #ddd;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 10px;
  pointer-events: none;
  letter-spacing: 0.03em;
}
.swipe-hint {
  text-align: center;
  font-size: 0.7rem;
  color: #555;
  margin-top: 4px;
  letter-spacing: 0.05em;
}
""".strip()

CAROUSEL_JS = """
<script>
(function() {
  document.querySelectorAll('.swipe-wrap').forEach(function(wrap) {
    var track = wrap.querySelector('.swipe');
    var counter = wrap.querySelector('.swipe-counter');
    if (!track || !counter) return;
    var total = track.children.length;
    function update() {
      var idx = Math.round(track.scrollLeft / track.clientWidth) + 1;
      if (idx < 1) idx = 1;
      if (idx > total) idx = total;
      counter.textContent = idx + ' / ' + total;
    }
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });
})();
</script>
""".strip()


def already_processed(soup):
    return soup.find(class_="swipe-wrap") is not None


def inject_css_and_js(soup):
    style = soup.find("style")
    if style:
        style.string = (style.string or "") + "\n" + CAROUSEL_CSS + "\n"
    else:
        head = soup.find("head") or soup
        new_style = soup.new_tag("style")
        new_style.string = CAROUSEL_CSS
        head.append(new_style)

    body = soup.find("body")
    if body:
        js_fragment = BeautifulSoup(CAROUSEL_JS, "html.parser")
        body.append(js_fragment)


def wrap_in_carousel(soup, slides_content, page_count):
    """Build the swipe-wrap container with given slide HTML fragments."""
    wrap = soup.new_tag("div", **{"class": "swipe-wrap"})
    track = soup.new_tag("div", **{"class": "swipe"})
    for slide_inner in slides_content:
        slide = soup.new_tag("div", **{"class": "slide"})
        for el in slide_inner:
            slide.append(el)
        track.append(slide)
    wrap.append(track)
    counter = soup.new_tag("div", **{"class": "swipe-counter"})
    counter.string = f"1 / {page_count}"
    wrap.append(counter)
    hint = soup.new_tag("div", **{"class": "swipe-hint"})
    hint.string = "← swipe →"
    wrap.append(hint)
    return wrap


def process_score_sections(soup):
    """Pattern 1: routine viewer score-section blocks."""
    count = 0
    for section in soup.find_all(class_="score-section"):
        imgs = section.find_all("img", class_="score-img")
        if len(imgs) < 2:
            continue

        # Group children into slides: each (label, img) pair is one slide.
        # The structure is: [score-label, score-img, score-label, score-img, ...]
        slides = []
        current = []
        for child in list(section.children):
            if getattr(child, "name", None) is None:
                # whitespace text node — skip
                continue
            classes = child.get("class", []) if hasattr(child, "get") else []
            if "score-label" in classes:
                if current:
                    slides.append(current)
                current = [child.extract()]
            elif "score-img" in classes:
                current.append(child.extract())
            else:
                # unknown child — leave outside carousel
                pass
        if current:
            slides.append(current)

        if len(slides) < 2:
            continue

        # Wrap each slide group in a container; pass the list of element lists.
        carousel = wrap_in_carousel(soup, slides, len(slides))
        section.append(carousel)
        count += 1
    return count


def process_page_blocks(soup):
    """Pattern 2: book viewer page-block siblings."""
    count = 0
    # Find all parents that have >1 page-block direct children
    parents_seen = set()
    for pb in soup.find_all(class_="page-block"):
        parent = pb.parent
        if parent is None or id(parent) in parents_seen:
            continue
        parents_seen.add(id(parent))
        siblings = [c for c in parent.children if getattr(c, "name", None) and "page-block" in (c.get("class") or [])]
        if len(siblings) < 2:
            continue

        # Build slides — each page-block is one slide (use its children as slide content)
        slides = []
        for sib in siblings:
            # Take the whole page-block as a slide
            slides.append([sib.extract()])

        carousel = wrap_in_carousel(soup, slides, len(slides))
        parent.append(carousel)
        count += 1
    return count


def process_file(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    if already_processed(soup):
        return "skip (already processed)"

    n_score = process_score_sections(soup)
    n_page = process_page_blocks(soup)

    if n_score == 0 and n_page == 0:
        return "skip (no multi-page blocks)"

    inject_css_and_js(soup)
    path.write_text(str(soup), encoding="utf-8")
    return f"ok ({n_score} score-sections, {n_page} page-blocks)"


def main():
    files = sorted(VIEWERS.glob("*.html"))
    if not files:
        print("No viewer HTML files found.")
        return
    for f in files:
        result = process_file(f)
        print(f"{f.name}: {result}")


if __name__ == "__main__":
    main()
