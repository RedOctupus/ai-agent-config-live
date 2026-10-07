"""Task-scoped subprocess containment; no shell or process-name killing."""
import ctypes
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import threading
import time
from types import SimpleNamespace
import uuid


class LaunchUncertain(OSError):
    """A broker may have created a worker: retain its lease until worker acknowledgment."""


if os.name == 'nt':
    from ctypes import wintypes

    class BasicLimit(ctypes.Structure):
        _fields_ = [('PerProcessUserTimeLimit', ctypes.c_int64), ('PerJobUserTimeLimit', ctypes.c_int64),
                    ('LimitFlags', wintypes.DWORD), ('MinimumWorkingSetSize', ctypes.c_size_t),
                    ('MaximumWorkingSetSize', ctypes.c_size_t), ('ActiveProcessLimit', wintypes.DWORD),
                    ('Affinity', ctypes.c_size_t), ('PriorityClass', wintypes.DWORD), ('SchedulingClass', wintypes.DWORD)]

    class IO(ctypes.Structure):
        _fields_ = [(n, ctypes.c_uint64) for n in ('ReadOperationCount', 'WriteOperationCount', 'OtherOperationCount',
                                                 'ReadTransferCount', 'WriteTransferCount', 'OtherTransferCount')]

    class ExtendedLimit(ctypes.Structure):
        _fields_ = [('BasicLimitInformation', BasicLimit), ('IoInfo', IO), ('ProcessMemoryLimit', ctypes.c_size_t),
                    ('JobMemoryLimit', ctypes.c_size_t), ('PeakProcessMemoryUsed', ctypes.c_size_t),
                    ('PeakJobMemoryUsed', ctypes.c_size_t)]

    class Accounting(ctypes.Structure):
        _fields_ = [(n, ctypes.c_int64) for n in ('TotalUserTime', 'TotalKernelTime', 'ThisPeriodTotalUserTime', 'ThisPeriodTotalKernelTime')] + [
            (n, wintypes.DWORD) for n in ('TotalPageFaultCount', 'TotalProcesses', 'ActiveProcesses', 'TotalTerminatedProcesses')]

    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p]
    kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
    ntdll = ctypes.WinDLL('ntdll')
    ntdll.NtResumeProcess.argtypes = [wintypes.HANDLE]
    ntdll.NtResumeProcess.restype = ctypes.c_long


