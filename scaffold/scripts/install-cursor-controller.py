"""Explicit, preview-first installation of this repository's Cursor controller."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / 'materials' / 'agent-skills' / 'codex' / 'cursor-cli-controller'
MANIFEST = REPO / 'materials' / 'tools' / 'cursor-controller' / 'manifest.json'
NAME = 'cursor-controller'


def relative_file(root: Path, name: str) -> Path:
    candidate = Path(name)
    if candidate.is_absolute() or '..' in candidate.parts:
        raise ValueError('Package path must stay inside source: ' + name)
    path = (root / candidate).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Linked package file escapes source: ' + name)
    return path


def verify_source(source: Path, manifest: dict) -> dict:
    files = manifest.get('files')
    if not isinstance(files, dict) or not files:
        raise ValueError('Manifest must contain source file hashes')
    for name, expected in files.items():
        path = relative_file(source, name)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Source integrity mismatch: ' + name)
    version = (source / 'VERSION').read_text(encoding='utf-8').strip()
    if version != manifest.get('version'):
        raise ValueError('Source VERSION and manifest differ')
    if not re.search(r'(?m)^name:\s*cursor-cli-controller\s*$', (source / 'SKILL.md').read_text(encoding='utf-8')):
        raise ValueError('Source skill identity differs')
    return {'version': version, 'verified_files': len(files), 'source': str(source.resolve())}


def copy_source(source: Path, target: Path, files: dict, apply: bool = False) -> dict:
    target = target.expanduser().resolve()
    if target.name != 'cursor-cli-controller' or target == target.parent:
        raise ValueError('Target must be a dedicated cursor-cli-controller folder')
    planned = []
    for name in files:
        original = relative_file(source, name)
        destination = relative_file(target, name)
        if destination.exists():
            if not destination.is_file() or destination.read_bytes() != original.read_bytes():
                raise ValueError('Existing installed asset differs; stop/review/backup explicitly before updating: ' + str(destination))
        else:
            planned.append(name)
    if target.exists() and not (target / 'SKILL.md').exists() and any(target.iterdir()):
        raise ValueError('Refusing to adopt a nonempty unrelated target directory')
    if apply:
        for name in planned:
            destination = relative_file(target, name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(relative_file(source, name), destination)
    return {'target': str(target), 'new_files': planned, 'applied': apply}


def configure_mcp(config: Path, python: Path, server: Path, audit: Path, apply: bool = False) -> dict:
    config = config.expanduser().resolve()
    command = str(python.expanduser().resolve())
    arguments = [str(server.expanduser().resolve()), '--data-dir', str(audit.expanduser().resolve())]
    original = config.read_text(encoding='utf-8') if config.exists() else ''
    parsed = tomllib.loads(original)
    current = parsed.get('mcp_servers', {}).get(NAME)
    if current is not None:
        if current.get('command') != command or current.get('args') != arguments:
            raise ValueError('Named MCP configuration differs; preserve it and resolve explicitly, do not overwrite')
        return {'configured': True, 'changed': False, 'config': str(config), 'applied': apply}
    table = ('\n[mcp_servers.cursor-controller]\ncommand = ' + json.dumps(command) +
             '\nargs = ' + json.dumps(arguments) + '\n')
    merged = original + ('\n' if original and not original.endswith('\n') else '') + table
    after = tomllib.loads(merged)
    for key, value in parsed.items():
        if key == 'mcp_servers':
            if any(after[key].get(name) != entry for name, entry in value.items()):
                raise ValueError('Unrelated MCP configuration would change')
        elif after.get(key) != value:
            raise ValueError('Unrelated configuration would change')
    backup = None
    if apply:
        config.parent.mkdir(parents=True, exist_ok=True)
        if config.exists():
            backup = config.with_name(config.name + '.cursor-controller-' + datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f') + '.bak')
            shutil.copy2(config, backup)
        config.write_text(merged, encoding='utf-8')
    return {'configured': apply, 'changed': True, 'config': str(config), 'backup': str(backup) if backup else None,
            'command': command, 'args': arguments, 'applied': apply}


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify/install/configure Cursor controller; writes require --apply')
    parser.add_argument('action', choices=['verify', 'install', 'configure'])
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--target', type=Path)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--data-dir', type=Path)
    args = parser.parse_args()
    codex_home = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex'))
    target = (args.target or codex_home / 'skills' / 'cursor-cli-controller').expanduser().resolve()
    audit = (args.data_dir or Path.home() / '.local' / 'share' / 'ai-agent-config' / 'cursor-controller' / 'audit').expanduser().resolve()
    try:
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
        output = {'source_verification': verify_source(SOURCE, manifest)}
        if args.action == 'install':
            output['installation'] = copy_source(SOURCE, target, manifest['files'], args.apply)
            python = target / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
            output['dependency'] = {'private_python': str(python), 'mcp_version': '2.3.0', 'network_only_when_missing': True}
            if args.apply:
                if not python.is_file():
                    subprocess.run([sys.executable, '-m', 'venv', str(target / '.venv')], check=True)
                probe = subprocess.run([str(python), '-c', 'import importlib.metadata; print(importlib.metadata.version("mcp"))'],
                                       capture_output=True, text=True)
                if probe.returncode or probe.stdout.strip() != '2.3.0':
                    subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(target / 'requirements.txt')], check=True)
                subprocess.run([str(python), str(target / 'scripts' / 'cursor_control.py'), '--data-dir', str(audit), 'doctor'], check=True)
        elif args.action == 'configure':
            python = target / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
            server = target / 'scripts' / 'mcp_server.py'
            if args.apply and (not python.is_file() or not server.is_file()):
                raise ValueError('Install the dedicated skill/private environment before applying MCP configuration')
            output['mcp'] = configure_mcp(args.config or codex_home / 'config.toml', python, server, audit, args.apply)
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
