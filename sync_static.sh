#!/usr/bin/env bash
# Re-copy the canonical static build into ./static so the Streamlit app never
# drifts from composers-duet-v3. Run this after editing any sheet in the v3 build.
set -euo pipefail
SRC="${1:-../composers-duet-v3}"
DST="$(cd "$(dirname "$0")" && pwd)/static"

echo "Syncing $SRC -> $DST"
mkdir -p "$DST"
for f in flow.html cover.html score.html orchestra.html aria.html cormac.html quiz.html encore.html lookup.json; do
  cp "$SRC/$f" "$DST/$f"
done
rm -rf "$DST/assets"
cp -r "$SRC/assets" "$DST/assets"
echo "Done. static/ now holds $(ls "$DST" | wc -l) top-level entries + $(ls "$DST/assets" | wc -l) assets."