class ManagedProcess:
    """Assign a suspended Windows process before any application thread can run."""
    def __init__(self, argv, cwd, stdout, stderr, env=None):
        self.job = None
        options = {'cwd': str(cwd), 'stdin': subprocess.DEVNULL, 'stdout': stdout, 'stderr': stderr,
                   'env': env, 'shell': False}
        if os.name == 'nt':
            self.job = kernel.CreateJobObjectW(None, None)
            if not self.job:
                raise ctypes.WinError(ctypes.get_last_error())
            limits = ExtendedLimit()
            limits.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            if not kernel.SetInformationJobObject(self.job, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
                self.close()
                raise ctypes.WinError(ctypes.get_last_error())
            options['creationflags'] = subprocess.CREATE_NO_WINDOW | 0x4  # CREATE_SUSPENDED
        else:
            options['start_new_session'] = True
        try:
            self.process = subprocess.Popen(argv, **options)
            if self.job:
                if not kernel.AssignProcessToJobObject(self.job, int(self.process._handle)):
                    raise ctypes.WinError(ctypes.get_last_error())
                if ntdll.NtResumeProcess(int(self.process._handle)) != 0:
                    raise OSError('NtResumeProcess failed')
        except BaseException:
            if hasattr(self, 'process'):
                self.process.kill()
                self.process.wait(timeout=5)
            self.close()
            raise

    @property
    def pid(self):
        return self.process.pid

    def poll(self):
        return self.process.poll()

    def terminate_tree(self):
        if self.job:
            if not kernel.TerminateJobObject(self.job, 1):
                raise ctypes.WinError(ctypes.get_last_error())
        else:
            try:
                os.killpg(self.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

    def quiescent(self):
        self.process.poll()
        if self.job:
            info = Accounting()
            if not kernel.QueryInformationJobObject(self.job, 1, ctypes.byref(info), ctypes.sizeof(info), None):
                return False
            return info.ActiveProcesses == 0
        try:
            os.killpg(self.pid, 0)
            return False
        except ProcessLookupError:
            return True

    def finish_tree(self, timeout=5):
        # Even normal parent completion must quiesce any surviving children.
        if not self.quiescent():
            self.terminate_tree()
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.quiescent():
                try:
                    self.process.wait(timeout=1)
                    return True
                except subprocess.TimeoutExpired:
                    return False
            time.sleep(0.05)
        if not self.quiescent():
            return False
        try:
            self.process.wait(timeout=1)
            return True
        except subprocess.TimeoutExpired:
            return False

    def close(self):
        if self.job:
            kernel.CloseHandle(self.job)
            self.job = None


def in_windows_job():
    if os.name != 'nt':
        return False
    result = wintypes.BOOL()
    if not kernel.IsProcessInJob(kernel.GetCurrentProcess(), None, ctypes.byref(result)):
        raise ctypes.WinError(ctypes.get_last_error())
    return bool(result.value)


def console_python(executable):
    path = Path(executable)
    return str(path.with_name('python.exe')) if os.name == 'nt' and path.name.lower() == 'pythonw.exe' else str(path)


def scheduler_command(envelope, operation):
    powershell = shutil.which('powershell.exe') or shutil.which('pwsh.exe')
    if not powershell:
        raise OSError('Windows Task Scheduler launch requires PowerShell')
    return [powershell, '-NoLogo', '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden',
            '-ExecutionPolicy', 'Bypass', '-File', str(Path(__file__).resolve().parents[1] / 'cursor_scheduler.ps1'),
            '-EnvelopePath', str(envelope), '-Operation', operation]


def spawn_scheduled(argv, log):
    """The per-user Scheduler service creates the worker outside the caller's Job."""
    directory = Path(log.name).resolve().parent
    hidden_python = Path(argv[0]).with_name('pythonw.exe')
    if not hidden_python.is_file():
        raise OSError('Hidden durable worker requires pythonw.exe beside the Python interpreter')
    token = uuid.uuid4().hex
    envelope = directory / 'broker-launch.json'
    action_args = subprocess.list2cmdline([str(Path(__file__).resolve().parents[1] / 'cursor_broker_worker.py'), str(envelope)])
    payload = {'task_name': 'CursorController-Worker-' + token, 'token': token, 'argv': argv,
               'log_path': str(Path(log.name).resolve()), 'executable': str(hidden_python), 'arguments': action_args}
    envelope.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
    command = scheduler_command(envelope, 'launch')
    try:
        result = subprocess.run(command, stdin=subprocess.DEVNULL, capture_output=True, timeout=20,
                                creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired as error:
        raise LaunchUncertain('Scheduler acknowledgment timed out; inspect broker-launch.json') from error
    # Once the helper ran, no later bookkeeping/decoding error proves Run()
    # was not accepted. Preserve uncertainty through the entire return boundary.
    try:
        if result.returncode:
            diagnostic = result.stderr.decode('utf-8', 'replace')[-8000:]
            (directory / 'broker-error.log').write_text(diagnostic, encoding='utf-8')
            raise LaunchUncertain('Scheduler launch failed or was not acknowledged: ' + diagnostic)
        registered = json.loads(result.stdout.decode('utf-8-sig'))
        if registered.get('task_name') != payload['task_name'] or registered.get('scheduled') is not True or not registered.get('sid'):
            raise ValueError('Broker response identity does not match its requested task')
        (directory / 'broker-registered.json').write_text(json.dumps(registered), encoding='utf-8')
        return SimpleNamespace(pid=None, launch_info={'mechanism': 'windows_task_scheduler',
                               'task_name': payload['task_name'], 'envelope_path': str(envelope),
                               'executable': str(hidden_python), 'identity': 'current_user_interactive_token',
                               'sid': registered['sid'], 'instance_id': registered['instance_id'], 'run_level': 'least_privilege'})
    except LaunchUncertain:
        raise
    except Exception as error:
        raise LaunchUncertain('Scheduler acknowledgment could not be recorded: ' + str(error)) from error


def spawn_detached(argv, log):
    if in_windows_job():
        return spawn_scheduled(argv, log)
    options = {'stdin': subprocess.DEVNULL, 'stdout': log, 'stderr': log, 'close_fds': True, 'shell': False}
    if os.name == 'nt':
        options['creationflags'] = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        options['start_new_session'] = True
    process = subprocess.Popen(argv, **options)
    try:
        process.launch_info = {'mechanism': 'detached_process', 'launcher_pid': process.pid}
        # Retain and reap the launcher handle without binding executor lifetime to it.
        threading.Thread(target=process.wait, daemon=True).start()
    except Exception as error:
        raise LaunchUncertain('Worker created but launcher bookkeeping failed: ' + str(error)) from error
    return process
