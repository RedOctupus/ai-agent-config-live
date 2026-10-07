"""Exercise the actual stdio MCP transport, not a function mock."""
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

from mcp import Client
from mcp.client.stdio import StdioServerParameters


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from cursor_runtime import Controller
EXPECTED_TOOLS = {
    "cursor_doctor", "cursor_capabilities", "cursor_submit", "cursor_status",
    "cursor_watch", "cursor_stop", "cursor_resume", "cursor_result",
    "cursor_verify", "cursor_record_acceptance", "cursor_audit", "cursor_list_tasks",
}


def unpack(result):
    if result.structured_content is not None:
        return result.structured_content
    return json.loads(next(block.text for block in result.content if block.type == "text"))


class MCPTransportTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cursor-mcp-test-")
        self.params = StdioServerParameters(
            command=sys.executable,
            args=[str(ROOT / "scripts" / "mcp_server.py"), "--data-dir", self.temp.name],
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    async def asyncTearDown(self):
        self.temp.cleanup()

    async def test_tools_discovery_and_structured_errors(self):
        async with Client(self.params, read_timeout_seconds=15) as client:
            listing = await client.list_tools()
            self.assertEqual({tool.name for tool in listing.tools}, EXPECTED_TOOLS)
            response = unpack(await client.call_tool("cursor_status", {"task_id": "missing-task"}))
            self.assertFalse(response["ok"])
            self.assertIsInstance(response["error"]["code"], str)
            self.assertIsInstance(response["error"]["message"], str)

    async def test_reconnect_uses_persistent_store(self):
        async with Client(self.params, read_timeout_seconds=15) as client:
            first = unpack(await client.call_tool("cursor_list_tasks", {}))
        async with Client(self.params, read_timeout_seconds=15) as client:
            second = unpack(await client.call_tool("cursor_list_tasks", {}))
        self.assertEqual(first, second)
        self.assertTrue(list(Path(self.temp.name).glob("*.sqlite*")) or
                        list(Path(self.temp.name).glob("*.db")))

    async def test_active_worker_survives_stdio_disconnect(self):
        await self.exercise_disconnect(wait_for_active=True)

    async def test_queued_worker_survives_immediate_stdio_disconnect(self):
        await self.exercise_disconnect(wait_for_active=False)

    async def exercise_disconnect(self, wait_for_active):
        workspace = Path(self.temp.name) / 'workspace'
        workspace.mkdir()
        params = self.params.model_copy(update={
            'args': self.params.args + ['--agent-path', str(ROOT / 'tests' / 'fixture_agent.py')]})
        contract = {'workspace': str(workspace), 'objective': 'sleep-disconnect',
                    'acceptance': ['Isolated test times out under its own worker'],
                    'strategy': ['direct'], 'timeout_seconds': 5,
                    'coordinator': {'id': 'codex:test', 'kind': 'agent', 'host': 'codex',
                                    'role': 'coordinator', 'source': 'declared'}}
        async with Client(params, read_timeout_seconds=20) as client:
            response = unpack(await client.call_tool('cursor_submit', {'contract': contract}))
            self.assertTrue(response['ok'], response)
            task = response['data']
            if wait_for_active:
                deadline = time.monotonic() + 8
                while time.monotonic() < deadline:
                    active = unpack(await client.call_tool('cursor_status', {'task_id': task['task_id']}))['data']
                    if active['session_id']:
                        break
                    await __import__('asyncio').sleep(0.1)
                self.assertEqual(active['state'], 'running', active)
                self.assertEqual(active['session_id'], 'fixture-session')
        controller = Controller(self.temp.name, ROOT / 'tests' / 'fixture_agent.py')
        deadline = time.monotonic() + 12
        while time.monotonic() < deadline:
            state = controller.status(task['task_id'])
            if state['state'] not in ('starting', 'running'):
                break
            await __import__('asyncio').sleep(0.1)
        self.assertEqual(state['state'], 'timed_out', state)
        self.assertTrue(state['tree_quiescent'])
        async with Client(params, read_timeout_seconds=20) as client:
            reconnected = unpack(await client.call_tool('cursor_status', {'task_id': task['task_id']}))['data']
        self.assertEqual(reconnected['run_id'], task['run_id'])
        self.assertEqual(reconnected['state'], 'timed_out')
        self.assertTrue(reconnected['tree_quiescent'])
        if os.name == 'nt':
            launches = [e for e in state['events'] if e['action'] == 'worker_launch']
            self.assertEqual(launches[0]['data']['mechanism'], 'windows_task_scheduler')
            cleanup = Path(self.temp.name) / 'tasks' / task['task_id'] / task['run_id'] / 'broker-cleanup.json'
            deadline = time.monotonic() + 5
            while not cleanup.exists() and time.monotonic() < deadline:
                await __import__('asyncio').sleep(0.1)
            self.assertTrue(json.loads(cleanup.read_text())['deleted'])
            self.assertIn('sid', launches[0]['data'], 'broker launch must retain the observed user identity')
            self.assertEqual(launches[0]['data']['sid'], json.loads(cleanup.read_text())['sid'])


if __name__ == "__main__":
    unittest.main()
