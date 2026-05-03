"""
Generate a self-contained scrollable HTML viewer for any song or exercise page range.

Usage:
  python generate_viewer.py <slug> <title> <start_page> <end_page>

Examples:
  python generate_viewer.py better-lovers-highly-irresponsible "Better Lovers - Lie Between the Lines" 7 19
  python generate_viewer.py master-studies-morello "Morello - Groups of Four" 10 15
  python generate_viewer.py progressive-independence-rock "PI Rock - Part 3 Combos" 9 11
"""

import base64, os, sys

RENDERED_BASE = "C:/Git/music-kb/docs/rendered"
VIEWER_OUT = "C:/Git/music-kb/docs/viewers"

def make_html(title, image_paths, out_path):
    imgs_html = ''
    for i, path in enumerate(image_paths):
        with open(path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        imgs_html += f'''
        <div class="page">
            <div class="page-num">Page {i+1} of {len(image_paths)}</div>
            <img src="data:image/png;base64,{b64}" alt="Page {i+1}">
        </div>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #1a1a1a; font-family: sans-serif; color: #ccc; }}
  header {{ position: sticky; top: 0; background: #111; padding: 12px 20px;
            display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid #333; z-index: 10; }}
  header h1 {{ font-size: 1rem; color: #fff; letter-spacing: 0.05em; }}
  header span {{ font-size: 0.8rem; color: #888; }}
  .pages {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
  .page {{ margin-bottom: 24px; background: #222; border-radius: 6px;
           overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.4); }}
  .page-num {{ padding: 6px 12px; font-size: 0.7rem; color: #555;
               background: #1a1a1a; border-bottom: 1px solid #2a2a2a; }}
  .page img {{ width: 100%; display: block; }}
</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <span>{len(image_paths)} pages</span>
</header>
<div class="pages">{imgs_html}
</div>
</body>
</html>'''
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    size = os.path.getsize(out_path) / 1024 / 1024
    print(f'Done: {out_path} ({size:.1f} MB)')

if __name__ == '__main__':
    slug = sys.argv[1]
    title = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])

    pages = [f'{RENDERED_BASE}/{slug}/page-{i:03d}.png' for i in range(start, end + 1)]
    missing = [p for p in pages if not os.path.exists(p)]
    if missing:
        print(f'Missing files: {missing}')
        sys.exit(1)

    safe_title = title.replace('/', '-').replace(':', '-')
    out = f'{VIEWER_OUT}/{safe_title}.html'
    make_html(title, pages, out)
