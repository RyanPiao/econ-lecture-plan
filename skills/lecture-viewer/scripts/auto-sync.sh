#!/bin/bash
# Auto-Sync — Watch for file changes and auto-push to GitHub Pages.
# Uses fswatch (macOS built-in) with debounce.
#
# Usage:
#   ./auto-sync.sh start    # Start watching (runs in background)
#   ./auto-sync.sh stop     # Stop watching
#   ./auto-sync.sh status   # Check if running

set -euo pipefail

PIDFILE=".auto-sync.pid"
LOGFILE=".auto-sync.log"

start_sync() {
  # Check if already running
  if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "Auto-sync already running (PID $(cat "$PIDFILE")). Use 'stop' first."
    exit 1
  fi

  # Check we're in a git repo
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "ERROR: Not in a git repository. Run from the GitHub Pages repo directory."
    exit 1
  fi

  # Check fswatch is available
  if ! command -v fswatch >/dev/null 2>&1; then
    echo "ERROR: fswatch not found. Install with: brew install fswatch"
    exit 1
  fi

  # Check remote exists
  if ! git remote get-url origin >/dev/null 2>&1; then
    echo "ERROR: No 'origin' remote. Set up GitHub remote first."
    exit 1
  fi

  echo "Starting auto-sync..."
  echo "  Watching: $(pwd)"
  echo "  Remote:   $(git remote get-url origin)"
  echo "  Log:      $LOGFILE"

  # Start watcher in background
  nohup bash -c '
    cd "'"$(pwd)"'"
    fswatch -o -l 5 --exclude ".git" --exclude ".auto-sync" . | while read num_events; do
      sleep 2  # debounce — wait for writes to finish

      # Check if there are actual changes
      if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
        continue  # no changes
      fi

      TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

      # Stage all changes
      git add -A

      # Get a meaningful commit message
      CHANGED=$(git diff --cached --name-only | head -5 | tr "\n" ", " | sed "s/,$//")
      MSG="Update slides: $CHANGED"

      # Commit and push
      if git commit -m "$MSG" 2>>.auto-sync.log; then
        if git push 2>>.auto-sync.log; then
          echo "[$TIMESTAMP] Pushed: $MSG" >> .auto-sync.log
          echo "[$TIMESTAMP] Pushed: $MSG"
        else
          echo "[$TIMESTAMP] ERROR: push failed" >> .auto-sync.log
        fi
      fi
    done
  ' > "$LOGFILE" 2>&1 &

  echo $! > "$PIDFILE"
  disown $!

  echo "Auto-sync started (PID $(cat "$PIDFILE"))."
  echo "Changes will auto-push to GitHub within ~10 seconds of saving."
  echo ""
  echo "Commands:"
  echo "  ./auto-sync.sh status   # check if running"
  echo "  ./auto-sync.sh stop     # stop watching"
  echo "  tail -f $LOGFILE        # watch the log"
}

stop_sync() {
  if [ ! -f "$PIDFILE" ]; then
    echo "Auto-sync not running (no PID file)."
    return
  fi

  PID=$(cat "$PIDFILE")
  if kill -0 "$PID" 2>/dev/null; then
    # Kill children first (fswatch, git), then parent — macOS compatible
    pkill -P "$PID" 2>/dev/null
    kill "$PID" 2>/dev/null
    echo "Auto-sync stopped (PID $PID)."
  else
    echo "Auto-sync was not running (stale PID $PID)."
  fi

  rm -f "$PIDFILE"
}

check_status() {
  if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    PID=$(cat "$PIDFILE")
    echo "Auto-sync running (PID $PID)"
    echo "Last log entries:"
    tail -3 "$LOGFILE" 2>/dev/null || echo "  (no log entries yet)"
  else
    echo "Auto-sync not running."
    rm -f "$PIDFILE" 2>/dev/null
  fi
}

case "${1:-help}" in
  start)   start_sync ;;
  stop)    stop_sync ;;
  status)  check_status ;;
  *)
    echo "Usage: auto-sync.sh {start|stop|status}"
    echo ""
    echo "  start   Start watching for changes and auto-pushing to GitHub"
    echo "  stop    Stop the file watcher"
    echo "  status  Check if auto-sync is running"
    ;;
esac
