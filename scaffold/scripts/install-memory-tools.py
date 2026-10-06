"""Offline Kit/AOCI installer. Python 3.11+, standard library only."""
import argparse
import hashlib
import json
import os
import platform
import re
import stat
import subprocess
import sys
import tomllib
import uuid
import zipfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2]
HOSTS = ('codex', 'claude', 'cursor')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, relative):
    root = root.resolve()
    path = root / relative
    if not path.resolve().is_relative_to(root):
        raise ValueError(f'Path escapes its root: {relative}')
    for part in (path, *path.parents):
        if part == root:
            break
        reparse = part.exists() and bool(getattr(part.lstat(), 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0))
        if part.is_symlink() or reparse:
            raise ValueError(f'Linked deployment path: {part}')
    return path


def state_root(home):
    return safe_path(home, '.local/share/ai-agent-config')


def read_state(home):
    p = state_root(home) / 'memory-tools.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def write_file(path, data, home, expected):
    old = path.read_bytes() if path.exists() else None
    if old != expected:
        raise ValueError(f'File changed during deployment: {path}')
    if old == data:
        return
    if old is not None:
        backup = state_root(home) / 'backups' / uuid.uuid4().hex / path.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(old)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp-' + uuid.uuid4().hex)
    tmp.write_bytes(data)
    if (path.read_bytes() if path.exists() else None) != old:
        raise ValueError(f'File changed during deployment: {path}')
    os.replace(tmp, path)


def package(source):
    root = source / 'materials/tools/aoci'
    meta = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    if not re.fullmatch(r'[A-Za-z0-9._-]+', meta['version']):
        raise ValueError('Invalid version path')
    archive = safe_path(root, meta['archive'])
    if sha(archive.read_bytes()) != meta['archive_sha256']:
        raise ValueError('AOCI archive SHA-256 mismatch')
    with zipfile.ZipFile(archive) as z:
        member = meta['binary_member']
        if len(z.infolist()) != len(set(i.filename for i in z.infolist())):
            raise ValueError('Duplicate archive members')
        for i in z.infolist():
            name = i.filename.replace('\\', '/')
            if name.startswith('/') or '..' in name.split('/') or ':' in name:
                raise ValueError('Unsafe archive member')
        data = z.read(member)
    if sha(data) != meta['binary_sha256']:
        raise ValueError('AOCI binary SHA-256 mismatch')
    return meta, data


def skill_files(path, require_entry=True):
    result = {}
    for p in path.rglob('*'):
        rel = p.relative_to(path)
        if any(n in ('_sandbox', '__pycache__') for n in rel.parts) or p.suffix == '.pyc':
            continue
        safe_path(path, rel)
        if p.is_file():
            result[str(rel)] = p.read_bytes()
    if require_entry and 'SKILL.md' not in result:
        raise ValueError('Kit SKILL.md missing')
    return result


def install(source, home, component, hosts, apply, upgrade_aoci=False):
    source, home = source.resolve(), home.resolve()
    state = read_state(home)
    plans = []
    existing_skills = {}
    meta = data = None
    if component in ('all', 'aoci'):
        meta, data = package(source)
        old = state.get('aoci', {})
        if old.get('version') not in (None, meta['version']) and not upgrade_aoci:
            raise ValueError('AOCI version changes require the upgrade checklist and --upgrade-aoci')
        binary = safe_path(home, f'.local/share/ai-agent-config/aoci/{meta["version"]}/aoci.exe')
        if binary.exists() and sha(binary.read_bytes()) != meta['binary_sha256']:
            raise ValueError('Installed version has different bytes; keep it for review')
        plans.append(('aoci', binary))
    if component in ('all', 'kit'):
        claude = skill_files(source / 'materials/agent-skills/claude/project-memory-kit')
        cursor = skill_files(source / 'materials/agent-skills/cursor/project-memory-kit')
        if claude != cursor:
            raise ValueError('Authoritative Kit mirrors differ')
        for host in hosts:
            base = '.agents' if host == 'codex' else '.' + host
            path = safe_path(home, base + '/skills/project-memory-kit')
            if path.exists() and not path.is_dir():
                raise ValueError(f'Skill target is not a directory: {path}')
            existing_skills[host] = skill_files(path, require_entry=False) if path.exists() else None
            plans.append((host, path))
    result = {'apply': apply, 'component': component, 'targets': {n: str(p) for n, p in plans}}
    if not apply:
        return result
    if meta:
        binary.parent.mkdir(parents=True, exist_ok=True)
        if not binary.exists():
            write_file(binary, data, home, None)
        with zipfile.ZipFile(source / 'materials/tools/aoci' / meta['archive']) as archive:
            for name in meta.get('notices', []):
                notice = safe_path(binary.parent, name)
                write_file(notice, archive.read(name), home, notice.read_bytes() if notice.exists() else None)
        state['aoci'] = {'version': meta['version'], 'binary': str(binary), 'sha256': meta['binary_sha256']}
    for host, path in plans:
        if host == 'aoci':
            continue
        files = cursor if host == 'cursor' else claude
        if (skill_files(path, require_entry=False) if path.exists() else None) != existing_skills[host]:
            raise ValueError(f'Skill changed during deployment: {path}')
        if not path.exists() or skill_files(path, require_entry=False) != files:
            stage = path.with_name(path.name + '.stage-' + uuid.uuid4().hex)
            stage.mkdir(parents=True)
            for rel, body in files.items():
                target = safe_path(stage, rel)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(body)
            if path.exists():
                backup = safe_path(home, '.local/share/ai-agent-config/backups/' + uuid.uuid4().hex + '/' + host + '-project-memory-kit')
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(path, backup)
            os.replace(stage, path)
        state.setdefault('skills', {})[host] = str(path)
    state['source_repo'] = str(source)
    p = state_root(home) / 'memory-tools.json'
    write_file(p, json_bytes(state), home, p.read_bytes() if p.exists() else None)
    return result


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, encoding='utf-8')


