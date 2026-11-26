#!/usr/bin/env bash
# install_fonts.sh — install deterministic 10 pt Latin Modern fonts for matplotlib.
#
# Why: Latin Modern ships 5/6/7/8/9/10/12/17 pt optical masters whose family
# name is identical ("Latin Modern Roman"). Keeping only the 10 pt masters plus
# latinmodern-math.otf prevents matplotlib from picking the 20%-wider 6 pt face.
#
# Usage:
#   SRC=/path/to/texmf/fonts/opentype/public bash scripts/install_fonts.sh
set -euo pipefail

DST="${DST:-/usr/local/share/fonts/latin-modern}"
SRC="${SRC:-}"

if [ -z "$SRC" ]; then
    for cand in \
        "/usr/share/texmf/fonts/opentype/public" \
        "/usr/share/texlive/texmf-dist/fonts/opentype/public" \
        "/usr/local/texlive/*/texmf-dist/fonts/opentype/public" \
        /mnt/c/Users/*/AppData/Local/Programs/MiKTeX/fonts/opentype/public; do
        if [ -d "$cand/lm" ]; then
            SRC="$cand"
            break
        fi
    done
fi

if [ -z "$SRC" ] || [ ! -d "$SRC/lm" ]; then
    echo "ERROR: Latin Modern OTFs not found. Set SRC=<path to .../opentype/public>." >&2
    exit 1
fi

STAGE="$(mktemp -d)"
mkdir -p "$DST"
cp "$SRC/lm"/*.otf "$STAGE"/
[ -d "$SRC/lm-math" ] && cp "$SRC/lm-math"/*.otf "$STAGE"/ || true

# Keep only the 10 pt optical masters (+ the math font)
find "$STAGE" -name '*.otf' ! -name '*10-*' ! -name 'latinmodern-math.otf' -delete

rm -f "$DST"/*.otf
cp "$STAGE"/*.otf "$DST"/
rm -rf "$STAGE"

fc-cache -f "$DST" >/dev/null
rm -rf "$HOME/.cache/matplotlib"

echo "installed $(ls -1 "$DST"/*.otf | wc -l) OTF files into $DST"
fc-match "Latin Modern Roman"
fc-match "Latin Modern Roman:bold"
fc-match "Latin Modern Math"
