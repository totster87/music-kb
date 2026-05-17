#!/usr/bin/env python3
"""Generate HTML viewers for the 14 newly rendered slugs."""
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RENDERED = os.path.join(REPO, "docs", "rendered")
VIEWERS = os.path.join(REPO, "docs", "viewers")
CDN = "https://media.githubusercontent.com/media/totster87/music-kb/main/docs/rendered"

BOOKS = [
    {
        "slug": "jungle-drum-n-bass",
        "title": "Jungle / Drum 'n' Bass",
        "subtitle": "Drums · Breakbeat patterns, Amen variations, syncopated grooves",
        "filename": "Jungle-DnB-Full.html",
    },
    {
        "slug": "rod-morgenstein-drum-set-warm-ups",
        "title": "Drum Set Warm-Ups",
        "subtitle": "Rod Morgenstein · Drums · Full book",
        "filename": "Morgenstein-Drum-Set-Warm-Ups-Full.html",
    },
    {
        "slug": "120-right-hand-studies-giuliani",
        "title": "120 Right Hand Studies",
        "subtitle": "Mauro Giuliani · Guitar · Classical fingerpicking (p i m a)",
        "filename": "Giuliani-120-Right-Hand-Studies-Full.html",
    },
    {
        "slug": "scale-studies-jazz-guitar-stone",
        "title": "Scale Studies for Jazz Guitar",
        "subtitle": "Rick Stone · Guitar · Jazz scales, modes, bebop vocabulary",
        "filename": "Stone-Scale-Studies-Jazz-Guitar-Full.html",
    },
    {
        "slug": "converge-axe-to-fall",
        "title": "Converge — Axe to Fall",
        "subtitle": "Guitar tab · Drop D",
        "filename": "Converge-Axe-to-Fall.html",
    },
    {
        "slug": "converge-concubine",
        "title": "Converge — Concubine",
        "subtitle": "Guitar tab",
        "filename": "Converge-Concubine.html",
    },
    {
        "slug": "converge-dark-horse",
        "title": "Converge — Dark Horse",
        "subtitle": "Guitar tab",
        "filename": "Converge-Dark-Horse.html",
    },
    {
        "slug": "converge-drop-out",
        "title": "Converge — Drop Out",
        "subtitle": "Guitar tab",
        "filename": "Converge-Drop-Out.html",
    },
    {
        "slug": "converge-first-light",
        "title": "Converge — First Light",
        "subtitle": "Guitar tab",
        "filename": "Converge-First-Light.html",
    },
    {
        "slug": "converge-hum-of-hurt",
        "title": "Converge — Hum of Hurt",
        "subtitle": "Guitar tab",
        "filename": "Converge-Hum-of-Hurt.html",
    },
    {
        "slug": "converge-to-feel-something",
        "title": "Converge — To Feel Something",
        "subtitle": "Guitar tab",
        "filename": "Converge-To-Feel-Something.html",
    },
    {
        "slug": "converge-under-duress",
        "title": "Converge — Under Duress",
        "subtitle": "Guitar tab",
        "filename": "Converge-Under-Duress.html",
    },
    {
        "slug": "converge-versus",
        "title": "Converge — Versus",
        "subtitle": "Guitar tab",
        "filename": "Converge-Versus.html",
    },
    {
        "slug": "converge-worms-will-feed",
        "title": "Converge — Worms Will Feed",
        "subtitle": "Guitar tab",
        "filename": "Converge-Worms-Will-Feed.html",
    },
]

CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #111; font-family: -apple-system, sans-serif; color: #ddd; line-height: 1.6; }
  header { position: sticky; top: 0; background: #0a0a0a; padding: 14px 20px;
            border-bottom: 1px solid #222; z-index: 10; }
  header h1 { font-size: 1rem; color: #fff; }
  header p { font-size: 0.75rem; color: #666; margin-top: 2px; }
  .content { max-width: 860px; margin: 0 auto; padding: 20px 16px; }
  .swipe-wrap { position: relative; margin: 8px 0 4px; }
  .swipe {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    border-radius: 8px;
    background: #161616;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4);
  }
  .swipe::-webkit-scrollbar { display: none; }
  .swipe > .slide {
    flex: 0 0 100%;
    min-width: 100%;
    scroll-snap-align: start;
    scroll-snap-stop: always;
    background: #1a1a1a;
  }
  .slide .page-label { padding: 7px 16px; font-size: 0.7rem; color: #555;
                       background: #111; border-bottom: 1px solid #222; }
  .slide img { width: 100%; display: block; min-height: 200px; background: #1a1a1a; }
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
"""

CAROUSEL_JS = """<script>
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
</script>"""


def make_viewer(book, pages):
    slug = book["slug"]
    title = book["title"]
    subtitle = book["subtitle"]

    slides = []
    for i in pages:
        url = f"{CDN}/{slug}/page-{i:03d}.png"
        slides.append(
            f'<div class="slide">\n'
            f'  <div class="page-label">Page {i}</div>\n'
            f'  <img src="{url}" alt="Page {i}" loading="lazy">\n'
            f'</div>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <p>{subtitle}</p>
</header>
<div class="content">
<div class="swipe-wrap">
<div class="swipe">
{"".join(slides)}
</div>
<div class="swipe-counter">1 / {len(pages)}</div>
<div class="swipe-hint">← swipe →</div>
</div>
</div>
{CAROUSEL_JS}
</body>
</html>"""
    return html


PAGE_COUNTS = {
    "jungle-drum-n-bass": 135,
    "rod-morgenstein-drum-set-warm-ups": 98,
    "120-right-hand-studies-giuliani": 15,
    "scale-studies-jazz-guitar-stone": 24,
    "converge-axe-to-fall": 5,
    "converge-concubine": 3,
    "converge-dark-horse": 6,
    "converge-drop-out": 5,
    "converge-first-light": 2,
    "converge-hum-of-hurt": 10,
    "converge-to-feel-something": 7,
    "converge-under-duress": 5,
    "converge-versus": 7,
    "converge-worms-will-feed": 7,
}

for book in BOOKS:
    slug = book["slug"]
    count = PAGE_COUNTS.get(slug, 0)
    if count == 0:
        print(f"SKIP (no count): {slug}")
        continue

    pages = list(range(1, count + 1))
    html = make_viewer(book, pages)
    out_path = os.path.join(VIEWERS, book["filename"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK  {book['filename']} ({len(pages)} pages)")

print("\nDone.")