def configure(home, repo, hosts, apply, replace_aoci=False):
    home, repo = home.resolve(), repo.resolve()
    actual = git(repo, 'rev-parse', '--show-toplevel')
    if actual.returncode or os.path.normcase(str(Path(actual.stdout.strip()).resolve())) != os.path.normcase(str(repo)):
        raise ValueError('--repo must be the exact Git workspace root')
    state = read_state(home)
    binary = Path(state.get('aoci', {}).get('binary', ''))
    if not binary.is_file() or sha(binary.read_bytes()) != state['aoci']['sha256']:
        raise ValueError('Install and verify local AOCI first')
    entry = {'command': str(binary), 'args': ['--repo', str(repo), 'mcp']}
    changes = []
    paths = {'codex': '.codex/config.toml', 'claude': '.mcp.json', 'cursor': '.cursor/mcp.json'}
    for host in hosts:
        rel = paths[host]
        path = safe_path(repo, rel)
        if git(repo, 'ls-files', '--error-unmatch', '--', rel).returncode == 0:
            raise ValueError(f'Tracked host config requires manual migration: {rel}')
        before = path.read_bytes() if path.exists() else None
        raw = (before or b'').decode('utf-8-sig')
        if host == 'codex':
            parsed = tomllib.loads(raw)
            old = parsed.get('mcp_servers', {}).get('aoci')
            if old is not None and any(old.get(k) != v for k, v in entry.items()) and not replace_aoci:
                raise ValueError('Existing Codex aoci differs; review then --replace-aoci')
            fields = '\n'.join(k + ' = ' + json.dumps(v, ensure_ascii=False) for k, v in entry.items()) + '\n'
            if old is None:
                raw += ('\n' if raw and not raw.endswith('\n') else '') + '\n[mcp_servers.aoci]\n' + fields
            elif any(old.get(k) != v for k, v in entry.items()):
                match = re.search(r'(?m)^\[mcp_servers\.aoci\]\s*\n(?P<body>[\s\S]*?)(?=^\[|\Z)', raw)
                if not match:
                    raise ValueError('Noncanonical aoci TOML table requires manual editing')
                body = match.group('body')
                for k, v in entry.items():
                    line = k + ' = ' + json.dumps(v, ensure_ascii=False) + '\n'
                    body = re.sub(r'(?m)^' + k + r'\s*=.*\n?', lambda _: line, body) if re.search(r'(?m)^' + k + r'\s*=', body) else body + line
                raw = raw[:match.start('body')] + body + raw[match.end('body'):]
            tomllib.loads(raw)
            after = raw.encode('utf-8')
        else:
            parsed = json.loads(raw) if raw.strip() else {}
            servers = parsed.setdefault('mcpServers', {})
            old = servers.get('aoci')
            if old is not None and any(old.get(k) != v for k, v in entry.items()) and not replace_aoci:
                raise ValueError(f'Existing {host} aoci differs; review then --replace-aoci')
            servers['aoci'] = {**(old or {}), **entry}
            after = json_bytes(parsed)
        changes.append((path, before, after))
    ignore = safe_path(repo, '.gitignore')
    before = ignore.read_bytes() if ignore.exists() else None
    raw = (before or b'').decode('utf-8-sig')
    needed = []
    for host in hosts:
        rel = paths[host]
        if git(repo, 'check-ignore', '-q', '--', rel).returncode != 0:
            needed.append('/' + rel)
    if needed:
        raw += ('\n' if raw and not raw.endswith('\n') else '') + '\n# Local AOCI host paths (generated per machine/workspace)\n' + '\n'.join(needed) + '\n'
        changes.insert(0, (ignore, before, raw.encode('utf-8')))
    if apply:
        for path, before, after in changes:
            write_file(path, after, home, before)
    return {'apply': apply, 'repo': str(repo), 'binary': str(binary), 'configs': [str(p) for p, _, _ in changes]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['install', 'configure', 'status', 'verify'])
    parser.add_argument('--component', choices=['kit', 'aoci', 'all'], default='all')
    parser.add_argument('--hosts', nargs='+', choices=HOSTS, default=list(HOSTS))
    parser.add_argument('--repo', type=Path)
    parser.add_argument('--apply', action='store_true', help='Write the previewed changes')
    parser.add_argument('--upgrade-aoci', action='store_true', help='After upgrade checklist, allow binary version switch')
    parser.add_argument('--replace-aoci', action='store_true', help='After review, update existing aoci command/args only')
    args = parser.parse_args()
    home = Path.home()
    if args.action == 'install':
        if args.component != 'kit' and (sys.platform != 'win32' or platform.machine().lower() not in ('amd64', 'x86_64')):
            raise ValueError('Bundled AOCI currently supports Windows AMD64 only')
        result = install(SOURCE, home, args.component, args.hosts, args.apply, args.upgrade_aoci)
    elif args.action == 'configure':
        if args.repo is None:
            parser.error('configure requires --repo')
        result = configure(home, args.repo, args.hosts, args.apply, args.replace_aoci)
    elif args.action == 'verify':
        meta, _ = package(SOURCE)
        result = {'archive_verified': True, 'version': meta['version'], 'platform': meta['platform']}
    else:
        result = read_state(home)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
