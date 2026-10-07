"""Deterministic local execution/audit core. All claims preserve their source."""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import time
import uuid

from .processes import ManagedProcess, spawn_detached, LaunchUncertain, console_python

SCRIPTS = Path(__file__).resolve().parents[1]
ACTIVE = ('starting', 'running')
SERVICE = {'id': 'cursor-controller', 'kind': 'service', 'host': 'local', 'role': 'runtime', 'source': 'observed'}


class ControlError(Exception):
    def __init__(self, code, message, details=None):
        super().__init__(message)
        self.message = message
        self.code, self.details = code, details or {}

    def as_dict(self):
        return {'error': {'code': self.code, 'message': str(self), 'details': self.details}}


def now():
    return datetime.now(timezone.utc).isoformat()


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def identifier():
    return uuid.uuid4().hex


def declared_actor(value):
    if not isinstance(value, dict) or any(not isinstance(value.get(k), str) or not value[k].strip()
                                           for k in ('id', 'kind', 'host', 'role')):
        raise ControlError('invalid_actor', 'Actor requires nonempty id, kind, host and role')
    if value['kind'] not in ('agent', 'user', 'service'):
        raise ControlError('invalid_actor', 'Unsupported actor kind')
    return {k: value[k] for k in ('id', 'kind', 'host', 'role')} | {'source': 'declared'}


def contained(base, path):
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def workspace_path(value):
    if not isinstance(value, str) or not Path(value).is_absolute() or not Path(value).is_dir():
        raise ControlError('invalid_workspace', 'Workspace must be an absolute existing directory')
    return Path(value).resolve()


def workspace_key(value):
    return os.path.normcase(str(Path(value).resolve()))


def overlaps(left, right):
    try:
        return os.path.commonpath([left, right]) in (left, right)
    except ValueError:
        return False


def project_memory(work):
    """Observe only known entries; metadata is data, never executable instructions."""
    observed = {'present': False, 'entrypoint': None, 'root': None, 'layout': None,
                'memory_schema_version': None, 'aoci_state': 'unknown'}
    entries = (('docs/memory/MEMORY.md', 'docs/memory'), ('docs/memory/ROOT-MEMORY.md', 'docs/memory'),
               ('memory/kit/MEMORY.md', 'memory/kit'), ('ROOT-MEMORY.md', 'workspace_root'))
    for relative, layout in entries:
        entry = work / relative
        try:
            # lstat distinguishes a broken/escaping link from genuinely missing Kit.
            entry.lstat()
        except FileNotFoundError:
            continue
        except OSError as error:
            return observed | {'present': None, 'diagnostic': {'code': 'entry_unreadable', 'path': str(entry), 'message': str(error)}}
        try:
            resolved = entry.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            return observed | {'present': None, 'diagnostic': {'code': 'entry_unreadable', 'path': str(entry), 'message': str(error)}}
        if not contained(work, resolved):
            return observed | {'present': None, 'diagnostic': {'code': 'entry_outside_workspace', 'path': str(entry)}}
        observed.update(present=True, entrypoint=str(resolved), root=str(resolved.parent), layout=layout)
        try:
            with resolved.open('rb') as stream:
                raw = stream.read(262145)
            text = raw[:262144].decode('utf-8-sig')
        except (OSError, UnicodeError) as error:
            return observed | {'diagnostic': {'code': 'entry_unreadable', 'path': str(entry), 'message': str(error)}}
        if len(raw) > 262144:
            observed['diagnostic'] = {'code': 'entry_truncated', 'path': str(entry), 'limit_bytes': 262144}
        # A progress/tool version is not a declaration of this memory's schema.
        schema = re.search(r'本记忆按\s*kit\s+(v?\d+\.\d+(?:\.\d+)?)\s*建立', text, re.IGNORECASE)
        if not schema:
            schema = re.search(r'^\s*(?:memory_schema_version|memory[- ]schema[- ]version)\s*:\s*["\']?(v?\d+\.\d+(?:\.\d+)?)\b', text, re.IGNORECASE | re.MULTILINE)
        if schema:
            observed['memory_schema_version'] = schema.group(1)
        for line in text.splitlines():
            if '<!-- kit:aoci-status -->' not in line:
                continue
            status = line.replace('<!-- kit:aoci-status -->', '').strip()
            observed['aoci_status_line'] = status[:1000]
            lower = status.lower()
            if any(word in lower for word in ('未启用', '已禁用', '不启用', '已停用')) or re.search(r'\bdisabled\b', lower):
                observed['aoci_state'] = 'disabled'
            elif any(word in lower for word in ('未初始化', 'not initialized', 'uninitialized')) and any(word in lower for word in ('已绑定', '已配置', 'configured', 'bound')):
                observed['aoci_state'] = 'configured_not_initialized'
            elif '已启用' in lower or re.search(r'\benabled\b', lower):
                observed['aoci_state'] = 'enabled'
            break
        return observed
    return observed


