"""One-shot MCP call against an ignored, disposable workspace fixture only."""

import argparse
import json
import subprocess
from pathlib import Path

from mcp_probe import request


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "artifacts" / "workspace-fixtures"
BIN = ROOT / "artifacts" / "bin" / "aoci.exe"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", choices=("integration", "task-merge-a", "task-merge-b"))
    parser.add_argument("tool")
    parser.add_argument("arguments", nargs="?", default="{}")
    args = parser.parse_args()
    repo = (FIXTURES / args.fixture).resolve()
    if not repo.is_relative_to(FIXTURES.resolve()) or not (repo / ".git").exists():
        raise SystemExit("fixture repo missing or outside test boundary")
    proc = subprocess.Popen(
        [str(BIN), "--repo", str(repo), "mcp"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        text=True, encoding="utf-8", bufsize=1,
    )
    try:
        request(proc, 1, "initialize", {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "kit-workspace-merge-trial", "version": "0.1"},
        })
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        proc.stdin.flush()
        response = request(proc, 2, "tools/call", {
            "name": args.tool, "arguments": json.loads(args.arguments),
        })
        print(json.dumps(response, ensure_ascii=False))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
