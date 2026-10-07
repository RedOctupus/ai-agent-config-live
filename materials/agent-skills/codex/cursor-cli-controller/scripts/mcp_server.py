"""stdio MCP adapter. Runtime state and audit also belong to the CLI core."""
from __future__ import annotations

import argparse
import asyncio
from typing import Any

from mcp.server import MCPServer

from cursor_runtime import Controller, ControlError


def create_server(controller: Controller) -> MCPServer:
    server = MCPServer(
        "cursor-controller",
        version="0.1.0",
        instructions=(
            "For the coordinating Codex host. Cursor executes delegated contracts; "
            "it must not recursively dispatch controller tasks. Execution success, "
            "verification, approval and required memory/AOCI writeback are separate. "
            "Audit remains independent of project MEMORY kit. Use exact current-run IDs."
        ),
    )

    async def call(method: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            data = await asyncio.to_thread(getattr(controller, method), *args, **kwargs)
            return {"ok": True, "data": data}
        except ControlError as exc:
            return {"ok": False, "error": {
                "code": exc.code,
                "message": str(exc),
                "details": getattr(exc, "details", None),
            }}

    @server.tool()
    async def cursor_doctor() -> dict[str, Any]:
        """Check Cursor Agent CLI and redacted authentication status; no model request."""
        response = await call("doctor")
        if response["ok"]:
            response["data"]["data_dir"] = str(controller.data_dir)
        return response

    @server.tool()
    async def cursor_capabilities(workspace: str, skill_names: list[str]) -> dict[str, Any]:
        """Resolve skill availability per host; readability is distinct from observed invocation."""
        return await call("capabilities", workspace, skill_names)

    @server.tool()
    async def cursor_submit(contract: dict[str, Any]) -> dict[str, Any]:
        """Start an authorized task from objective, workspace, strategy, ownership and acceptance contract."""
        return await call("submit", contract)

    @server.tool()
    async def cursor_status(task_id: str, after_event_id: int = 0) -> dict[str, Any]:
        """Read latest run state and new bounded events after its audit cursor."""
        return await call("status", task_id, after_event_id)

    @server.tool()
    async def cursor_watch(task_id: str, after_event_id: int = 0,
                           wait_seconds: float = 10) -> dict[str, Any]:
        """Wait up to 30 seconds for task changes; reuse returned cursor on the next call."""
        return await call("watch", task_id, after_event_id, wait_seconds)

    @server.tool()
    async def cursor_stop(task_id: str) -> dict[str, Any]:
        """Request task-scoped process-tree stop; parent exit alone does not release ownership."""
        return await call("stop", task_id)

    @server.tool()
    async def cursor_resume(task_id: str, instruction: str) -> dict[str, Any]:
        """Continue the exact recorded Cursor session in a new run needing fresh receipts."""
        return await call("resume", task_id, instruction)

    @server.tool()
    async def cursor_result(task_id: str) -> dict[str, Any]:
        """Read execution result and evidence; this does not imply approval."""
        return await call("result", task_id)

    @server.tool()
    async def cursor_verify(task_id: str, run_id: str) -> dict[str, Any]:
        """Run only contract-registered argv verification commands and record actual machine evidence."""
        return await call("verify", task_id, run_id)

    @server.tool()
    async def cursor_record_acceptance(
        task_id: str, run_id: str, decision: str,
        attribution: dict[str, Any], evidence: list[dict[str, Any]],
        memory_receipt: dict[str, Any] | None = None,
        aoci_receipt: dict[str, Any] | None = None,
        report_path: str | None = None,
    ) -> dict[str, Any]:
        """Record current-run review/decision with explicit author/reviewer/decider and required writeback receipts."""
        return await call(
            "record_acceptance", task_id, run_id, decision, attribution, evidence,
            memory_receipt=memory_receipt, aoci_receipt=aoci_receipt, report_path=report_path,
        )

    @server.tool()
    async def cursor_audit(task_id: str, after_event_id: int = 0) -> dict[str, Any]:
        """Read independent task audit and actor/evidence links, even when project Kit is absent."""
        return await call("audit", task_id, after_event_id)

    @server.tool()
    async def cursor_list_tasks() -> dict[str, Any]:
        """List persisted controller tasks after a reconnect or across conversations."""
        return await call("list_tasks")

    return server


def main() -> None:
    parser = argparse.ArgumentParser(description="Cursor task MCP (stdio; Codex coordinator only)")
    parser.add_argument("--data-dir", help="Shared runtime/audit directory; defaults to the user's local data directory")
    parser.add_argument("--agent-path", help="Optional explicit Cursor Agent executable or launcher")
    args = parser.parse_args()
    create_server(Controller(data_dir=args.data_dir, agent_path=args.agent_path)).run(transport="stdio")


if __name__ == "__main__":
    main()
