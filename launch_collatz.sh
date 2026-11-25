#!/usr/bin/env bash
set -euo pipefail

script_path="$(readlink -f -- "${BASH_SOURCE[0]}")"
app_dir="$(cd -- "$(dirname -- "$script_path")" && pwd)"

choose_port() {
  python3 - <<'PY'
import socket

with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    print(sock.getsockname()[1])
PY
}

open_browser() {
  local url="$1"

  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url" >/dev/null 2>&1 &
  elif command -v sensible-browser >/dev/null 2>&1; then
    sensible-browser "$url" >/dev/null 2>&1 &
  elif command -v firefox >/dev/null 2>&1; then
    firefox "$url" >/dev/null 2>&1 &
  elif command -v google-chrome >/dev/null 2>&1; then
    google-chrome "$url" >/dev/null 2>&1 &
  fi
}

port="$(choose_port)"
url="http://127.0.0.1:$port/index.html"
printf 'Collatz Explorer: %s\n' "$url"
printf 'Serving from %s. Press Ctrl+C to stop.\n' "$app_dir"

open_browser "$url"
exec python3 -m http.server "$port" --bind 127.0.0.1 --directory "$app_dir"
