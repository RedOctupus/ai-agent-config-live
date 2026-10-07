"""JSON CLI sharing exactly the Controller state used by the MCP adapter."""
import argparse
import json
from pathlib import Path
import sys

from cursor_runtime import Controller, ControlError


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({'error': {'code': 'invalid_arguments', 'message': message, 'details': {}}}, ensure_ascii=False))
        raise SystemExit(2)


def main(argv=None):
    parser = JsonArgumentParser(description='Local Cursor task controller (JSON output)')
    parser.add_argument('--data-dir')
    parser.add_argument('--agent-path')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('doctor')
    commands.add_parser('list-tasks')
    cap = commands.add_parser('capabilities')
    cap.add_argument('--workspace', required=True)
    cap.add_argument('--skill', action='append', default=[])
    submit = commands.add_parser('submit')
    submit.add_argument('--contract-file', required=True)
    for name in ('status', 'watch', 'stop', 'resume', 'result', 'verify', 'acceptance', 'audit', 'worker'):
        cmd = commands.add_parser(name)
        cmd.add_argument('--task-id', required=True)
        if name in ('verify', 'worker', 'acceptance'):
            cmd.add_argument('--run-id', required=True)
        if name in ('status', 'watch', 'audit'):
            cmd.add_argument('--after-event-id', type=int, default=0)
        if name == 'watch':
            cmd.add_argument('--wait-seconds', type=float, default=10)
        if name == 'resume':
            cmd.add_argument('--instruction', required=True)
        if name == 'acceptance':
            cmd.add_argument('--receipt-file', required=True)
    args = parser.parse_args(argv)
    try:
        controller = Controller(args.data_dir, args.agent_path)
        if args.command == 'doctor':
            result = controller.doctor()
        elif args.command == 'list-tasks':
            result = controller.list_tasks()
        elif args.command == 'capabilities':
            result = controller.capabilities(args.workspace, args.skill)
        elif args.command == 'submit':
            result = controller.submit(json.loads(Path(args.contract_file).read_text(encoding='utf-8-sig')))
        elif args.command == 'acceptance':
            receipt = json.loads(Path(args.receipt_file).read_text(encoding='utf-8-sig'))
            for key in ('task_id', 'run_id'):
                receipt.pop(key, None)
            result = controller.record_acceptance(args.task_id, args.run_id, **receipt)
        elif args.command == 'worker':
            from cursor_runtime.worker import run_worker
            run_worker(controller, args.task_id, args.run_id)
            return 0
        else:
            keywords = {'task_id': args.task_id}
            for key in ('run_id', 'instruction', 'after_event_id', 'wait_seconds'):
                if hasattr(args, key):
                    keywords[key] = getattr(args, key)
            result = getattr(controller, args.command)(**keywords)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except ControlError as error:
        print(json.dumps(error.as_dict(), ensure_ascii=False))
        return 1
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({'error': {'code': 'invalid_input', 'message': str(error), 'details': {}}}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
