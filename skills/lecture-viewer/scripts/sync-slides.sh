#!/bin/bash
# sync-slides.sh — Drop folder approach for adding PNG slides
#
# Usage:
#   1. Put PNGs in extra-slides/ (name them to control order: 01-intro.png, 02-chart.png)
#   2. Run: ./sync-slides.sh
#   3. Done. Presentation updated. If auto-sync is running, it pushes to GitHub.
#
# PNGs display edge-to-edge (full 16:9 fill) — perfect for NLM slides, Canva exports, screenshots.
# Order = alphabetical sort of filenames in extra-slides/
#
# To add a new slide: just copy a PNG to extra-slides/ and re-run this script.
# To remove a slide: delete the PNG from extra-slides/ and re-run.
# To reorder: rename files (01-xxx.png, 02-xxx.png) and re-run.

set -euo pipefail

# Find presentation.html
if [ -f "presentation.html" ]; then
  PRES="presentation.html"
  DIR="."
elif [ -f "../presentation.html" ]; then
  PRES="../presentation.html"
  DIR=".."
else
  echo "ERROR: presentation.html not found. Run from the lecture directory."
  exit 1
fi

EXTRA_DIR="$DIR/extra-slides"

# Create drop folder if it doesn't exist
mkdir -p "$EXTRA_DIR"

# Count PNGs
PNGS=($(find "$EXTRA_DIR" -maxdepth 1 -name "*.png" -o -name "*.PNG" -o -name "*.jpg" -o -name "*.jpeg" | sort))
COUNT=${#PNGS[@]}

if [ "$COUNT" -eq 0 ]; then
  echo "No images in extra-slides/. Drop PNGs there and re-run."
  echo "  mkdir -p extra-slides"
  echo "  cp your-slide.png extra-slides/01-slide-name.png"
  exit 0
fi

# Build the HTML for extra slides
MARKER_START="<!-- EXTRA-SLIDES-START -->"
MARKER_END="<!-- EXTRA-SLIDES-END -->"

SLIDES_HTML="$MARKER_START"
SLIDES_HTML+="\n<section id=\"extra-divider\" data-background-color=\"#2D2D2D\">"
SLIDES_HTML+="\n  <h2 style=\"color: #FAFAF8; font-size: 32pt;\">Additional Slides</h2>"
SLIDES_HTML+="\n  <p style=\"color: #A0A0A0; font-size: 16pt;\">$COUNT slides from extra-slides/</p>"
SLIDES_HTML+="\n</section>"

for png in "${PNGS[@]}"; do
  BASENAME=$(basename "$png")
  REL_PATH="extra-slides/$BASENAME"
  # Clean name for alt text: remove number prefix + extension
  ALT=$(echo "$BASENAME" | sed 's/^[0-9]*[-_]*//' | sed 's/\.[^.]*$//' | tr '-_' '  ')

  SLIDES_HTML+="\n<section id=\"extra-$(echo "$BASENAME" | sed 's/\.[^.]*$//')\">"
  SLIDES_HTML+="\n  <img src=\"$REL_PATH\" style=\"position:absolute;top:0;left:0;width:100%;height:100%;object-fit:contain;\" alt=\"$ALT\">"
  SLIDES_HTML+="\n</section>"
done

SLIDES_HTML+="\n$MARKER_END"

# Check if extra slides section already exists
if grep -q "$MARKER_START" "$PRES"; then
  # Replace existing section
  # Use python for reliable multi-line replacement
  python3 -c "
import re
with open('$PRES', 'r') as f:
    content = f.read()

# Replace between markers (inclusive)
pattern = r'$MARKER_START.*?$MARKER_END'
replacement = '''$(echo -e "$SLIDES_HTML")'''
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('$PRES', 'w') as f:
    f.write(content)
"
  echo "Updated $COUNT extra slides in presentation.html"
else
  # Insert before closing </div> of .slides container
  python3 -c "
with open('$PRES', 'r') as f:
    content = f.read()

# Find the last </section> before </div> closing .slides
# Insert our slides before the closing </div> of the .slides div
import re
# Find </div> that closes .slides (last one before </div> closing .reveal)
# Strategy: insert before the very last </div></div> pair in the file
insertion = '''$(echo -e "$SLIDES_HTML")'''
# Insert before the final closing tags of the slides container
# Look for the pattern where .slides div ends
pos = content.rfind('</section>')
if pos >= 0:
    insert_pos = pos + len('</section>')
    content = content[:insert_pos] + '\n' + insertion + '\n' + content[insert_pos:]

with open('$PRES', 'w') as f:
    f.write(content)
"
  echo "Added $COUNT extra slides to presentation.html"
fi

echo ""
echo "Slides from extra-slides/:"
for png in "${PNGS[@]}"; do
  echo "  $(basename "$png")"
done
echo ""
echo "To add more: copy PNGs to extra-slides/ and re-run ./sync-slides.sh"
echo "To reorder: rename files (01-xxx.png, 02-xxx.png) and re-run"
echo "To remove: delete from extra-slides/ and re-run"
