"""Real local subprocess fixture; never makes model requests."""
import json
import os
import pathlib
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

if '--help' in sys.argv:
    print('--workspace --print --output-format --mode --force --resume --model --trust')
    sys.exit(0)
if '--version' in sys.argv:
    print('fixture-agent 1')
    sys.exit(0)
if 'status' in sys.argv:
    print('Authenticated')
    sys.exit(0)

prompt = sys.argv[-1]
contract_path = prompt.split('CONTRACT_FILE=', 1)[1].split('\n', 1)[0]
contract = json.loads(pathlib.Path(contract_path).read_text(encoding='utf-8'))
objective = contract['objective']
workspace = pathlib.Path(contract['workspace'])
if objective == 'report-signature':
    fields = ['task_id=' + contract['task_id'], 'run_id=' + contract['run_id'],
              'contract_revision=' + str(contract['contract_revision']), 'executed_by', 'authored_by',
              'reviewed_by=pending coordinator', 'decided_by=pending coordinator', 'decision=pending coordinator acceptance',
              'declared', 'known audit', 'unknown']
    if any(field not in prompt for field in fields):
        print('Executor responsibility block instructions are missing', file=sys.stderr)
        sys.exit(12)
if contract.get('trust_workspace') and '--trust' not in sys.argv:
    print('Missing explicit trust flag', file=sys.stderr)
    sys.exit(8)
if not contract.get('allow_writes') and '--force' in sys.argv:
    sys.exit(9)
print(json.dumps({'type': 'system', 'subtype': 'init', 'session_id': 'fixture-session'}, ensure_ascii=False), flush=True)
if objective.startswith('sleep') or objective.startswith('child'):
    if objective.startswith('child'):
        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(90)'])
        (workspace / 'child.pid').write_text(str(child.pid))
    time.sleep(90)
if objective == 'flood':
    while True:
        print(json.dumps({'type': 'future_event', 'message': 'chatter'}), flush=True)
if objective == 'malformed':
    print('this is not JSON', flush=True)
    print(json.dumps({'type': 'future_event', 'novel': {'a': 1}}), flush=True)
tool_event = {'type': 'tool_call', 'tool_name': 'Read', 'session_id': 'fixture-session'}
if objective == 'typed-tool':
    tool_event = {'type': 'tool_call', 'subtype': 'started', 'tool_call': {'readToolCall': {'args': {'path': str(workspace / 'artifact.txt')}}}, 'session_id': 'fixture-session'}
print(json.dumps(tool_event), flush=True)
if contract.get('allow_writes'):
    (workspace / 'artifact.txt').write_text(objective, encoding='utf-8')
if objective != 'missing':
    terminal = {'type': 'result', 'subtype': 'success', 'is_error': objective == 'terminal-error', 'result': objective, 'session_id': 'fixture-session'}
    if objective == 'invalid-terminal':
        terminal.pop('result')
    print(json.dumps(terminal, ensure_ascii=False), flush=True)
sys.exit(7 if objective == 'nonzero' else 0)
