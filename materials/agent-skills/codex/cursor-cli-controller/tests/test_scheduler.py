"""Actual per-user Scheduler action and owned-entry cleanup checks."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from cursor_runtime.processes import scheduler_command


@unittest.skipUnless(os.name == 'nt', 'Per-user Windows Scheduler')
class SchedulerWorkingDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.envelope = self.directory / 'broker-launch.json'
        self.token = uuid.uuid4().hex
        self.task_name = 'CursorController-Worker-' + self.token
        self.output = self.directory / 'cwd.json'
        program = ('import json,os,pathlib; pathlib.Path(' + repr(str(self.output)) +
                   ').write_text(json.dumps({"cwd":os.getcwd(),"pid":os.getpid()}),encoding="utf-8")')
        self.payload = {'task_name': self.task_name, 'token': self.token,
                        'executable': str(Path(sys.executable).with_name('pythonw.exe')),
                        'arguments': subprocess.list2cmdline(['-c', program])}
        self.envelope.write_text(json.dumps(self.payload), encoding='utf-8')
        done = self.helper('launch')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.owned_task_exists = True
        self.addCleanup(self.delete_owned_task)
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline and not self.output.exists():
            time.sleep(.02)
        self.assertTrue(self.output.exists(), 'Scheduled fixture did not produce cwd observation')
        self.observation = json.loads(self.output.read_text(encoding='utf-8'))
        self.wait_worker()

    def helper(self, operation):
        return subprocess.run(scheduler_command(self.envelope, operation), capture_output=True,
                              encoding='utf-8', timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)

    def wait_worker(self):
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x100000, False, self.observation['pid'])
        if handle:
            try:
                self.assertEqual(kernel.WaitForSingleObject(handle, 5000), 0)
            finally:
                kernel.CloseHandle(handle)

    def delete_owned_task(self):
        # Exact created name only; no process-name or Scheduler-wide cleanup.
        if self.owned_task_exists:
            done = self.helper('cleanup')
            self.assertEqual(done.returncode, 0, done.stderr)

    def set_owned_working_directory(self, directory):
        def literal(text):
            return "'" + str(text).replace("'", "''") + "'"
        script = ("$ErrorActionPreference='Stop'; $s=New-Object -ComObject Schedule.Service; $s.Connect(); "
                  "$f=$s.GetFolder('\\'); $t=$f.GetTask(" + literal(self.task_name) + "); $d=$t.Definition; "
                  "$d.Actions.Item(1).WorkingDirectory=" + literal(directory) + "; "
                  "$null=$f.RegisterTaskDefinition(" + literal(self.task_name) + ", $d, 4, $d.Principal.UserId, $null, 3, $null)")
        command = scheduler_command(self.envelope, 'cleanup')[:]
        command = command[:command.index('-File')] + ['-Command', script]
        done = subprocess.run(command, capture_output=True, encoding='utf-8', timeout=20,
                              creationflags=subprocess.CREATE_NO_WINDOW)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_broker_uses_stable_script_directory_instead_of_disposable_run(self):
        self.assertEqual(Path(self.observation['cwd']).resolve(), (ROOT / 'scripts').resolve())

    def test_cleanup_refuses_owned_name_with_modified_working_directory(self):
        self.set_owned_working_directory(self.directory / 'unexpected')
        try:
            done = self.helper('cleanup')
            if done.returncode == 0:
                self.owned_task_exists = False
            self.assertNotEqual(done.returncode, 0, 'Cleanup accepted changed action cwd')
            self.assertIn('Task identity mismatch', done.stderr)
        finally:
            if self.owned_task_exists:
                self.set_owned_working_directory(self.observation['cwd'])
