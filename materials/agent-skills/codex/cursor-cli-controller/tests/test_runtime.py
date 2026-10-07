import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import contextmanager
from unittest.mock import patch
import sqlite3

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
AVAILABLE = importlib.util.find_spec('cursor_runtime') is not None
if AVAILABLE:
    from cursor_runtime import Controller, ControlError


def actor(name='codex', role='coordinator'):
    return {'id': name, 'kind': 'agent', 'host': 'codex', 'role': role, 'source': 'observed'}


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(AVAILABLE, 'deterministic cursor_runtime implementation is missing')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / '中文 project'
        self.workspace.mkdir()
        self.controller = Controller(self.root / 'data', Path(__file__).with_name('fixture_agent.py'))
        self.tasks = []
        self.addCleanup(self.cleanup_tasks)

    def cleanup_tasks(self):
        for task in self.tasks:
            state = self.controller.status(task['task_id'])
            if state['state'] in ('starting', 'running'):
                self.controller.stop(task['task_id'])
                self.wait(task)
            # Executor quiescence precedes the worker's own final log close.
            if os.name == 'nt':
                import ctypes
                from ctypes import wintypes
                kernel = ctypes.WinDLL('kernel32', use_last_error=True)
                kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
                kernel.OpenProcess.restype = wintypes.HANDLE
                kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
                kernel.CloseHandle.argtypes = [wintypes.HANDLE]
                handle = kernel.OpenProcess(0x100000, False, state.get('worker_pid') or 0)
                if handle:
                    kernel.WaitForSingleObject(handle, 5000)
                    kernel.CloseHandle(handle)

    def contract(self, objective='hello', **overrides):
        contract = {'workspace': str(self.workspace), 'objective': objective, 'acceptance': ['observable artifact'],
                    'coordinator': actor(), 'strategy': ['tdd'], 'timeout_seconds': 10}
        contract.update(overrides)
        return contract

    def submit(self, objective='hello', **overrides):
        task = self.controller.submit(self.contract(objective, **overrides))
        self.tasks.append(task)
        return task

    def wait(self, task):
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            state = self.controller.watch(task['task_id'], wait_seconds=0.1)
            if state['state'] not in ('starting', 'running'):
                return state
        self.fail('worker did not finish')

    def receipt(self, task):
        verified = self.controller.verify(task['task_id'], task['run_id'])
        attribution = {'executed_by': self.controller.result(task['task_id'])['executed_by'],
                       'authored_by': actor(role='author'), 'reviewed_by': actor(role='reviewer'),
                       'decided_by': actor(role='decider'), 'decision_basis': 'Actual test evidence and artifact inspected',
                       'authorization_basis': 'User authorized this isolated test'}
        return verified, attribution

    def test_success_unicode_and_audit_recreation(self):
        objective = '中文\n"quoted" $() `literal`'
        task = self.submit(objective)
        status = self.wait(task)
        self.assertEqual(status['state'], 'succeeded')
        self.assertEqual(status['session_id'], 'fixture-session')
        self.assertTrue(status['tree_quiescent'])
        self.assertEqual(self.controller.result(task['task_id'])['result'], objective)
        again = Controller(self.root / 'data', Path(__file__).with_name('fixture_agent.py'))
        audit = again.audit(task['task_id'])
        self.assertGreater(len(audit['records']), 2)
        self.assertTrue(audit['integrity_valid'])
        self.assertEqual(audit['records'][0]['actor']['source'], 'declared')

    def test_post_spawn_bookkeeping_failure_keeps_live_executor_lease(self):
        from cursor_runtime import core
        original_spawn, original_db = core.spawn_detached, self.controller._db
        fault = {'armed': False}
        launched = []

        @contextmanager
        def faulty_db(write=False):
            if write and fault['armed']:
                fault['armed'] = False
                raise sqlite3.OperationalError('injected post-spawn registration failure')
            with original_db(write) as db:
                yield db

        def spawn_and_wait(argv, log):
            worker = original_spawn(argv, log)
            launched.append(worker)
            task_id = argv[argv.index('--task-id') + 1]
            deadline = time.monotonic() + 6
            while time.monotonic() < deadline:
                state = self.controller.status(task_id)
                if state['session_id'] and state['pid']:
                    break
                time.sleep(0.05)
            self.assertEqual(state['state'], 'running')
            fault['armed'] = True
            return worker

        try:
            with patch.object(core, 'spawn_detached', spawn_and_wait), patch.object(self.controller, '_db', faulty_db):
                try:
                    self.controller.submit(self.contract('sleep', timeout_seconds=2))
                except ControlError:
                    pass
            task = self.controller.list_tasks()['tasks'][0]
            self.tasks.append(task)
            state = self.controller.status(task['task_id'])
            self.assertIn(state['state'], ('starting', 'running'))
            self.assertFalse(state['tree_quiescent'])
            self.assertIsNotNone(state['worker_pid'], 'worker must claim its own PID')
            with original_db() as db:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM leases').fetchone()[0], 1)
            with self.assertRaises(ControlError) as busy:
                self.controller.submit(self.contract())
            self.assertEqual(busy.exception.code, 'workspace_busy')
        finally:
            # Even the red implementation has a real bounded executor: wait for its terminal acknowledgment.
            deadline = time.monotonic() + 8
            while time.monotonic() < deadline:
                tasks = self.controller.list_tasks()['tasks']
                if tasks and self.controller.status(tasks[0]['task_id'])['state'] == 'timed_out':
                    if not self.tasks:
                        self.tasks.append(tasks[0])
                    break
                time.sleep(0.05)
            for worker in launched:
                if hasattr(worker, 'wait'):
                    worker.wait(timeout=5)

    def test_final_decision_prevents_verification_from_mutating_run(self):
        marker = self.workspace / 'verification-ran'
        command = [sys.executable, '-c', 'import pathlib; pathlib.Path("verification-ran").write_text("ran")']
        task = self.submit(verification_commands=[command])
        self.wait(task)
        verified, attribution = self.receipt(task)
        accepted = self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])
        marker.unlink()
        before = self.controller.audit(task['task_id'])
        with self.assertRaises(ControlError) as error:
            self.controller.verify(task['task_id'], task['run_id'])
        self.assertEqual(error.exception.code, 'invalid_transition')
        self.assertFalse(marker.exists(), 'finalized verification must not execute commands')
        current = self.controller.result(task['task_id'])
        self.assertEqual(current['verification_id'], verified['verification_id'])
        self.assertEqual(current['decision_id'], accepted['decision_id'])
        self.assertEqual(self.controller.audit(task['task_id']), before)

    def test_maintenance_performer_is_separate_from_codex_report_author(self):
        paths = ['map.md', 'modules/core.md']
        for relative in paths:
            path = self.workspace / relative
            path.parent.mkdir(exist_ok=True)
            path.write_text('executor maintenance evidence')
        task = self.submit(memory={'required': True, 'mode': 'executor', 'pending_paths': paths},
                           aoci={'required': True, 'host': 'cursor-cli'},
                           write_ownership={'cursor-cli': paths})
        self.wait(task)
        verified, attribution = self.receipt(task)
        evidence = [e for e in verified['evidence'] if e['kind'] == 'artifact']
        performer = actor('cursor-maintainer', 'maintenance') | {'host': 'cursor-cli'}
        memory = {'task_id': task['task_id'], 'run_id': task['run_id'], 'state': 'completed',
                  'performed_by': performer, 'evidence': evidence}
        aoci = memory | {'state': 'checked', 'host': 'cursor-cli'}
        accepted = self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                                     verified['evidence'], memory, aoci)
        records = self.controller.audit(task['task_id'])['records']
        for event in (e for e in records if e['action'] in ('memory', 'aoci')):
            self.assertEqual(event['actor'], performer | {'source': 'declared'})
            self.assertEqual(event['data']['performed_by'], event['actor'])
            self.assertEqual(event['data']['recorded_by']['host'], 'codex')
        result = self.controller.result(task['task_id'])
        self.assertEqual(result['memory_receipt']['performed_by']['host'], 'cursor-cli')
        report = Path(accepted['report_path']).read_text(encoding='utf-8')
        self.assertIn('cursor-maintainer', report)

    def mixed_memory_receipt(self, write_ownership=None, **memory_overrides):
        paths = ['project-memory.md', 'modules/core.md']
        for relative in paths:
            path = self.workspace / relative
            path.parent.mkdir(exist_ok=True)
            path.write_text('current maintenance artifact', encoding='utf-8')
        task = self.submit(memory={'required': True, 'mode': 'coordinator', 'pending_paths': paths} | memory_overrides,
                           write_ownership=({'codex': [paths[0]], 'cursor-cli': ['modules']}
                                            if write_ownership is None else write_ownership))
        self.assertEqual(self.wait(task)['state'], 'succeeded')
        verified, attribution = self.receipt(task)
        self.assertTrue(verified['passed'])
        actions = []
        for relative, host in zip(paths, ('codex', 'cursor-cli')):
            actions.append({'performed_by': actor(host + '-maintainer', 'maintenance') | {'host': host},
                            'evidence': [e for e in verified['evidence'] if e.get('relative_path') == relative]})
        memory = {'task_id': task['task_id'], 'run_id': task['run_id'], 'state': 'completed', 'actions': actions}
        return task, verified, attribution, memory

    def test_mixed_memory_performers_survive_audit_result_and_report(self):
        task, verified, attribution, memory = self.mixed_memory_receipt()
        accepted = self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                                     verified['evidence'], memory)
        records = self.controller.audit(task['task_id'])
        self.assertTrue(records['integrity_valid'])
        events = [e for e in records['records'] if e['action'] == 'memory_action']
        self.assertEqual(len(events), 2)
        stored = self.controller.result(task['task_id'])['memory_receipt']
        self.assertNotIn('performed_by', stored)
        self.assertEqual(stored['recorded_by'], attribution['authored_by'] | {'source': 'declared'})
        for original, action, event in zip(memory['actions'], stored['actions'], events):
            self.assertEqual(action['performed_by'], original['performed_by'] | {'source': 'declared'})
            self.assertEqual(event['actor'], action['performed_by'])
            self.assertEqual(action['receipt_id'], event['id'])
            self.assertEqual(event['data']['evidence'], original['evidence'])
            self.assertEqual(event['data']['recorded_by'], stored['recorded_by'])
            self.assertEqual(event['data']['task_id'], task['task_id'])
            self.assertEqual(event['data']['run_id'], task['run_id'])
        aggregate = next(e for e in records['records'] if e['id'] == accepted['memory_receipt_id'])
        self.assertEqual(aggregate['action'], 'memory')
        self.assertEqual(aggregate['actor']['id'], 'cursor-controller')
        self.assertEqual(aggregate['data'], stored)
        report = Path(accepted['report_path']).read_text(encoding='utf-8')
        data = json.loads(report.split('```json\n', 1)[1].split('\n```', 1)[0])
        self.assertEqual(data['memory_receipt'], stored)
        self.assertEqual(data['memory_receipt_id'], aggregate['id'])
        self.assertNotIn('recorded_by', memory, 'input receipt must not be mutated')

    def test_mixed_memory_rejects_wrong_owner_without_audit_mutation(self):
        task, verified, attribution, memory = self.mixed_memory_receipt()
        memory['actions'][1]['performed_by']['host'] = 'codex'
        before = self.controller.audit(task['task_id'])
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                             verified['evidence'], memory)
        self.assertEqual(error.exception.code, 'invalid_receipt')
        self.assertEqual(self.controller.audit(task['task_id']), before)
        self.assertEqual(self.controller.result(task['task_id'])['acceptance'], 'pending')

    def test_mixed_memory_rejects_omitted_path(self):
        task, verified, attribution, memory = self.mixed_memory_receipt()
        memory['actions'].pop()
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                             verified['evidence'], memory)
        self.assertEqual(error.exception.code, 'memory_pending')

    def test_mixed_memory_rejects_duplicate_path_claim(self):
        task, verified, attribution, memory = self.mixed_memory_receipt()
        memory['actions'].append(memory['actions'][0])
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                             verified['evidence'], memory)
        self.assertEqual(error.exception.code, 'invalid_receipt')

    def test_mixed_memory_rejects_stale_action_evidence(self):
        task, verified, attribution, memory = self.mixed_memory_receipt()
        entry = memory['actions'][1]['evidence'][0]
        original = entry.copy()
        for key, value in [('run_id', 'old-run'), ('sha256', '0' * 64)]:
            with self.subTest(field=key):
                memory['actions'][1]['evidence'] = [original | {key: value}]
                with self.assertRaises(ControlError) as error:
                    self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                                     verified['evidence'], memory)
                self.assertEqual(error.exception.code, 'stale_evidence')

    def test_mixed_memory_rejects_changed_artifact_hash(self):
        task, verified, attribution, memory = self.mixed_memory_receipt()
        Path(memory['actions'][1]['evidence'][0]['path']).write_text('changed after verification')
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                             verified['evidence'], memory)
        self.assertEqual(error.exception.code, 'version_conflict')

    def test_explicit_memory_host_still_restricts_mixed_receipt(self):
        task, verified, attribution, memory = self.mixed_memory_receipt(host='codex')
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                             verified['evidence'], memory)
        self.assertEqual(error.exception.code, 'invalid_receipt')

    def test_memory_grouped_receipt_rejects_ambiguous_or_empty_actions(self):
        task, verified, attribution, memory = self.mixed_memory_receipt()
        variants = [memory | {'performed_by': actor()}, memory | {'evidence': []}, memory | {'actions': []},
                    memory | {'actions': 'invalid'}, memory | {'actions': [{}]},
                    memory | {'actions': [memory['actions'][0] | {'evidence': verified['evidence']}]}]
        for invalid in variants:
            with self.subTest(receipt=invalid):
                with self.assertRaises(ControlError) as error:
                    self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                                     verified['evidence'], invalid)
                self.assertEqual(error.exception.code, 'invalid_receipt')

    def test_memory_mode_default_still_restricts_unassigned_paths(self):
        task, verified, attribution, memory = self.mixed_memory_receipt(write_ownership={})
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                             verified['evidence'], memory)
        self.assertEqual(error.exception.code, 'invalid_receipt')
        memory['actions'][1]['performed_by'] = memory['actions'][0]['performed_by']
        accepted = self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                                     verified['evidence'], memory)
        self.assertEqual(accepted['decision'], 'accepted')

    def test_memory_single_receipt_remains_compatible_with_explicit_path_owner(self):
        task, verified, attribution, memory = self.mixed_memory_receipt(
            write_ownership={'cursor-cli': ['project-memory.md', 'modules']})
        legacy = {k: memory[k] for k in ('task_id', 'run_id', 'state')}
        legacy.update(performed_by=memory['actions'][1]['performed_by'],
                      evidence=[e for action in memory['actions'] for e in action['evidence']])
        accepted = self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                                     verified['evidence'], legacy)
        stored = self.controller.result(task['task_id'])['memory_receipt']
        self.assertNotIn('actions', stored)
        self.assertEqual(stored['performed_by'], legacy['performed_by'] | {'source': 'declared'})
        records = self.controller.audit(task['task_id'])['records']
        event = next(e for e in records if e['id'] == accepted['memory_receipt_id'])
        self.assertEqual(event['action'], 'memory')
        self.assertEqual(event['actor'], stored['performed_by'])
        self.assertFalse(any(e['action'] == 'memory_action' for e in records))

    def test_mixed_memory_report_collision_rolls_back_performer_events(self):
        task, verified, attribution, memory = self.mixed_memory_receipt()
        report = self.workspace / 'existing-report.md'
        report.write_text('existing user report')
        before = self.controller.audit(task['task_id'])
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                             verified['evidence'], memory, report_path=str(report))
        self.assertEqual(error.exception.code, 'report_exists')
        self.assertEqual(self.controller.audit(task['task_id']), before)
        self.assertEqual(self.controller.result(task['task_id'])['acceptance'], 'pending')
        self.assertEqual(report.read_text(), 'existing user report')

    def test_maintenance_receipts_reject_missing_or_wrong_performer(self):
        path = self.workspace / 'map.md'
        path.write_text('map')
        task = self.submit(memory={'required': True, 'mode': 'executor', 'pending_paths': ['map.md']},
                           aoci={'required': True, 'host': 'cursor-cli'}, write_ownership={'cursor-cli': ['map.md']})
        self.wait(task)
        verified, attribution = self.receipt(task)
        evidence = [e for e in verified['evidence'] if e['kind'] == 'artifact']
        receipt = {'task_id': task['task_id'], 'run_id': task['run_id'], 'state': 'completed', 'evidence': evidence}
        cursor_actor = actor('cursor-maintainer', 'maintenance') | {'host': 'cursor-cli'}
        valid_memory = receipt | {'performed_by': cursor_actor}
        valid_aoci = receipt | {'state': 'checked', 'host': 'cursor-cli', 'performed_by': cursor_actor}
        for memory, aoci in [(receipt, valid_aoci), (receipt | {'performed_by': actor()}, valid_aoci),
                             (valid_memory, valid_aoci | {'performed_by': actor()})]:
            with self.subTest(memory=memory, aoci=aoci):
                with self.assertRaises(ControlError):
                    self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution,
                                                     verified['evidence'], memory, aoci)
                self.assertEqual(self.controller.result(task['task_id'])['acceptance'], 'pending')

    def test_nonzero_exit_with_success_result_fails(self):
        task = self.submit('nonzero')
        self.assertEqual(self.wait(task)['state'], 'failed')
        self.assertEqual(self.controller.result(task['task_id'])['exit_code'], 7)

    def test_missing_terminal_result_is_incomplete(self):
        self.assertEqual(self.wait(self.submit('missing'))['state'], 'incomplete')

    def test_malformed_unknown_and_cursor_no_repetition(self):
        task = self.submit('malformed')
        status = self.wait(task)
        self.assertEqual(status['state'], 'succeeded')
        events = self.controller.status(task['task_id'])
        self.assertTrue(any(e['action'] == 'diagnostic' for e in events['events']))
        self.assertTrue(any(e['data'].get('type') == 'future_event' for e in events['events']))
        self.assertEqual(self.controller.watch(task['task_id'], events['event_cursor'], 0)['events'], [])
        with self.assertRaises(ControlError):
            self.controller.watch(task['task_id'], wait_seconds=31)

    def test_overlap_rejected_and_stop_confirms_child_tree(self):
        task = self.submit('child')
        deadline = time.monotonic() + 6
        while not (self.workspace / 'child.pid').exists() and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertTrue((self.workspace / 'child.pid').exists())
        nested = self.workspace / 'nested'
        nested.mkdir()
        with self.assertRaises(ControlError) as error:
            self.controller.submit(self.contract(workspace=str(nested)))
        self.assertEqual(error.exception.code, 'workspace_busy')
        self.controller.stop(task['task_id'])
        state = self.wait(task)
        self.assertEqual(state['state'], 'stopped')
        self.assertTrue(state['tree_quiescent'])
        child_pid = int((self.workspace / 'child.pid').read_text())
        if os.name == 'nt':
            import ctypes
            handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, child_pid)
            if handle:
                exit_code = ctypes.c_ulong()
                ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
                ctypes.windll.kernel32.CloseHandle(handle)
                self.assertNotEqual(exit_code.value, 259)

    def test_timeout_is_durable_and_tree_quiescent(self):
        state = self.wait(self.submit('sleep', timeout_seconds=0.2))
        self.assertEqual(state['state'], 'timed_out')
        self.assertTrue(state['tree_quiescent'])

    def test_small_flushed_event_is_visible_before_executor_exits(self):
        task = self.submit('sleep')
        deadline = time.monotonic() + 2
        status = self.controller.status(task['task_id'])
        while time.monotonic() < deadline and not status['session_id']:
            time.sleep(0.05)
            status = self.controller.status(task['task_id'])
        self.assertEqual(status['state'], 'running')
        self.assertEqual(status['session_id'], 'fixture-session', 'flushed init must stream before EOF')

    def test_continuous_stdout_does_not_starve_stop_request(self):
        task = self.submit('flood', timeout_seconds=10)
        time.sleep(0.3)
        started = time.monotonic()
        self.controller.stop(task['task_id'])
        state = self.wait(task)
        self.assertEqual(state['state'], 'stopped')
        self.assertLess(time.monotonic() - started, 8)
        self.assertTrue(state['tree_quiescent'])

    def test_agent_disappearing_before_worker_spawn_is_terminal_failure(self):
        ephemeral = self.root / 'ephemeral_agent.py'
        text = Path(__file__).with_name('fixture_agent.py').read_text(encoding='utf-8')
        text = text.replace("print('Authenticated')", "print('Authenticated'); pathlib.Path(__file__).unlink()")
        ephemeral.write_text(text, encoding='utf-8')
        self.controller = Controller(self.root / 'data', ephemeral)
        task = self.submit()
        state = self.wait(task)
        self.assertEqual(state['state'], 'failed')
        self.assertTrue(state['tree_quiescent'])
        result = self.controller.result(task['task_id'])
        self.assertEqual(result['executed_by']['source'], 'unknown')
        self.assertEqual(result['executed_by']['id'], 'unknown')
        verified, attribution = self.receipt(task)
        rejected = self.controller.record_acceptance(task['task_id'], task['run_id'], 'rejected', attribution, verified['evidence'])
        report = Path(rejected['report_path']).read_text(encoding='utf-8')
        self.assertNotIn('process:None', report)
        self.assertIn('"source": "unknown"', report)

    @unittest.skipUnless(os.name == 'nt', 'Windows broker failure path')
    def test_uncertain_scheduler_ack_retains_starting_lease(self):
        from cursor_runtime import processes
        with patch.object(processes, 'in_windows_job', return_value=True), patch.object(
                processes.subprocess, 'run', side_effect=subprocess.TimeoutExpired('scheduler', 20)):
            with self.assertRaises(ControlError) as error:
                self.controller.submit(self.contract())
        self.assertEqual(error.exception.code, 'launch_uncertain')
        task = self.controller.list_tasks()['tasks'][0]
        state = self.controller.status(task['task_id'])
        self.assertEqual(state['state'], 'starting')
        self.assertFalse(state['tree_quiescent'])
        self.assertTrue((self.controller._run_dir(task['task_id'], task['run_id']) / 'launch-diagnostic.json').is_file())
        with self.controller._db() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM leases').fetchone()[0], 1)
        # Timeout injection never invoked the scheduler: there is no external worker to clean up.

    @unittest.skipUnless(os.name == 'nt', 'Windows broker failure path')
    def test_scheduler_post_ack_recording_failure_retains_lease(self):
        from cursor_runtime import processes
        write_text = Path.write_text

        def fail_registration_record(path, *args, **kwargs):
            if path.name == 'broker-registered.json':
                raise OSError('injected registration receipt disk failure')
            return write_text(path, *args, **kwargs)

        def acknowledged(command, **kwargs):
            payload = json.loads(Path(command[command.index('-EnvelopePath') + 1]).read_text(encoding='utf-8'))
            return subprocess.CompletedProcess(command, 0, json.dumps({'scheduled': True, 'task_name': payload['task_name'],
                                                'sid': 'S-1-fixture', 'instance_id': 'fixture'}).encode(), b'')

        with patch.object(processes, 'in_windows_job', return_value=True), patch.object(processes.subprocess, 'run', acknowledged), patch.object(Path, 'write_text', fail_registration_record):
            with self.assertRaises(ControlError) as error:
                self.controller.submit(self.contract())
        self.assertEqual(error.exception.code, 'launch_uncertain')
        task = self.controller.list_tasks()['tasks'][0]
        self.assertEqual(task['state'], 'starting')
        self.assertFalse(task['tree_quiescent'])
        with self.controller._db() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM leases').fetchone()[0], 1)

    def test_reaper_thread_failure_is_a_launch_uncertainty(self):
        from cursor_runtime import processes
        with patch.object(processes, 'in_windows_job', return_value=False), patch.object(processes.threading.Thread, 'start', side_effect=RuntimeError('injected reaper failure')):
            with self.assertRaises(ControlError) as error:
                self.controller.submit(self.contract('sleep', timeout_seconds=1))
        task = self.controller.list_tasks()['tasks'][0]
        self.tasks.append(task)
        # Wait for the independent worker on the fixed implementation; red may reject
        # startup because the coordinator prematurely marked the row terminal.
        time.sleep(1.5)
        self.assertEqual(error.exception.code, 'launch_uncertain')
        state = self.wait(task)
        self.assertEqual(state['state'], 'timed_out')
        self.assertTrue(state['tree_quiescent'])

    def test_detached_worker_survives_launcher_disconnection(self):
        contract_file = self.root / 'contract.json'
        contract_file.write_text(json.dumps(self.contract(), ensure_ascii=False), encoding='utf-8')
        command = [sys.executable, str(SCRIPTS / 'cursor_control.py'), '--data-dir', str(self.root / 'data'),
                   '--agent-path', str(Path(__file__).with_name('fixture_agent.py')), 'submit', '--contract-file', str(contract_file)]
        completed = subprocess.run(command, capture_output=True, encoding='utf-8', timeout=10)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        task = json.loads(completed.stdout)
        self.tasks.append(task)
        self.assertEqual(self.wait(task)['state'], 'succeeded')

    def test_invalid_cli_arguments_return_nonzero_json_diagnostic(self):
        command = [sys.executable, str(SCRIPTS / 'cursor_control.py'), 'status']
        done = subprocess.run(command, capture_output=True, encoding='utf-8', timeout=5)
        self.assertNotEqual(done.returncode, 0)
        self.assertTrue(done.stdout.strip(), 'missing CLI arguments must produce a JSON diagnostic')
        self.assertEqual(json.loads(done.stdout)['error']['code'], 'invalid_arguments')

    def test_acceptance_receipt_linkage_and_resume_invalidation(self):
        task = self.submit(allow_writes=True, evidence_paths=['artifact.txt'],
                           verification_commands=[[sys.executable, '-c', 'print("verified")']])
        self.wait(task)
        verified, attribution = self.receipt(task)
        accepted = self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])
        self.assertEqual(accepted['decision'], 'accepted')
        self.assertTrue(Path(accepted['report_path']).is_file())
        old_ids = [e['id'] for e in self.controller.audit(task['task_id'])['records']]
        resumed = self.controller.resume(task['task_id'], 'follow-up 中文')
        self.assertNotEqual(resumed['run_id'], task['run_id'])
        self.wait(resumed)
        result = self.controller.result(task['task_id'])
        self.assertEqual(result['acceptance'], 'pending')
        self.assertIsNone(result['memory_receipt'])
        self.assertIsNone(result['aoci_receipt'])
        self.assertTrue(set(old_ids).issubset(e['id'] for e in self.controller.audit(task['task_id'])['records']))
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])
        self.assertEqual(error.exception.code, 'stale_run')

    def test_external_change_rejects_stale_hashes(self):
        task = self.submit(allow_writes=True, evidence_paths=['artifact.txt'])
        self.wait(task)
        verified, attribution = self.receipt(task)
        (self.workspace / 'artifact.txt').write_text('external change')
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])
        self.assertEqual(error.exception.code, 'version_conflict')

    def test_memory_aoci_required_receipts_and_actor_claims_declared(self):
        memory_path = self.workspace / 'docs' / 'memory' / 'MEMORY.md'
        memory_path.parent.mkdir(parents=True)
        memory_path.write_text('authorized existing memory')
        task = self.submit(allow_writes=True, evidence_paths=['artifact.txt', 'docs/memory/MEMORY.md'],
                           memory={'required': True, 'mode': 'coordinator', 'pending_paths': ['docs/memory/MEMORY.md']},
                           aoci={'required': True, 'host': 'codex'})
        self.wait(task)
        verified, attribution = self.receipt(task)
        with self.assertRaises(ControlError):
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])
        memory_evidence = [e for e in verified['evidence'] if e.get('relative_path') == 'docs/memory/MEMORY.md']
        memory = {'task_id': task['task_id'], 'run_id': task['run_id'], 'state': 'completed', 'evidence': memory_evidence,
                  'performed_by': actor(role='maintenance')}
        aoci = {'task_id': task['task_id'], 'run_id': task['run_id'], 'state': 'checked', 'host': 'codex', 'evidence': memory_evidence,
                'performed_by': actor(role='checker')}
        accepted = self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'], memory, aoci)
        audit = self.controller.audit(task['task_id'])['records']
        decisions = [e for e in audit if e['action'] == 'decision']
        self.assertEqual(decisions[-1]['actor']['source'], 'declared')
        self.assertEqual(decisions[-1]['data']['attribution']['executed_by']['source'], 'observed')
        self.assertEqual(decisions[-1]['data']['attribution']['reviewed_by']['source'], 'declared')
        self.assertIn(accepted['memory_receipt_id'], [e['id'] for e in audit])
        self.assertIn(accepted['aoci_receipt_id'], [e['id'] for e in audit])

    def test_failed_verification_blocks_acceptance_but_allows_rejection(self):
        task = self.submit(verification_commands=[[sys.executable, '-c', 'raise SystemExit(3)']])
        self.wait(task)
        verified, attribution = self.receipt(task)
        self.assertFalse(verified['passed'])
        with self.assertRaises(ControlError):
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])
        receipt = self.controller.record_acceptance(task['task_id'], task['run_id'], 'rejected', attribution, verified['evidence'])
        self.assertEqual(receipt['decision'], 'rejected')

    def test_doctor_capabilities_and_validation(self):
        doctor = self.controller.doctor()
        self.assertTrue(doctor['available'])
        self.assertTrue(doctor['supported_flags']['--force'])
        capability = self.controller.capabilities(str(self.workspace), ['skill-that-does-not-exist'])
        self.assertFalse(capability['skills'][0]['available'])
        with self.assertRaises(ControlError):
            self.controller.submit(self.contract(mode='agent'))
        with self.assertRaises(ControlError):
            self.controller.submit(self.contract(evidence_paths=['../outside']))

    def test_explicit_readonly_trust_uses_trust_and_not_write_permission(self):
        self.assertTrue(self.controller.doctor()['supported_flags'].get('--trust'))
        task = self.submit(trust_workspace=True)
        self.assertEqual(self.wait(task)['state'], 'succeeded')
        self.assertFalse(json.loads(Path(self.controller.result(task['task_id'])['contract_path']).read_text(encoding='utf-8'))['allow_writes'])
        with self.assertRaises(ControlError):
            self.controller.submit(self.contract(trust_workspace='yes'))

    def test_typed_cursor_tool_call_updates_recent_action(self):
        task = self.submit('typed-tool')
        state = self.wait(task)
        self.assertEqual(state['recent_tool'], 'readToolCall')

    def test_executor_prompt_requires_current_run_signed_pending_report(self):
        task = self.submit('report-signature')
        self.assertEqual(self.wait(task)['state'], 'succeeded')
        resumed = self.controller.resume(task['task_id'], 'Retain a signed pending report for this new run')
        self.assertEqual(self.wait(resumed)['state'], 'succeeded')

    def test_error_terminal_does_not_succeed(self):
        self.assertEqual(self.wait(self.submit('terminal-error'))['state'], 'failed')

    def test_terminal_success_without_result_field_is_invalid(self):
        self.assertEqual(self.wait(self.submit('invalid-terminal'))['state'], 'failed')

    def test_contract_file_mutation_invalidates_verification(self):
        task = self.submit()
        self.wait(task)
        result = self.controller.result(task['task_id'])
        contract_path = Path(result['contract_path'])
        revised = json.loads(contract_path.read_text(encoding='utf-8'))
        revised['objective'] = 'externally substituted task'
        contract_path.write_text(json.dumps(revised), encoding='utf-8')
        verified, attribution = self.receipt(task)
        self.assertFalse(verified['passed'], 'contract revision file must match immutable registered data')
        with self.assertRaises(ControlError):
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])

    def test_readonly_verification_includes_actual_execution_log_hashes(self):
        task = self.submit()
        self.wait(task)
        verified, attribution = self.receipt(task)
        self.assertTrue(verified['evidence'], 'even readonly work needs observed execution evidence')
        execution = [entry for entry in verified['evidence'] if entry['kind'] == 'execution']
        self.assertEqual(len(execution), 1)
        Path(execution[0]['path']).write_text('external alteration')
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])
        self.assertEqual(error.exception.code, 'version_conflict')

    def test_verification_timeout_contains_child_and_rejection(self):
        command = [sys.executable, '-c', 'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c","import time; time.sleep(90)"]); time.sleep(90)']
        task = self.submit(verification_commands=[command], verification_timeout_seconds=0.15)
        self.wait(task)
        verified, attribution = self.receipt(task)
        self.assertFalse(verified['passed'])
        command_evidence = [e for e in verified['evidence'] if e['kind'] == 'command'][0]
        self.assertTrue(command_evidence['timed_out'])
        self.assertTrue(command_evidence['tree_quiescent'])
        result = self.controller.record_acceptance(task['task_id'], task['run_id'], 'rejected', attribution, verified['evidence'])
        self.assertEqual(result['decision'], 'rejected')

    def test_existing_report_not_overwritten_and_decision_not_committed(self):
        report = self.workspace / 'user-report.md'
        report.write_text('preserve user text')
        task = self.submit(report_path=str(report))
        self.wait(task)
        verified, attribution = self.receipt(task)
        with self.assertRaises(ControlError) as error:
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])
        self.assertEqual(error.exception.code, 'report_exists')
        self.assertEqual(report.read_text(), 'preserve user text')
        self.assertEqual(self.controller.result(task['task_id'])['acceptance'], 'pending')
        with self.assertRaises(ControlError):
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'], report_path=str(self.root / 'outside.md'))

    def test_declared_human_decider_and_forged_executor_rejected(self):
        task = self.submit()
        self.wait(task)
        verified, attribution = self.receipt(task)
        attribution['decided_by']['kind'] = 'user'
        with self.assertRaises(ControlError):
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])
        attribution['decided_by']['kind'] = 'agent'
        attribution['executed_by']['id'] = 'imagined-cursor-session'
        with self.assertRaises(ControlError):
            self.controller.record_acceptance(task['task_id'], task['run_id'], 'accepted', attribution, verified['evidence'])

    @unittest.skipUnless(os.name == 'nt', 'PowerShell envelope is Windows-specific')
    def test_powershell_envelope_preserves_unicode_and_quoted_arguments(self):
        wrapper = self.root / 'agent.ps1'
        python_literal = sys.executable.replace("'", "''")
        fixture_literal = str(Path(__file__).with_name('fixture_agent.py')).replace("'", "''")
        wrapper.write_text("& '" + python_literal + "' '" + fixture_literal + "' @args\nexit $LASTEXITCODE\n", encoding='utf-8-sig')
        self.controller = Controller(self.root / 'data', wrapper)
        task = self.submit('中文\n"quoted" $() `literal`')
        self.assertEqual(self.wait(task)['state'], 'succeeded')

    def test_probe_timeout_kills_own_helper_tree(self):
        slow = self.root / 'slow_agent.py'
        slow.write_text('import json,os,pathlib,subprocess,sys,time\nchild=subprocess.Popen([sys.executable,"-c","import time; time.sleep(90)"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\npathlib.Path(sys.argv[-1]).write_text(json.dumps([os.getpid(),child.pid]))\ntime.sleep(90)\n', encoding='utf-8')
        probe = Controller(self.root / 'probe-data', slow)
        pid_file = self.root / 'probe-pids.json'
        with self.assertRaises(ControlError) as error:
            probe._probe(['--help', str(pid_file)])
        self.assertEqual(error.exception.code, 'probe_timeout')
        if os.name == 'nt':
            import ctypes
            from ctypes import wintypes
            kernel = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            kernel.OpenProcess.restype = wintypes.HANDLE
            kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
            kernel.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
            kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
            kernel.CloseHandle.argtypes = [wintypes.HANDLE]
            for pid in json.loads(pid_file.read_text()):
                handle = kernel.OpenProcess(0x1000 | 0x100000 | 1, False, pid)
                if handle:
                    code = wintypes.DWORD()
                    kernel.GetExitCodeProcess(handle, ctypes.byref(code))
                    # Keep the red-stage test from leaving its own observed child alive.
                    if code.value == 259:
                        kernel.TerminateProcess(handle, 1)
                        kernel.WaitForSingleObject(handle, 5000)
                    kernel.CloseHandle(handle)
                    self.assertNotEqual(code.value, 259, 'timed-out probe left a child running')


if __name__ == '__main__':
    unittest.main()
