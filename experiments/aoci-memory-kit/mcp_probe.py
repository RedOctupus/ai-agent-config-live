"""Minimal stdio MCP probe, scoped to the ignored SSSS sandbox only."""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BIN = ROOT / "artifacts" / "bin" / "aoci.exe"
REPO = ROOT / "sandbox" / "ssss-agent"


def request(proc, request_id, method, params=None):
    payload = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        payload["params"] = params
    proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
    proc.stdin.flush()
    while True:
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("MCP server closed stdout")
        result = json.loads(line)
        if result.get("id") == request_id:
            return result


def main():
    if not BIN.is_file() or not REPO.is_dir():
        raise SystemExit("Sandbox binary/repo missing")
    proc = subprocess.Popen(
        [str(BIN), "--repo", str(REPO), "mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        bufsize=1,
    )
    try:
        initialized = request(proc, 1, "initialize", {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "aoci-sandbox-probe", "version": "0.1"},
        })
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        proc.stdin.flush()
        print(json.dumps(initialized))
        listed = request(proc, 2, "tools/list")
        if len(sys.argv) <= 1:
            print(json.dumps(listed))
        else:
            print(json.dumps({"tool_names": [x["name"] for x in listed["result"]["tools"]]}))
        if len(sys.argv) > 1:
            name = sys.argv[1]
            arguments = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
            called = request(proc, 3, "tools/call", {"name": name, "arguments": arguments})
            print(json.dumps(called))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
