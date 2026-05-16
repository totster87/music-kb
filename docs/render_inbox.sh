#!/bin/bash
# Run from music-kb repo root: bash docs/render_inbox.sh
# Requires: pdftoppm (poppler-utils) — brew install poppler / apt install poppler-utils
set -e
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INBOX="$REPO/docs/inbox"
RENDERED="$REPO/docs/rendered"
IDX="$REPO/docs/page-index.json"

declare -A SLUG_MAP
SLUG_MAP["331734875-Jungle-Drum-n-Bass-pdf.pdf"]="jungle-drum-n-bass"
SLUG_MAP["481222696-Rod-Morgenstein-Drum-Set-Warm-Ups.pdf"]="rod-morgenstein-drum-set-warm-ups"
SLUG_MAP["673871533-120-Right-Hand-Studies-by-Mauro-Giuliani.pdf"]="120-right-hand-studies-giuliani"
SLUG_MAP["927941105-Scale-Studies-for-Jazz-Guitar-Rick-Stone.pdf"]="scale-studies-jazz-guitar-stone"
SLUG_MAP["converge-axe to fall.pdf"]="converge-axe-to-fall"
SLUG_MAP["converge-concubine.pdf"]="converge-concubine"
SLUG_MAP["converge-dark horse.pdf"]="converge-dark-horse"
SLUG_MAP["converge-drop out.pdf"]="converge-drop-out"
SLUG_MAP["converge-first light.pdf"]="converge-first-light"
SLUG_MAP["converge-hum of hurt.pdf"]="converge-hum-of-hurt"
SLUG_MAP["converge-to feel something.pdf"]="converge-to-feel-something"
SLUG_MAP["converge-under duress.pdf"]="converge-under-duress"
SLUG_MAP["converge-versus.pdf"]="converge-versus"
SLUG_MAP["converge-worms will feed.pdf"]="converge-worms-will-feed"

for fname in "${!SLUG_MAP[@]}"; do
    pdf="$INBOX/$fname"
    slug="${SLUG_MAP[$fname]}"
    outdir="$RENDERED/$slug"

    if [ ! -f "$pdf" ]; then
        echo "SKIP (not found): $fname"
        continue
    fi

    # Check if it's an LFS pointer (130 bytes or so)
    size=$(wc -c < "$pdf")
    if [ "$size" -lt 500 ]; then
        echo "SKIP (LFS pointer, not downloaded): $fname — run 'git lfs pull' first"
        continue
    fi

    echo "Rendering $fname → $slug ..."
    mkdir -p "$outdir"

    # Track in LFS if not already
    git lfs track "docs/rendered/$slug/*.png" 2>/dev/null || true

    # Render at 150 DPI (good for iPhone retina, reasonable file size)
    pdftoppm -r 150 -png "$pdf" "$outdir/page"

    # Rename page-1.png → page-001.png
    for f in "$outdir"/page-*.png "$outdir"/page*.png 2>/dev/null; do
        [ -f "$f" ] || continue
        n=$(basename "$f" | grep -o '[0-9]*\.png$' | sed 's/\.png//')
        [ -z "$n" ] && continue
        new="$outdir/page-$(printf '%03d' "$n").png"
        [ "$f" != "$new" ] && mv "$f" "$new"
    done

    count=$(ls "$outdir"/page-*.png 2>/dev/null | wc -l)
    echo "  → $count pages rendered"
done

echo ""
echo "Done. Now run:"
echo "  git add docs/rendered/ docs/.gitattributes docs/page-index.json"
echo "  git commit -m 'Render inbox PDFs to pages'"
echo "  git push"
echo ""
echo "Then tell Claude 'generate viewers' to build the HTML viewer files."
