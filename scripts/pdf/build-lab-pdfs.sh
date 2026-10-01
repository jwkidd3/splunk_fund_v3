#!/bin/bash
# Build one PDF per lab: markdown -> styled HTML (pandoc) -> PDF (headless Chrome).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$REPO/labs/pdf"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$OUT" "$SC/.build"

for md in "$REPO"/labs/lab*.md; do
  base=$(basename "$md" .md)
  html="$SC/.build/$base.html"

  pandoc "$md" \
    --standalone \
    --from=gfm \
    --to=html5 \
    --metadata title="$base" \
    --css="$SC/lab.css" \
    --embed-resources \
    --highlight-style=tango \
    -o "$html"

  # <details> renders collapsed in print, which would hide the answer key
  # entirely. Force it open.
  perl -pi -e 's/<details>/<details open>/g' "$html"
  # "Click to reveal" is meaningless on paper
  perl -pi -e 's/Click to reveal answers/Instructor answer key/g' "$html"

  "$CHROME" --headless --disable-gpu --no-sandbox \
    --no-pdf-header-footer \
    --print-to-pdf="$OUT/$base.pdf" \
    --virtual-time-budget=10000 \
    "file://$html" >/dev/null 2>&1

  printf "  %-38s %s\n" "$base.pdf" "$(du -h "$OUT/$base.pdf" | cut -f1)"
done

echo "BUILD_DONE"
