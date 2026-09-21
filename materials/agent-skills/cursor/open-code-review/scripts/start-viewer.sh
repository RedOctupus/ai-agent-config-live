#!/usr/bin/env bash
# Start ocr viewer if port 5483 is free. stdout = JSON only.
set -u
ADDR="${1:-localhost:5483}"
PORT="${ADDR##*:}"
URL="http://localhost:${PORT}"

port_open() {
  python3 - "$1" <<'PY' 2>/dev/null && return 0
import socket, sys
s = socket.socket()
s.settimeout(0.4)
try:
    s.connect(("127.0.0.1", int(sys.argv[1])))
    sys.exit(0)
except Exception:
    sys.exit(1)
finally:
    s.close()
PY
  return 1
}

if ! command -v ocr >/dev/null; then
  printf '%s\n' '{"ok":false,"error":"ocr not on PATH","started":false,"already_running":false}'
  exit 2
fi

if port_open "$PORT"; then
  printf '%s\n' "{\"ok\":true,\"started\":false,\"already_running\":true,\"url\":\"$URL\",\"addr\":\"$ADDR\"}"
  exit 0
fi

LOGDIR="${TMPDIR:-/tmp}/ocr-viewer"
mkdir -p "$LOGDIR"
nohup ocr viewer --open=never --addr "$ADDR" >"$LOGDIR/stdout.log" 2>"$LOGDIR/stderr.log" &
PID=$!

up=false
for _ in $(seq 1 25); do
  sleep 0.2
  if port_open "$PORT"; then up=true; break; fi
done

if [ "$up" = true ]; then
  printf '%s\n' "{\"ok\":true,\"started\":true,\"already_running\":false,\"url\":\"$URL\",\"addr\":\"$ADDR\",\"pid\":$PID,\"log\":\"$LOGDIR/stdout.log\"}"
  exit 0
fi
printf '%s\n' "{\"ok\":false,\"started\":true,\"already_running\":false,\"url\":\"$URL\",\"pid\":$PID}"
exit 3