class Controller:
    def __init__(self, data_dir=None, agent_path=None):
        default = (Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'CursorController'
                   if os.name == 'nt' else Path.home() / '.local' / 'share' / 'cursor-controller')
        self.data_dir = Path(data_dir or default).expanduser().resolve()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / 'state.sqlite3'
        self.agent_path = str(Path(agent_path).expanduser().resolve()) if agent_path else None
        with self._db() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS tasks(task_id TEXT PRIMARY KEY,workspace TEXT NOT NULL,current_run TEXT NOT NULL,revision INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS runs(run_id TEXT PRIMARY KEY,task_id TEXT NOT NULL,revision INTEGER NOT NULL,contract TEXT NOT NULL,
                state TEXT NOT NULL,session_id TEXT,pid INTEGER,worker_pid INTEGER,started_at TEXT,ended_at TEXT,last_event_at TEXT,
                recent_tool TEXT,exit_code INTEGER,result TEXT,tree_quiescent INTEGER NOT NULL DEFAULT 0,stop_requested INTEGER NOT NULL DEFAULT 0,
                acceptance TEXT NOT NULL DEFAULT 'pending',memory_receipt TEXT,aoci_receipt TEXT,decision_id INTEGER,verification_id INTEGER);
            CREATE TABLE IF NOT EXISTS leases(token TEXT PRIMARY KEY,task_id TEXT NOT NULL,run_id TEXT NOT NULL,workspace TEXT NOT NULL,phase TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,task_id TEXT NOT NULL,run_id TEXT NOT NULL,action TEXT NOT NULL,
                actor TEXT NOT NULL,source TEXT NOT NULL,event_time TEXT NOT NULL,recorded_at TEXT NOT NULL,data TEXT NOT NULL,
                evidence_digests TEXT NOT NULL,prev_hash TEXT NOT NULL,hash TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS audit_task ON audit(task_id,id);
            CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit BEGIN SELECT RAISE(ABORT,'audit append-only'); END;
            CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit BEGIN SELECT RAISE(ABORT,'audit append-only'); END;
            ''')

    @contextmanager
    def _db(self, write=False):
        db = sqlite3.connect(self.db_path, timeout=15)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA busy_timeout=15000')
        try:
            if write:
                db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def _append(self, db, task_id, run_id, action, actor=SERVICE, data=None, evidence=None, event_time=None):
        previous = db.execute('SELECT hash FROM audit WHERE task_id=? ORDER BY id DESC LIMIT 1', (task_id,)).fetchone()
        record = {'task_id': task_id, 'run_id': run_id, 'action': action, 'actor': actor, 'source': actor['source'],
                  'event_time': event_time or now(), 'recorded_at': now(), 'data': data or {}, 'evidence_digests': evidence or [],
                  'prev_hash': previous['hash'] if previous else ''}
        record['hash'] = hashlib.sha256(encoded(record).encode('utf-8')).hexdigest()
        values = [encoded(record[k]) if k in ('actor', 'data', 'evidence_digests') else record[k] for k in record]
        cursor = db.execute('INSERT INTO audit(task_id,run_id,action,actor,source,event_time,recorded_at,data,evidence_digests,prev_hash,hash) VALUES (?,?,?,?,?,?,?,?,?,?,?)', values)
        return cursor.lastrowid

    def _current(self, db, task_id, run_id=None):
        task = db.execute('SELECT * FROM tasks WHERE task_id=?', (task_id,)).fetchone()
        if task is None:
            raise ControlError('unknown_task', 'Task not found')
        if run_id is not None and run_id != task['current_run']:
            raise ControlError('stale_run', 'Run no longer matches current task', {'current_run_id': task['current_run']})
        return db.execute('SELECT * FROM runs WHERE run_id=?', (task['current_run'],)).fetchone()

    def _run_dir(self, task_id, run_id):
        # IDs are only looked up from the database, never trusted as path components.
        return self.data_dir / 'tasks' / task_id / run_id

    def _lease(self, db, task_id, run_id, workspace, token, phase):
        key = workspace_key(workspace)
        for row in db.execute('SELECT * FROM leases'):
            if overlaps(key, row['workspace']):
                raise ControlError('workspace_busy', 'An overlapping workspace is leased', {'task_id': row['task_id'], 'run_id': row['run_id'], 'phase': row['phase']})
        db.execute('INSERT INTO leases VALUES (?,?,?,?,?)', (token, task_id, run_id, key, phase))

    def _agent(self):
        candidate = self.agent_path or shutil.which('agent') or shutil.which('cursor-agent')
        if not candidate:
            # The standard Windows installation is sometimes absent from PATH.
            local = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'cursor-agent' / 'agent.ps1'
            if local.is_file():
                candidate = str(local)
        if not candidate or not Path(candidate).is_file():
            raise ControlError('agent_missing', 'Cursor Agent CLI not found; specify agent_path')
        candidate = Path(candidate).resolve()
        if candidate.stem.lower() == 'cursor':
            raise ControlError('editor_not_agent', 'The editor cursor command cannot execute controller tasks')
        return candidate

    def _argv(self, args, envelope_dir):
        agent = self._agent()
        if agent.suffix.lower() == '.py':
            return [console_python(sys.executable), str(agent), *args]
        if agent.suffix.lower() == '.ps1':
            powershell = shutil.which('pwsh') or shutil.which('powershell')
            if not powershell:
                raise ControlError('powershell_missing', 'PowerShell is required for the installed agent.ps1')
            envelope = Path(envelope_dir) / ('envelope-' + identifier() + '.json')
            envelope.parent.mkdir(parents=True, exist_ok=True)
            envelope.write_text(encoded({'agent_path': str(agent), 'arguments': args}), encoding='utf-8')
            return [powershell, '-NoLogo', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File',
                    str(SCRIPTS / 'cursor_launcher.ps1'), '-EnvelopePath', str(envelope)]
        return [str(agent), *args]

    def _probe(self, args):
        import tempfile
        with tempfile.TemporaryDirectory(prefix='cursor-probe-') as directory:
            process = None
            try:
                command = self._argv(args, directory)
                out_path, err_path = Path(directory) / 'stdout', Path(directory) / 'stderr'
                with out_path.open('wb', buffering=0) as out, err_path.open('wb', buffering=0) as err:
                    process = ManagedProcess(command, Path(directory), out, err)
                    deadline = time.monotonic() + 15
                    while process.poll() is None and time.monotonic() < deadline:
                        time.sleep(0.05)
                    timed_out = process.poll() is None
                    if not process.finish_tree():
                        raise ControlError('probe_unconfirmed', 'Capability helper tree termination could not be confirmed')
                    if timed_out:
                        raise ControlError('probe_timeout', 'Agent capability probe timed out')
                text = out_path.read_bytes()[:1048576] + err_path.read_bytes()[:1048576]
                return process.poll(), text.decode('utf-8', 'replace')
            finally:
                if process:
                    process.close()

    def doctor(self):
        try:
            agent = self._agent()
            code, help_text = self._probe(['--help'])
            version_code, version = self._probe(['--version'])
            auth_code, auth_text = self._probe(['status'])
            lower = auth_text.lower()
            auth = 'authenticated' if auth_code == 0 and ('authenticated' in lower or 'logged in' in lower) and 'not logged' not in lower else 'unknown'
            if 'not authenticated' in lower or 'not logged in' in lower or 'unauthenticated' in lower:
                auth = 'unauthenticated'
            flags = {flag: flag in help_text for flag in ('--workspace', '--print', '--output-format', '--mode', '--force', '--resume', '--model', '--trust')}
            return {'available': code == 0, 'agent_path': str(agent), 'version': version.strip()[:200] if version_code == 0 else None,
                    'authentication': auth, 'supported_flags': flags, 'help_checked': code == 0,
                    'runtime_protocol_verified': False, 'subagents': 'not_verified'}
        except ControlError as error:
            return {'available': False, 'authentication': 'unknown', **error.as_dict()}

    def capabilities(self, workspace, skill_names):
        work = workspace_path(workspace)
        if not isinstance(skill_names, list) or any(not isinstance(n, str) or not n or '/' in n or '\\' in n or n in ('.', '..') for n in skill_names):
            raise ControlError('invalid_skills', 'Skill names must be simple directory names')
        roots = [work / '.cursor' / 'skills', Path.home() / '.cursor' / 'skills', Path.home() / '.agents' / 'skills',
                 Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')) / 'skills']
        skills = []
        for name in skill_names:
            paths = [str(root / name / 'SKILL.md') for root in roots if (root / name / 'SKILL.md').is_file()]
            skills.append({'name': name, 'available': bool(paths), 'paths': paths, 'source': 'observed', 'host': 'local-filesystem',
                           'invocation_verified': False})
        return {'workspace': str(work), 'doctor': self.doctor(), 'skills': skills, 'project_memory': project_memory(work)}

    def _relative(self, workspace, relative):
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            raise ControlError('invalid_path', 'Artifact paths must be workspace-relative')
        path = (workspace / relative).resolve()
        if not contained(workspace, path):
            raise ControlError('invalid_path', 'Path escapes workspace')
        return path

    def _validate(self, value):
        if not isinstance(value, dict):
            raise ControlError('invalid_contract', 'Contract must be an object')
        contract = json.loads(encoded(value))
        work = workspace_path(contract.get('workspace'))
        contract['workspace'] = str(work)
        if not isinstance(contract.get('objective'), str) or not contract['objective'].strip():
            raise ControlError('invalid_contract', 'Objective is required')
        if not isinstance(contract.get('acceptance'), list) or not contract['acceptance'] or any(not isinstance(v, str) or not v.strip() for v in contract['acceptance']):
            raise ControlError('invalid_contract', 'Observable acceptance criteria are required')
        if not isinstance(contract.get('strategy'), list) or any(not isinstance(v, str) or not v.strip() for v in contract['strategy']):
            raise ControlError('invalid_contract', 'Strategy must be a list of nonempty strings')
        contract['coordinator'] = declared_actor(contract.get('coordinator'))
        contract.setdefault('allow_writes', False)
        if type(contract['allow_writes']) is not bool:
            raise ControlError('invalid_contract', 'allow_writes must be boolean')
        contract.setdefault('trust_workspace', False)
        if type(contract['trust_workspace']) is not bool:
            raise ControlError('invalid_contract', 'trust_workspace must be boolean')
        contract.setdefault('mode', 'agent' if contract['allow_writes'] else 'ask')
        if contract['mode'] not in ('ask', 'plan', 'agent') or (not contract['allow_writes'] and contract['mode'] != 'ask'):
            raise ControlError('invalid_contract', 'Read-only contracts require mode=ask; valid modes are ask/plan/agent')
        for key, default in (('timeout_seconds', 3600), ('verification_timeout_seconds', 300)):
            contract.setdefault(key, default)
            number = contract[key]
            if isinstance(number, bool) or not isinstance(number, (int, float)) or not math.isfinite(number) or not 0 < number <= 86400:
                raise ControlError('invalid_contract', key + ' must be finite and within (0,86400]')
        for key in ('verification_commands', 'evidence_paths', 'skill_bindings'):
            contract.setdefault(key, [])
            if not isinstance(contract[key], list):
                raise ControlError('invalid_contract', key + ' must be a list')
        for command in contract['verification_commands']:
            if not isinstance(command, list) or not command or any(not isinstance(v, str) or not v or '\x00' in v for v in command):
                raise ControlError('invalid_contract', 'Verification commands are nonempty argv arrays')
        for relative in contract['evidence_paths']:
            self._relative(work, relative)
        for binding in contract['skill_bindings']:
            if not isinstance(binding, dict) or any(not isinstance(binding.get(k), str) or not binding[k].strip() for k in ('name', 'host', 'requirement')):
                raise ControlError('invalid_contract', 'Skill binding requires name, host, requirement')
            if binding.get('path'):
                path = Path(binding['path']).expanduser().resolve()
                if not path.is_file():
                    raise ControlError('skill_missing', 'Selected skill path is not readable', {'path': str(path)})
                binding['path'] = str(path)
            elif binding['requirement'] == 'required':
                raise ControlError('skill_missing', 'Required skill binding needs an explicit readable path')
        contract.setdefault('write_ownership', {})
        if not isinstance(contract['write_ownership'], dict):
            raise ControlError('invalid_contract', 'write_ownership must map host to workspace-relative paths')
        owners = []
        for host, paths in contract['write_ownership'].items():
            if not isinstance(host, str) or not isinstance(paths, list):
                raise ControlError('invalid_contract', 'Invalid write_ownership')
            for relative in paths:
                path = workspace_key(self._relative(work, relative))
                for other_host, other in owners:
                    if host != other_host and overlaps(path, other):
                        raise ControlError('ownership_conflict', 'Multiple hosts own overlapping paths')
                owners.append((host, path))
        for key in ('memory', 'aoci'):
            contract.setdefault(key, {'required': False})
            if not isinstance(contract[key], dict) or type(contract[key].get('required', False)) is not bool:
                raise ControlError('invalid_contract', key + ' must have boolean required')
        for relative in contract['memory'].get('pending_paths', []):
            path = self._relative(work, relative)
            if contract['memory'].get('required') and not path.is_file():
                raise ControlError('memory_missing', 'Required memory paths must already exist', {'path': str(path)})
            if relative not in contract['evidence_paths']:
                contract['evidence_paths'].append(relative)
        if 'model' in contract and (not isinstance(contract['model'], str) or not contract['model'].strip()):
            raise ControlError('invalid_contract', 'model must be a nonempty string')
        if contract.get('report_path'):
            self._report_path(work, contract['report_path'])
        return contract

    def _report_path(self, work, value):
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = work / path
        path = path.resolve()
        if not contained(work, path) and not contained(self.data_dir, path):
            raise ControlError('invalid_report_path', 'Report must be under workspace or managed data directory')
        return path

    def submit(self, contract):
        contract = self._validate(contract)
        doctor = self.doctor()
        required = ['--workspace', '--print', '--output-format', '--mode'] + (['--force'] if contract['allow_writes'] else [])
        if contract['trust_workspace']:
            required.append('--trust')
        if not doctor.get('available') or any(not doctor['supported_flags'].get(flag) for flag in required):
            raise ControlError('capability_missing', 'Installed CLI lacks required capabilities', {'doctor': doctor, 'required': required})
        if doctor['authentication'] == 'unauthenticated':
            raise ControlError('authentication_required', 'Cursor Agent CLI is not authenticated')
        task_id, run_id = identifier(), identifier()
        directory = self._run_dir(task_id, run_id)
        directory.mkdir(parents=True)
        contract.update({'task_id': task_id, 'run_id': run_id, 'contract_revision': 1, 'role': 'executor'})
        (directory / 'contract.json').write_text(encoded(contract), encoding='utf-8')
        with self._db(write=True) as db:
            self._lease(db, task_id, run_id, contract['workspace'], run_id, 'execution')
            db.execute('INSERT INTO tasks VALUES (?,?,?,?)', (task_id, workspace_key(contract['workspace']), run_id, 1))
            db.execute('INSERT INTO runs(run_id,task_id,revision,contract,state) VALUES (?,?,?,?,?)', (run_id, task_id, 1, encoded(contract), 'starting'))
            self._append(db, task_id, run_id, 'submit', contract['coordinator'], {'contract_revision': 1, 'contract_path': str(directory / 'contract.json')},
                         [{'path': str(directory / 'contract.json'), 'sha256': digest_file(directory / 'contract.json')}])
        self._launch(task_id, run_id)
        return {'task_id': task_id, 'run_id': run_id, 'contract_revision': 1, 'state': 'starting'}

    def _launch(self, task_id, run_id):
        command = [console_python(sys.executable), str(SCRIPTS / 'cursor_control.py'), '--data-dir', str(self.data_dir)]
        if self.agent_path:
            command += ['--agent-path', self.agent_path]
        command += ['worker', '--task-id', task_id, '--run-id', run_id]
        worker = None
        try:
            with open(self._run_dir(task_id, run_id) / 'worker.log', 'ab', buffering=0) as log:
                worker = spawn_detached(command, log)
            with self._db(write=True) as db:
                # Python's Windows venv launcher can have a different PID. The worker
                # alone claims worker_pid; the parent records only launch evidence.
                self._append(db, task_id, run_id, 'worker_launch', data=worker.launch_info)
        except Exception as error:
            if worker is not None or isinstance(error, LaunchUncertain):
                # Creation succeeded or a broker may have accepted it. Only the worker
                # can acknowledge executor-tree quiescence; bookkeeping is not proof.
                diagnostic = {'error': str(error), 'ownership': 'retained', 'task_id': task_id, 'run_id': run_id}
                with open(self._run_dir(task_id, run_id) / 'launch-diagnostic.json', 'w', encoding='utf-8') as stream:
                    stream.write(encoded(diagnostic))
                try:
                    with self._db(write=True) as db:
                        self._append(db, task_id, run_id, 'launch_uncertain', data=diagnostic)
                except sqlite3.Error:
                    pass  # The existing starting row/lease remains durable even if recording fails again.
                raise ControlError('launch_uncertain', 'Worker launch ownership retained; inspect task status', diagnostic) from error
            with self._db(write=True) as db:
                db.execute('UPDATE runs SET state=?,tree_quiescent=1,ended_at=? WHERE run_id=?', ('failed', now(), run_id))
                db.execute('DELETE FROM leases WHERE token=?', (run_id,))
                self._append(db, task_id, run_id, 'launch_failed', data={'error': str(error)})
            raise ControlError('launch_failed', 'Detached worker failed to launch', {'task_id': task_id, 'run_id': run_id})

    def _audit_record(self, row):
        value = dict(row)
        for key in ('actor', 'data', 'evidence_digests'):
            value[key] = json.loads(value[key])
        return value

    def status(self, task_id, after_event_id=0):
        if type(after_event_id) is not int or after_event_id < 0:
            raise ControlError('invalid_cursor', 'after_event_id must be a nonnegative integer')
        with self._db() as db:
            row = self._current(db, task_id)
            records = db.execute('SELECT * FROM audit WHERE task_id=? AND id>? ORDER BY id LIMIT 100', (task_id, after_event_id)).fetchall()
            total_cursor = db.execute('SELECT COALESCE(MAX(id),0) AS cursor FROM audit WHERE task_id=?', (task_id,)).fetchone()['cursor']
            state = {key: row[key] for key in ('task_id', 'run_id', 'state', 'session_id', 'pid', 'worker_pid', 'started_at', 'ended_at',
                                               'last_event_at', 'recent_tool', 'exit_code', 'acceptance')}
            state.update({'contract_revision': row['revision'], 'tree_quiescent': bool(row['tree_quiescent']),
                          'stop_requested': bool(row['stop_requested']), 'events': [self._bounded(self._audit_record(v)) for v in records],
                          'event_cursor': records[-1]['id'] if records else after_event_id,
                          'has_more_events': bool(records and records[-1]['id'] < total_cursor)})
            state['elapsed_seconds'] = max(0, (datetime.fromisoformat(row['ended_at'] or now()) - datetime.fromisoformat(row['started_at'])).total_seconds()) if row['started_at'] else 0
            return state

    def _bounded(self, record):
        if len(encoded(record['data'])) > 4096:
            record['data'] = {'preview': encoded(record['data'])[:4096], 'truncated': True}
        return record

    def watch(self, task_id, after_event_id=0, wait_seconds=10):
        if isinstance(wait_seconds, bool) or not isinstance(wait_seconds, (int, float)) or not math.isfinite(wait_seconds) or not 0 <= wait_seconds <= 30:
            raise ControlError('invalid_wait', 'wait_seconds must be finite within [0,30]')
        deadline = time.monotonic() + wait_seconds
        while True:
            response = self.status(task_id, after_event_id)
            if response['events'] or response['state'] not in ACTIVE or time.monotonic() >= deadline:
                return response
            time.sleep(min(0.1, max(0, deadline - time.monotonic())))

    def stop(self, task_id):
        with self._db(write=True) as db:
            row = self._current(db, task_id)
            if row['state'] not in ACTIVE:
                raise ControlError('invalid_transition', 'Only an active task can be stopped', {'state': row['state']})
            if not row['stop_requested']:
                db.execute('UPDATE runs SET stop_requested=1 WHERE run_id=?', (row['run_id'],))
                self._append(db, task_id, row['run_id'], 'stop_requested', data={'durable': True})
            return {'task_id': task_id, 'run_id': row['run_id'], 'state': row['state'], 'stop_requested': True, 'tree_quiescent': False}

    def resume(self, task_id, instruction):
        if not isinstance(instruction, str) or not instruction.strip():
            raise ControlError('invalid_instruction', 'Resume instruction must be nonempty')
        doctor = self.doctor()
        if not doctor.get('supported_flags', {}).get('--resume'):
            raise ControlError('capability_missing', 'Installed CLI does not support exact session resume')
        with self._db(write=True) as db:
            old = self._current(db, task_id)
            if old['state'] in ACTIVE or not old['tree_quiescent']:
                raise ControlError('invalid_transition', 'Resume requires terminal, quiescent previous execution')
            if not old['session_id']:
                raise ControlError('session_missing', 'No observed session ID is available')
            run_id, revision = identifier(), old['revision'] + 1
            contract = json.loads(old['contract'])
            contract.update({'run_id': run_id, 'contract_revision': revision, 'resume_instruction': instruction,
                             'resume_session_id': old['session_id']})
            self._lease(db, task_id, run_id, contract['workspace'], run_id, 'execution')
            directory = self._run_dir(task_id, run_id)
            directory.mkdir(parents=True)
            (directory / 'contract.json').write_text(encoded(contract), encoding='utf-8')
            db.execute('INSERT INTO runs(run_id,task_id,revision,contract,state) VALUES (?,?,?,?,?)', (run_id, task_id, revision, encoded(contract), 'starting'))
            db.execute('UPDATE tasks SET current_run=?,revision=? WHERE task_id=?', (run_id, revision, task_id))
            self._append(db, task_id, run_id, 'resume', contract['coordinator'], {'previous_run_id': old['run_id'], 'session_id': old['session_id'], 'contract_revision': revision})
        self._launch(task_id, run_id)
        return {'task_id': task_id, 'run_id': run_id, 'contract_revision': revision, 'state': 'starting'}

    def _executed_by(self, row):
        if not row['session_id'] and row['pid'] is None:
            return {'id': 'unknown', 'kind': 'agent', 'host': 'cursor-cli', 'role': 'executor', 'source': 'unknown'}
        return {'id': row['session_id'] or ('process:' + str(row['pid'])), 'kind': 'agent', 'host': 'cursor-cli', 'role': 'executor', 'source': 'observed'}

    def result(self, task_id):
        with self._db() as db:
            row = self._current(db, task_id)
            contract = json.loads(row['contract'])
            directory = self._run_dir(task_id, row['run_id'])
            return {'task_id': task_id, 'run_id': row['run_id'], 'contract_revision': row['revision'], 'state': row['state'],
                    'result': row['result'], 'session_id': row['session_id'], 'exit_code': row['exit_code'],
                    'tree_quiescent': bool(row['tree_quiescent']), 'executed_by': self._executed_by(row),
                    'acceptance': row['acceptance'], 'decision_id': row['decision_id'], 'verification_id': row['verification_id'],
                    'memory_receipt': json.loads(row['memory_receipt']) if row['memory_receipt'] else None,
                    'aoci_receipt': json.loads(row['aoci_receipt']) if row['aoci_receipt'] else None,
                    'contract_path': str(directory / 'contract.json'), 'stdout_path': str(directory / 'stdout.ndjson'),
                    'stderr_path': str(directory / 'stderr.log'), 'evidence_paths': contract['evidence_paths'],
                    'memory_delta': {'source': 'executor_output', 'status': 'inspect_result_and_artifacts'}}

    def verify(self, task_id, run_id):
        token = identifier()
        with self._db(write=True) as db:
            row = self._current(db, task_id, run_id)
            if row['state'] in ACTIVE or not row['tree_quiescent']:
                raise ControlError('invalid_transition', 'Verification requires a terminal quiescent execution')
            if row['decision_id'] is not None or row['acceptance'] != 'pending':
                raise ControlError('invalid_transition', 'This run already has a decision; resume before new verification')
            contract = json.loads(row['contract'])
            self._lease(db, task_id, run_id, contract['workspace'], token, 'verification')
            self._append(db, task_id, run_id, 'verification_started', data={'token': token})
        directory = self._run_dir(task_id, run_id) / ('verify-' + token)
        directory.mkdir()
        evidence, passed, safe_release = [], True, True
        try:
            contract_path = self._run_dir(task_id, run_id) / 'contract.json'
            contract_sha = hashlib.sha256(row['contract'].encode('utf-8')).hexdigest()
            with self._db() as db:
                registered = db.execute('SELECT id FROM audit WHERE task_id=? AND run_id=? AND action IN (?,?) ORDER BY id LIMIT 1',
                                        (task_id, run_id, 'submit', 'resume')).fetchone()
            if registered:
                evidence.append({'kind': 'contract', 'id': registered['id'], 'task_id': task_id, 'run_id': run_id,
                                 'path': str(contract_path), 'sha256': contract_sha})
            if not registered or not contract_path.is_file() or digest_file(contract_path) != contract_sha:
                passed = False
            # Every verification includes the observed execution record, including read-only tasks.
            with self._db() as db:
                execution = db.execute('SELECT * FROM audit WHERE task_id=? AND run_id=? AND action=? ORDER BY id DESC LIMIT 1',
                                       (task_id, run_id, 'execution')).fetchone()
            if execution:
                logs = {Path(e['path']).name: e for e in json.loads(execution['evidence_digests'])}
                if 'stdout.ndjson' in logs and 'stderr.log' in logs:
                    out, err = logs['stdout.ndjson'], logs['stderr.log']
                    execution_evidence = {'kind': 'execution', 'id': execution['id'], 'task_id': task_id, 'run_id': run_id,
                                          'path': out['path'], 'sha256': out['sha256'], 'stderr_path': err['path'], 'stderr_sha256': err['sha256']}
                    evidence.append(execution_evidence)
                    for item in (out, err):
                        if not Path(item['path']).is_file() or digest_file(item['path']) != item['sha256']:
                            passed = False
                else:
                    passed = False
            else:
                passed = False
            for index, command in enumerate(contract['verification_commands']):
                stdout, stderr = directory / (str(index) + '.stdout'), directory / (str(index) + '.stderr')
                started = now()
                proc = None
                timed_out, quiescent = False, True
                try:
                    with stdout.open('wb', buffering=0) as out, stderr.open('wb', buffering=0) as err:
                        proc = ManagedProcess(command, contract['workspace'], out, err)
                        deadline = time.monotonic() + contract['verification_timeout_seconds']
                        while proc.poll() is None and time.monotonic() < deadline:
                            time.sleep(0.05)
                        timed_out = proc.poll() is None
                        quiescent = proc.finish_tree()
                        exit_code = proc.poll()
                except Exception as error:
                    exit_code = None
                    stderr.write_text(str(error), encoding='utf-8')
                    if proc:
                        quiescent = proc.finish_tree()
                finally:
                    if proc:
                        proc.close()
                safe_release = safe_release and quiescent
                passed = passed and exit_code == 0 and not timed_out and quiescent
                data = {'argv': command, 'exit_code': exit_code, 'timed_out': timed_out, 'tree_quiescent': quiescent,
                        'stdout_path': str(stdout), 'stderr_path': str(stderr), 'stdout_sha256': digest_file(stdout),
                        'stderr_sha256': digest_file(stderr), 'started_at': started, 'ended_at': now()}
                with self._db(write=True) as db:
                    record_id = self._append(db, task_id, run_id, 'verification_command', data=data,
                                             evidence=[{'path': str(stdout), 'sha256': data['stdout_sha256']}, {'path': str(stderr), 'sha256': data['stderr_sha256']}])
                evidence.append({'kind': 'command', 'id': record_id, 'task_id': task_id, 'run_id': run_id, 'path': str(stdout),
                                 'sha256': data['stdout_sha256'], 'stderr_path': str(stderr), 'stderr_sha256': data['stderr_sha256'],
                                 'exit_code': exit_code, 'timed_out': timed_out, 'tree_quiescent': quiescent})
            for relative in contract['evidence_paths']:
                path = self._relative(Path(contract['workspace']), relative)
                if not path.is_file():
                    passed = False
                    continue
                sha = digest_file(path)
                with self._db(write=True) as db:
                    record_id = self._append(db, task_id, run_id, 'verification_artifact', data={'path': str(path), 'relative_path': relative},
                                             evidence=[{'path': str(path), 'sha256': sha}])
                evidence.append({'kind': 'artifact', 'id': record_id, 'task_id': task_id, 'run_id': run_id,
                                 'path': str(path), 'relative_path': relative, 'sha256': sha})
            with self._db(write=True) as db:
                self._current(db, task_id, run_id)
                verification_id = self._append(db, task_id, run_id, 'verification', data={'passed': bool(passed), 'evidence': evidence, 'tree_quiescent': safe_release})
                db.execute('UPDATE runs SET verification_id=? WHERE run_id=?', (verification_id, run_id))
                if not safe_release:
                    db.execute('UPDATE runs SET tree_quiescent=0,state=? WHERE run_id=?', ('stopped_unconfirmed', run_id))
            return {'task_id': task_id, 'run_id': run_id, 'verification_id': verification_id, 'passed': bool(passed), 'evidence': evidence}
        finally:
            if safe_release:
                with self._db(write=True) as db:
                    db.execute('DELETE FROM leases WHERE token=?', (token,))

    def _check_evidence(self, db, row, evidence, require_full=False):
        if not isinstance(evidence, list):
            raise ControlError('invalid_evidence', 'Evidence must be a list')
        verified = db.execute('SELECT * FROM audit WHERE id=? AND task_id=? AND run_id=? AND action=?',
                              (row['verification_id'], row['task_id'], row['run_id'], 'verification')).fetchone()
        valid = json.loads(verified['data']) if verified else {'passed': False, 'evidence': []}
        if require_full and not valid['passed']:
            raise ControlError('verification_failed', 'A successful current machine verification is required')
        expected = {v['id']: v for v in valid['evidence']}
        seen = set()
        for entry in evidence:
            if not isinstance(entry, dict) or entry.get('id') not in expected or entry != expected[entry['id']]:
                raise ControlError('stale_evidence', 'Evidence does not match the current verification receipt')
            if entry['id'] in seen:
                raise ControlError('invalid_evidence', 'Duplicate evidence receipt')
            seen.add(entry['id'])
            for path_key, digest_key in (('path', 'sha256'), ('stderr_path', 'stderr_sha256')):
                if path_key in entry:
                    path = Path(entry[path_key])
                    if not path.is_file() or digest_file(path) != entry[digest_key]:
                        raise ControlError('version_conflict', 'Evidence file changed after verification', {'path': str(path)})
        if require_full and seen != set(expected):
            raise ControlError('missing_evidence', 'All current verification evidence is required')
        return valid

    def _receipt(self, db, row, receipt, kind, contract):
        if receipt is None:
            if contract[kind].get('required'):
                raise ControlError(kind + '_pending', 'Required ' + kind + ' receipt is missing')
            return None
        state = 'completed' if kind == 'memory' else 'checked'
        if not isinstance(receipt, dict) or receipt.get('task_id') != row['task_id'] or receipt.get('run_id') != row['run_id'] or receipt.get('state') != state:
            raise ControlError('invalid_receipt', 'Receipt must match task, current run and completion state')
        if 'actions' in receipt:
            if kind != 'memory' or 'performed_by' in receipt or 'evidence' in receipt or not isinstance(receipt['actions'], list) or not receipt['actions']:
                raise ControlError('invalid_receipt', 'Grouped memory receipt requires nonempty actions and no aggregate performer or evidence')
            actions, claimed, covered = [], set(), set()
            for action in receipt['actions']:
                if not isinstance(action, dict) or not isinstance(action.get('performed_by'), dict) or not isinstance(action.get('evidence'), list):
                    raise ControlError('invalid_receipt', 'Memory action requires performer and artifact evidence')
                performer = declared_actor(action['performed_by'])
                self._check_evidence(db, row, action['evidence'])
                if not action['evidence'] or any(e['kind'] != 'artifact' or not contained(Path(contract['workspace']), Path(e['path'])) for e in action['evidence']):
                    raise ControlError('invalid_receipt', 'Memory actions require current project artifact evidence only')
                for artifact in action['evidence']:
                    path_key = workspace_key(artifact['path'])
                    if path_key in claimed:
                        raise ControlError('invalid_receipt', 'Duplicate memory path claim')
                    claimed.add(path_key)
                    covered.add(artifact['relative_path'])
                    self._memory_owner(contract, performer, artifact)
                actions.append({'performed_by': performer, 'evidence': action['evidence']})
            if not set(contract['memory'].get('pending_paths', [])).issubset(covered):
                raise ControlError('memory_pending', 'Memory receipt must include each pending project path')
            return {k: receipt[k] for k in ('task_id', 'run_id', 'state')} | {'actions': actions}
        performer = declared_actor(receipt.get('performed_by'))
        self._check_evidence(db, row, receipt.get('evidence'))
        artifacts = [e for e in receipt['evidence'] if e['kind'] == 'artifact' and contained(Path(contract['workspace']), Path(e['path']))]
        if not artifacts:
            raise ControlError('invalid_receipt', 'Receipt requires current existing project artifact evidence')
        if kind == 'memory':
            required = set(contract['memory'].get('pending_paths', []))
            if not required.issubset(e['relative_path'] for e in artifacts):
                raise ControlError('memory_pending', 'Memory receipt must include each pending project path')
            for artifact in artifacts:
                self._memory_owner(contract, performer, artifact)
        if kind == 'aoci':
            if receipt.get('host') != performer['host'] or (contract['aoci'].get('host') and performer['host'] != contract['aoci']['host']):
                raise ControlError('invalid_receipt', 'AOCI performer and receipt host must match the registered host')
        return receipt | {'performed_by': performer}

    def _memory_owner(self, contract, performer, artifact):
        # Explicit memory.host remains a single-host restriction. Path owners override
        # the mode default, so the documented project/module split can be truthful.
        explicit_host = contract['memory'].get('host')
        if explicit_host and performer['host'] != explicit_host:
            raise ControlError('invalid_receipt', 'Memory performer must match the registered maintenance host')
        owners = {host for host, paths in contract['write_ownership'].items()
                  if any(overlaps(workspace_key(artifact['path']), workspace_key(Path(contract['workspace']) / path)) for path in paths)}
        if owners and owners != {performer['host']}:
            raise ControlError('invalid_receipt', 'Memory performer conflicts with registered path ownership')
        mode_host = {'executor': 'cursor-cli', 'coordinator': contract['coordinator']['host']}.get(contract['memory'].get('mode'))
        if not owners and mode_host and performer['host'] != (explicit_host or mode_host):
            raise ControlError('invalid_receipt', 'Memory performer must match the registered maintenance host')

    def record_acceptance(self, task_id, run_id, decision, attribution, evidence, memory_receipt=None, aoci_receipt=None, report_path=None):
        if decision not in ('accepted', 'rejected'):
            raise ControlError('invalid_decision', 'decision must be accepted or rejected')
        with self._db(write=True) as db:
            row = self._current(db, task_id, run_id)
            if row['state'] in ACTIVE or not row['tree_quiescent']:
                raise ControlError('invalid_transition', 'Decision requires terminal, quiescent execution')
            if row['acceptance'] != 'pending':
                raise ControlError('invalid_transition', 'This run already has a decision; resume before a new decision')
            contract = json.loads(row['contract'])
            for lease in db.execute('SELECT * FROM leases'):
                if overlaps(workspace_key(contract['workspace']), lease['workspace']):
                    raise ControlError('workspace_busy', 'Decision conflicts with an active workspace lease')
            if not isinstance(attribution, dict):
                raise ControlError('invalid_attribution', 'Explicit responsibility attribution is required')
            normalized = {}
            actual = self._executed_by(row)
            if attribution.get('executed_by') != actual:
                raise ControlError('invalid_attribution', 'executed_by must match the observed execution actor', {'executed_by': actual})
            normalized['executed_by'] = actual
            for key in ('authored_by', 'reviewed_by', 'decided_by'):
                normalized[key] = declared_actor(attribution.get(key))
            for key in ('reviewed_by', 'decided_by'):
                if normalized[key]['kind'] != 'agent':
                    raise ControlError('invalid_attribution', 'Technical reviewer and decider must explicitly be agents')
            for key in ('decision_basis', 'authorization_basis'):
                if not isinstance(attribution.get(key), str) or not attribution[key].strip():
                    raise ControlError('invalid_attribution', key + ' must be explicit')
                normalized[key] = attribution[key]
            self._check_evidence(db, row, evidence, require_full=decision == 'accepted')
            if decision == 'accepted' and row['state'] != 'succeeded':
                raise ControlError('execution_not_successful', 'Acceptance requires successful execution')
            memory = self._receipt(db, row, memory_receipt, 'memory', contract) if decision == 'accepted' or memory_receipt is not None else None
            aoci = self._receipt(db, row, aoci_receipt, 'aoci', contract) if decision == 'accepted' or aoci_receipt is not None else None
            if memory:
                memory['recorded_by'] = normalized['authored_by']
                if 'actions' in memory:
                    for action in memory['actions']:
                        action['recorded_by'] = normalized['authored_by']
                        action_data = {k: memory[k] for k in ('task_id', 'run_id', 'state')} | action
                        action['receipt_id'] = self._append(db, task_id, run_id, 'memory_action', action['performed_by'], action_data,
                                                            evidence=action['evidence'])
            if aoci:
                aoci['recorded_by'] = normalized['authored_by']
            memory_id = self._append(db, task_id, run_id, 'memory', memory.get('performed_by', SERVICE), memory) if memory else None
            aoci_id = self._append(db, task_id, run_id, 'aoci', aoci['performed_by'], aoci) if aoci else None
            decision_data = {'decision': decision, 'attribution': normalized, 'verification_id': row['verification_id'],
                             'memory_receipt_id': memory_id, 'aoci_receipt_id': aoci_id, 'memory_receipt': memory,
                             'aoci_receipt': aoci, 'contract_revision': row['revision'], 'evidence': evidence}
            decision_id = self._append(db, task_id, run_id, 'decision', normalized['decided_by'], decision_data, evidence=evidence)
            db.execute('UPDATE runs SET acceptance=?,decision_id=?,memory_receipt=?,aoci_receipt=? WHERE run_id=?',
                       (decision, decision_id, encoded(memory) if memory else None, encoded(aoci) if aoci else None, run_id))
            desired = report_path or contract.get('report_path')
            path = self._report_path(Path(contract['workspace']), desired) if desired else self._run_dir(task_id, run_id) / ('report-' + str(decision_id) + '.md')
            # Never bulk-overwrite a report owned by the user or a preceding run.
            if path.exists():
                raise ControlError('report_exists', 'Report path already exists; choose a new path', {'path': str(path)})
            path.parent.mkdir(parents=True, exist_ok=True)
            content = '# Cursor task report\n\n' + '\n'.join([
                f'Task: {task_id}', f'Run: {run_id}', f'Contract revision: {row["revision"]}', f'Decision: {decision}',
                f'Execution started: {row["started_at"]}', f'Execution ended: {row["ended_at"]}', f'Decision recorded: {now()}',
                f'Decision receipt: {decision_id}', f'Verification receipt: {row["verification_id"]}',
                f'Memory receipt: {memory_id or "not supplied"}', f'AOCI receipt: {aoci_id or "not supplied"}',
                '\nAttribution and evidence (declared identities are responsibility claims):\n',
                '```json\n' + json.dumps(decision_data, ensure_ascii=False, indent=2) + '\n```\n'])
            with path.open('x', encoding='utf-8') as stream:
                stream.write(content)
            report_id = self._append(db, task_id, run_id, 'report_rendered', normalized['authored_by'], {'path': str(path), 'decision_id': decision_id},
                                     evidence=[{'path': str(path), 'sha256': digest_file(path)}])
            return {'task_id': task_id, 'run_id': run_id, 'decision': decision, 'decision_id': decision_id,
                    'memory_receipt_id': memory_id, 'aoci_receipt_id': aoci_id, 'report_receipt_id': report_id, 'report_path': str(path)}

    def audit(self, task_id, after_event_id=0):
        if type(after_event_id) is not int or after_event_id < 0:
            raise ControlError('invalid_cursor', 'after_event_id must be nonnegative integer')
        with self._db() as db:
            self._current(db, task_id)
            all_rows = db.execute('SELECT * FROM audit WHERE task_id=? ORDER BY id', (task_id,)).fetchall()
            previous, valid = '', True
            for row in all_rows:
                record = self._audit_record(row)
                record.pop('id')
                sha = record.pop('hash')
                if record['prev_hash'] != previous or hashlib.sha256(encoded(record).encode('utf-8')).hexdigest() != sha:
                    valid = False
                previous = sha
            rows = [r for r in all_rows if r['id'] > after_event_id][:100]
            return {'task_id': task_id, 'records': [self._bounded(self._audit_record(r)) for r in rows],
                    'event_cursor': rows[-1]['id'] if rows else after_event_id,
                    'has_more_events': bool(rows and rows[-1]['id'] < all_rows[-1]['id']), 'integrity_valid': valid,
                    'integrity_scope': 'hash-linked database records, not tamper-proof'}

    def list_tasks(self):
        with self._db() as db:
            rows = db.execute('SELECT t.task_id,t.workspace,t.current_run AS run_id,t.revision AS contract_revision,r.state,r.acceptance,r.tree_quiescent FROM tasks t JOIN runs r ON r.run_id=t.current_run ORDER BY t.rowid DESC LIMIT 100').fetchall()
            return {'tasks': [dict(r) | {'tree_quiescent': bool(r['tree_quiescent'])} for r in rows]}
