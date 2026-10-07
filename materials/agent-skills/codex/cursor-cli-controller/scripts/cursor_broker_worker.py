"""Hidden Scheduler entrypoint; only executes the fixed controller worker command."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback

from cursor_runtime.processes import scheduler_command


def main():
    envelope = Path(sys.argv[1]).resolve()
    launch = json.loads(envelope.read_text(encoding='utf-8'))
    token = launch['token']
    if not re.fullmatch('[a-f0-9]{32}', token) or launch['task_name'] != 'CursorController-Worker-' + token:
        raise ValueError('Invalid transient worker identity')
    argv = launch['argv']
    script = Path(__file__).with_name('cursor_control.py').resolve()
    if Path(argv[1]).resolve() != script or 'worker' not in argv or Path(launch['log_path']).resolve() != envelope.with_name('worker.log'):
        raise ValueError('Broker only executes its fixed controller worker and managed log')
    # pythonw intentionally has no console streams. External fixture/executor .py files
    # still use console python.exe via Controller._argv and explicit managed pipes.
    with envelope.with_name('worker.log').open('a', encoding='utf-8', buffering=1) as log:
        sys.stdout = sys.stderr = log
        try:
            # Deleting this uniquely validated task does not stop the already-running
            # process. No recurring trigger or permanent launcher is left behind.
            cleanup = subprocess.run(scheduler_command(envelope, 'cleanup'), stdin=subprocess.DEVNULL,
                                     capture_output=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
            if cleanup.returncode:
                raise RuntimeError('Scheduled task cleanup failed: ' + cleanup.stderr.decode('utf-8', 'replace'))
            envelope.with_name('broker-cleanup.json').write_bytes(cleanup.stdout)
            from cursor_control import main as worker_main
            return worker_main(argv[2:])
        except BaseException:
            traceback.print_exc()
            raise


if __name__ == '__main__':
    main()
