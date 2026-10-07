"""One detached worker per execution; durable stop requests remain in SQLite."""
import json
import os
import queue
import subprocess
import threading
import time

from .core import Controller, ControlError, encoded, now, digest_file
from .processes import ManagedProcess


def run_worker(controller, task_id, run_id):
    with controller._db(write=True) as db:
        row = controller._current(db, task_id, run_id)
        if row['state'] != 'starting':
            return
        contract = json.loads(row['contract'])
        # A duplicate internal worker cannot become a second process writer.
        db.execute('UPDATE runs SET state=?,started_at=?,worker_pid=? WHERE run_id=?', ('running', now(), os.getpid(), run_id))
        controller._append(db, task_id, run_id, 'worker_started', data={'contract_revision': row['revision'], 'worker_pid': os.getpid()})
    directory = controller._run_dir(task_id, run_id)
    contract_path = directory / 'contract.json'
    prompt = ('role=executor. Read and follow the UTF-8 task contract at the exact path below. '
              'It defines objective, scope, strategy, selected skill paths, write ownership and acceptance. '
              'Respect each host/path owner. Do not recursively dispatch cursor-controller tasks. '
              'Report actual tools, test evidence, changed artifacts, and memory_delta; final acceptance belongs to the coordinator. '
              'Every executor report must include a responsibility block: '
              f'task_id={task_id}, run_id={run_id}, contract_revision={row["revision"]}; '
              'executed_by=Cursor Agent (observed session if actually known, otherwise unknown); '
              'authored_by=Cursor Agent (declared, host=cursor-cli); '
              'reviewed_by=pending coordinator; decided_by=pending coordinator; decision=pending coordinator acceptance. '
              'List actual command/file evidence and only known audit receipt references; mark absent IDs unknown/pending. '
              'Never fabricate audit IDs, reviewer decisions or human approval.\n'
              'CONTRACT_FILE=' + str(contract_path) + '\n')
    arguments = ['--workspace', contract['workspace'], '--print', '--output-format', 'stream-json']
    if contract['mode'] != 'agent':
        arguments += ['--mode', contract['mode']]
    if contract['allow_writes']:
        arguments.append('--force')
    if contract.get('trust_workspace'):
        arguments.append('--trust')
    if contract.get('model'):
        arguments += ['--model', contract['model']]
    if contract.get('resume_session_id'):
        arguments += ['--resume', contract['resume_session_id']]
    arguments.append(prompt)
    messages = queue.Queue(maxsize=256)
    proc, terminal, session, exit_code = None, None, None, None
    reason, quiescent = None, False
    stdout_path, stderr_path = directory / 'stdout.ndjson', directory / 'stderr.log'

    def pump(pipe, raw, parse):
        try:
            # Preserve every byte, but cap in-memory line assembly at one MiB.
            pending = bytearray()
            oversize = False
            while True:
                block = pipe.read1(4096)
                if not block:
                    break
                raw.write(block)
                if not parse:
                    continue
                for part_index, part in enumerate(block.split(b'\n')):
                    if part_index:
                        if not oversize:
                            messages.put(bytes(pending))
                        else:
                            messages.put(b'__CURSOR_OVERSIZE_EVENT__')
                        pending.clear()
                        oversize = False
                    if not oversize:
                        pending.extend(part)
                        if len(pending) > 1048576:
                            pending.clear()
                            oversize = True
            if pending and not oversize:
                messages.put(bytes(pending))
        finally:
            pipe.close()

    def record_event(raw):
        nonlocal terminal, session
        try:
            event = json.loads(raw.decode('utf-8'))
            if not isinstance(event, dict):
                raise ValueError('Event must be a JSON object')
        except (ValueError, UnicodeError):
            with controller._db(write=True) as db:
                controller._append(db, task_id, run_id, 'diagnostic', data={'reason': 'invalid_ndjson', 'preview': raw.decode('utf-8', 'replace')[:2048]})
            return
        event_session = event.get('session_id')
        if isinstance(event_session, str) and event_session:
            if session and event_session != session:
                with controller._db(write=True) as db:
                    controller._append(db, task_id, run_id, 'diagnostic', data={'reason': 'session_id_changed', 'previous': session, 'current': event_session})
            session = event_session
        if event.get('type') == 'result':
            terminal = event
        tool = event.get('tool_name')
        if not tool and isinstance(event.get('tool_call'), dict):
            tool = event['tool_call'].get('name')
            if not tool:
                tool = next((name for name, detail in event['tool_call'].items()
                             if name.endswith('ToolCall') and isinstance(detail, dict)), None)
        if tool is not None and not isinstance(tool, str):
            tool = None
        stamp = now()
        with controller._db(write=True) as db:
            controller._append(db, task_id, run_id, 'stdout_event', data=event, event_time=stamp)
            db.execute('UPDATE runs SET last_event_at=?,session_id=COALESCE(?,session_id),recent_tool=COALESCE(?,recent_tool) WHERE run_id=?',
                       (stamp, session, tool[:256] if tool else None, run_id))

    threads = []
    try:
        with stdout_path.open('wb', buffering=0) as stdout, stderr_path.open('wb', buffering=0) as stderr:
            if contract_path.read_text(encoding='utf-8') != row['contract']:
                raise ControlError('version_conflict', 'Task contract file changed before executor launch')
            command = controller._argv(arguments, directory)
            proc = ManagedProcess(command, contract['workspace'], subprocess.PIPE, subprocess.PIPE)
            with controller._db(write=True) as db:
                db.execute('UPDATE runs SET pid=? WHERE run_id=?', (proc.pid, run_id))
                controller._append(db, task_id, run_id, 'process_started', data={'pid': proc.pid, 'containment': 'windows_job_suspended_assignment' if proc.job else 'posix_process_group'})
            for pipe, raw, parse in ((proc.process.stdout, stdout, True), (proc.process.stderr, stderr, False)):
                thread = threading.Thread(target=pump, args=(pipe, raw, parse), daemon=True)
                thread.start()
                threads.append(thread)
            deadline = time.monotonic() + contract['timeout_seconds']
            while True:
                for _ in range(100):
                    try:
                        record_event(messages.get_nowait())
                    except queue.Empty:
                        break
                with controller._db() as db:
                    stop = controller._current(db, task_id, run_id)['stop_requested']
                if stop:
                    reason = 'stopped'
                    break
                if proc.poll() is not None:
                    exit_code = proc.poll()
                    break
                if time.monotonic() >= deadline:
                    reason = 'timed_out'
                    with controller._db(write=True) as db:
                        db.execute('UPDATE runs SET stop_requested=1 WHERE run_id=?', (run_id,))
                        controller._append(db, task_id, run_id, 'timeout_stop_requested', data={'timeout_seconds': contract['timeout_seconds']})
                    break
                time.sleep(0.05)
            quiescent = proc.finish_tree()
            exit_code = proc.poll() if exit_code is None else exit_code
            # Drain concurrently so a full queue never blocks stdout-pump joining.
            end = time.monotonic() + 5
            while (any(t.is_alive() for t in threads) or not messages.empty()) and time.monotonic() < end:
                try:
                    record_event(messages.get(timeout=0.05))
                except queue.Empty:
                    pass
            for thread in threads:
                thread.join(timeout=0.1)
            if any(t.is_alive() for t in threads):
                quiescent = False
    except BaseException as error:
        reason = 'failed'
        with controller._db(write=True) as db:
            controller._append(db, task_id, run_id, 'worker_error', data={'type': type(error).__name__, 'error': str(error)})
        if proc:
            try:
                quiescent = proc.finish_tree()
            except Exception:
                quiescent = False
        else:
            quiescent = True  # Process startup failed before any executor was running.
    finally:
        if proc:
            proc.close()
    success = (exit_code == 0 and terminal is not None and terminal.get('subtype') == 'success'
               and terminal.get('is_error') is False and 'result' in terminal and isinstance(terminal['result'], str))
    state = 'stopped_unconfirmed' if not quiescent else (reason or ('succeeded' if success else ('failed' if exit_code != 0 or terminal else 'incomplete')))
    final_result = terminal.get('result') if terminal else None
    if final_result is not None and not isinstance(final_result, str):
        final_result = encoded(final_result)
    with controller._db(write=True) as db:
        db.execute('UPDATE runs SET state=?,ended_at=?,exit_code=?,result=?,tree_quiescent=? WHERE run_id=?',
                   (state, now(), exit_code, final_result, int(quiescent), run_id))
        evidence = [{'path': str(path), 'sha256': digest_file(path)} for path in (stdout_path, stderr_path) if path.is_file()]
        controller._append(db, task_id, run_id, 'execution', data={'state': state, 'exit_code': exit_code,
                           'valid_success_result': success, 'tree_quiescent': quiescent, 'session_id': session}, evidence=evidence)
        if quiescent:
            db.execute('DELETE FROM leases WHERE token=?', (run_id,))
