#!/bin/bash
# Run from music-kb repo root: bash docs/render_inbox.sh
# Requires: pdftoppm (poppler-utils)
# Git Bash on Windows: download poppler from https://github.com/oschwartz10612/poppler-windows/releases
#   unzip, add the bin/ folder to PATH, then run this script

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INBOX="$REPO/docs/inbox"
RENDERED="$REPO/docs/rendered"

render_pdf() {
    local fname="$1"
    local slug="$2"
    local pdf="$INBOX/$fname"
    local outdir="$RENDERED/$slug"

    if [ ! -f "$pdf" ]; then
        echo "SKIP (not found): $fname"
        return
    fi

    local size
    size=$(wc -c < "$pdf")
    if [ "$size" -lt 500 ]; then
        echo "SKIP (LFS pointer — run git lfs pull first): $fname"
        return
    fi

    echo "Rendering: $fname"
    echo "  → slug: $slug"
    mkdir -p "$outdir"

    git lfs track "docs/rendered/$slug/*.png" 2>/dev/null || true

    # Convert to Windows paths if on Windows (pdftoppm is a Windows binary)
    local win_pdf win_prefix
    if command -v cygpath &>/dev/null; then
        win_pdf="$(cygpath -w "$pdf")"
        win_prefix="$(cygpath -w "$outdir/page")"
    else
        win_pdf="$pdf"
        win_prefix="$outdir/page"
    fi
    pdftoppm -r 150 -png "$win_pdf" "$win_prefix"

    # Rename page-1.png → page-001.png
    for f in "$outdir"/page*.png; do
        [ -f "$f" ] || continue
        n=$(basename "$f" .png | sed 's/[^0-9]//g')
        [ -z "$n" ] && continue
        new="$outdir/page-$(printf '%03d' "$n").png"
        [ "$f" = "$new" ] || mv "$f" "$new"
    done

    local count
    count=$(ls "$outdir"/page-*.png 2>/dev/null | wc -l)
    echo "  → $count pages done"
    echo ""
}

render_pdf "331734875-Jungle-Drum-n-Bass-pdf.pdf"                   "jungle-drum-n-bass"
render_pdf "481222696-Rod-Morgenstein-Drum-Set-Warm-Ups.pdf"         "rod-morgenstein-drum-set-warm-ups"
render_pdf "673871533-120-Right-Hand-Studies-by-Mauro-Giuliani.pdf"  "120-right-hand-studies-giuliani"
render_pdf "927941105-Scale-Studies-for-Jazz-Guitar-Rick-Stone.pdf"  "scale-studies-jazz-guitar-stone"
render_pdf "converge-axe to fall.pdf"                                "converge-axe-to-fall"
render_pdf "converge-concubine.pdf"                                  "converge-concubine"
render_pdf "converge-dark horse.pdf"                                 "converge-dark-horse"
render_pdf "converge-drop out.pdf"                                   "converge-drop-out"
render_pdf "converge-first light.pdf"                                "converge-first-light"
render_pdf "converge-hum of hurt.pdf"                                "converge-hum-of-hurt"
render_pdf "converge-to feel something.pdf"                          "converge-to-feel-something"
render_pdf "converge-under duress.pdf"                               "converge-under-duress"
render_pdf "converge-versus.pdf"                                     "converge-versus"
render_pdf "converge-worms will feed.pdf"                            "converge-worms-will-feed"

echo "All done. Now run:"
echo "  git add docs/rendered/ .gitattributes"
echo "  git commit -m 'Render inbox PDFs to pages'"
echo "  git push"
