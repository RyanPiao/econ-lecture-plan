#!/bin/bash
# Slide Manager — CLI wrapper for slide-manager.py
# Safe HTML manipulation for RevealJS presentations.
#
# Usage:
#   ./slide-manager.sh list                                    # list all slides
#   ./slide-manager.sh add-png image.png                       # add PNG as slide at end
#   ./slide-manager.sh add-png image.png --after 12            # add PNG after slide 12
#   ./slide-manager.sh add content-figure --title "MRP Curve"  # add from template
#   ./slide-manager.sh add full-figure --image fig.png         # add full-width image slide
#   ./slide-manager.sh add two-column --title "Before vs After"
#   ./slide-manager.sh add section-divider --title "Part 2"
#   ./slide-manager.sh edit 8                                  # edit slide 8 in $EDITOR
#   ./slide-manager.sh remove 14                               # remove slide 14
#   ./slide-manager.sh show 5                                  # print slide 5 HTML

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/slide-manager.py"

# Find presentation.html — look in current dir, parent, or accept explicit path
find_presentation() {
  if [ -f "presentation.html" ]; then
    echo "presentation.html"
  elif [ -f "../presentation.html" ]; then
    echo "../presentation.html"
  else
    echo ""
  fi
}

PRES=$(find_presentation)
if [ -z "$PRES" ]; then
  echo "ERROR: presentation.html not found in current or parent directory."
  echo "Run this from the lecture directory or the viewer/ subdirectory."
  exit 1
fi

CMD="${1:-help}"
shift || true

case "$CMD" in
  list|ls)
    python3 "$PYTHON_SCRIPT" list "$PRES"
    ;;

  add-png|png)
    if [ -z "${1:-}" ]; then
      echo "Usage: slide-manager.sh add-png <image.png> [--after N]"
      exit 1
    fi
    python3 "$PYTHON_SCRIPT" add-png "$PRES" "$@"
    ;;

  add|template)
    if [ -z "${1:-}" ]; then
      echo "Usage: slide-manager.sh add <template> [--after N] [--title '...'] [--image '...']"
      echo "Templates: content-figure, full-figure, two-column, section-divider"
      exit 1
    fi
    python3 "$PYTHON_SCRIPT" add-template "$PRES" "$@"
    ;;

  edit)
    if [ -z "${1:-}" ]; then
      echo "Usage: slide-manager.sh edit <slide_number>"
      exit 1
    fi
    python3 "$PYTHON_SCRIPT" edit "$PRES" "$@"
    ;;

  remove|rm)
    if [ -z "${1:-}" ]; then
      echo "Usage: slide-manager.sh remove <slide_number>"
      exit 1
    fi
    # Confirm before removing
    SLIDE_NUM="$1"
    python3 "$PYTHON_SCRIPT" export-slide "$PRES" "$SLIDE_NUM" | head -3
    read -t 10 -p "Remove slide $SLIDE_NUM? [y/N] " confirm || confirm="N"
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
      python3 "$PYTHON_SCRIPT" remove "$PRES" "$SLIDE_NUM"
    else
      echo "Cancelled."
    fi
    ;;

  show|view)
    if [ -z "${1:-}" ]; then
      echo "Usage: slide-manager.sh show <slide_number>"
      exit 1
    fi
    python3 "$PYTHON_SCRIPT" export-slide "$PRES" "$@"
    ;;

  help|--help|-h)
    cat << 'EOF'
Slide Manager — Safe slide manipulation for RevealJS

Commands:
  list                              List all slides with numbers and titles
  add-png <image> [--after N]       Insert a PNG as a new image slide
  add <template> [options]          Insert a slide from template
  edit <N>                          Open slide N in $EDITOR
  remove <N>                        Remove slide N (with confirmation)
  show <N>                          Print slide N's HTML

Templates:
  content-figure    Title + bullets (left) + image (right)
  full-figure       Centered image + caption
  two-column        Two text columns (comparison/before-after)
  section-divider   Dark background title slide

Template options:
  --after N          Insert after slide N (default: end)
  --title "..."      Slide title
  --image "..."      Image path (for content-figure, full-figure)
  --notes "..."      Speaker notes
  --point1/2/3       Bullet points (content-figure)
  --left-heading     Left column heading (two-column)
  --right-heading    Right column heading (two-column)
  --subtitle         Subtitle text (section-divider)

Examples:
  ./slide-manager.sh list
  ./slide-manager.sh add-png new-chart.png --after 10
  ./slide-manager.sh add content-figure --title "MRP Curve" --image figures/mrp.png --after 5
  ./slide-manager.sh add section-divider --title "Part 2: Inequality" --after 15
  ./slide-manager.sh edit 8
  ./slide-manager.sh remove 22
EOF
    ;;

  *)
    echo "Unknown command: $CMD"
    echo "Run: slide-manager.sh help"
    exit 1
    ;;
esac
