import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest import mock
import subprocess

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'install-cursor-controller.py'


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'Cursor controller installer is missing')
        spec = importlib.util.spec_from_file_location('cursor_install', SCRIPT)
        self.install = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.install)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        (self.source / 'scripts').mkdir(parents=True)
        (self.source / 'SKILL.md').write_text('---\nname: cursor-cli-controller\ndescription: fixture\n---\n', encoding='utf-8')
        (self.source / 'VERSION').write_text('0.1.0\n', encoding='utf-8')
        (self.source / 'scripts' / 'mcp_server.py').write_text('# fixture\n', encoding='utf-8')
        files = {str(p.relative_to(self.source)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in self.source.rglob('*') if p.is_file()}
        self.manifest = {'version': '0.1.0', 'files': files}

    def test_verify_checks_actual_file_hashes(self):
        result = self.install.verify_source(self.source, self.manifest)
        self.assertEqual(result['version'], '0.1.0')
        (self.source / 'VERSION').write_text('tampered', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.install.verify_source(self.source, self.manifest)

    def test_dry_copy_creates_nothing(self):
        target = self.root / 'installed' / 'cursor-cli-controller'
        self.install.copy_source(self.source, target, self.manifest['files'], apply=False)
        self.assertFalse(target.exists())

    def test_copy_is_idempotent_and_preserves_private_environment(self):
        target = self.root / 'installed' / 'cursor-cli-controller'
        self.install.copy_source(self.source, target, self.manifest['files'], apply=True)
        (target / '.venv').mkdir()
        (target / '.venv' / 'marker').write_text('private')
        self.install.copy_source(self.source, target, self.manifest['files'], apply=True)
        self.assertEqual((target / '.venv' / 'marker').read_text(), 'private')
        self.assertEqual((target / 'VERSION').read_text(), '0.1.0\n')

    def test_differing_target_is_never_silently_overwritten(self):
        target = self.root / 'installed' / 'cursor-cli-controller'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('user version')
        with self.assertRaises(ValueError):
            self.install.copy_source(self.source, target, self.manifest['files'], apply=True)
        self.assertEqual((target / 'SKILL.md').read_text(), 'user version')
        self.assertFalse((target / 'VERSION').exists())

    def test_manifest_path_cannot_escape_source(self):
        with self.assertRaises(ValueError):
            self.install.verify_source(self.source, {'version': '0.1.0', 'files': {'../outside': '0'*64}})

    def test_mcp_merge_preserves_original_text_and_is_idempotent(self):
        config = self.root / 'config.toml'
        original = '# existing comments\n[mcp_servers.node_repl]\ncommand = "existing"\nargs = []\n'
        config.write_text(original, encoding='utf-8')
        python = self.root / 'python.exe'
        server = self.root / 'mcp_server.py'
        audit = self.root / 'audit'
        self.install.configure_mcp(config, python, server, audit, apply=True)
        first = config.read_text(encoding='utf-8')
        self.assertTrue(first.startswith(original))
        self.assertEqual(tomllib.loads(first)['mcp_servers']['node_repl'], {'command':'existing','args':[]})
        self.install.configure_mcp(config, python, server, audit, apply=True)
        self.assertEqual(config.read_text(encoding='utf-8'), first)
        self.assertEqual(tomllib.loads(first)['mcp_servers']['cursor-controller']['args'], [str(server), '--data-dir', str(audit)])

    def test_mcp_name_conflict_and_preview_make_no_changes(self):
        config = self.root / 'config.toml'
        self.install.configure_mcp(config, self.root/'python', self.root/'server', self.root/'audit', apply=False)
        self.assertFalse(config.exists())
        original = '[mcp_servers.cursor-controller]\ncommand = "another-server"\n'
        config.write_text(original, encoding='utf-8')
        with self.assertRaises(ValueError):
            self.install.configure_mcp(config, self.root/'python', self.root/'server', self.root/'audit', apply=True)
        self.assertEqual(config.read_text(encoding='utf-8'), original)

    def exercise_main_install(self, target, audit, check_venv_target=False):
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps(self.manifest), encoding='utf-8')
        home = self.root / 'fakehome'
        home.mkdir(exist_ok=True)
        commands = []
        def run(argv, **kwargs):
            commands.append(argv)
            if argv[1:3] == ['-m', 'venv']:
                if check_venv_target:
                    self.assertEqual(Path(argv[3]), home / 'sandbox' / 'cursor-cli-controller' / '.venv')
                python = Path(argv[3]) / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
                python.parent.mkdir(parents=True, exist_ok=True)
                python.write_text('fixture interpreter', encoding='utf-8')
            return subprocess.CompletedProcess(argv, 0, stdout='2.3.0\n', stderr='')
        with mock.patch.object(self.install, 'SOURCE', self.source), mock.patch.object(self.install, 'MANIFEST', manifest), \
             mock.patch.dict(os.environ, {'USERPROFILE':str(home), 'HOME':str(home)}), \
             mock.patch.object(self.install.sys, 'argv', ['installer','install','--apply','--target',str(target),'--data-dir',str(audit)]), \
             mock.patch.object(self.install.subprocess, 'run', side_effect=run):
            self.assertEqual(self.install.main(), 0)
        return commands, home

    def test_main_resolves_tilde_target_for_source_and_private_environment(self):
        commands, home = self.exercise_main_install('~/sandbox/cursor-cli-controller', self.root/'audit', check_venv_target=True)
        self.assertTrue((home/'sandbox/cursor-cli-controller/SKILL.md').is_file())
        self.assertTrue((home/'sandbox/cursor-cli-controller/.venv/Scripts/python.exe').is_file() if os.name=='nt' else
                        (home/'sandbox/cursor-cli-controller/.venv/bin/python').is_file())

    def test_install_doctor_uses_selected_audit_directory(self):
        audit = self.root / 'isolated-audit'
        commands, _ = self.exercise_main_install(self.root/'installed/cursor-cli-controller', audit)
        doctor = commands[-1]
        self.assertEqual(doctor[-3:], ['--data-dir',str(audit),'doctor'])


if __name__ == '__main__':
    unittest.main()
