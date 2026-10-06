"""Offline deployment behavior with disposable homes and Git repositories."""
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('memory_tools', ROOT / 'scaffold/scripts/install-memory-tools.py')
mt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mt)


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.home, self.repo = [self.root / n for n in ('source', 'home', 'repo')]
        self.repo.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        bundle = self.source / 'materials/tools/aoci'
        bundle.mkdir(parents=True)
        data = b'test binary'
        with zipfile.ZipFile(bundle / 'aoci.zip', 'w') as z:
            z.writestr('aoci.exe', data)
        archive = (bundle / 'aoci.zip').read_bytes()
        self.manifest = {'version': 'test-1', 'platform': 'windows-amd64', 'archive': 'aoci.zip',
                         'archive_sha256': hashlib.sha256(archive).hexdigest(),
                         'binary_sha256': hashlib.sha256(data).hexdigest(), 'binary_member': 'aoci.exe'}
        (bundle / 'manifest.json').write_text(json.dumps(self.manifest), encoding='utf-8')
        for host in ('claude', 'cursor'):
            kit = self.source / f'materials/agent-skills/{host}/project-memory-kit'
            kit.mkdir(parents=True)
            (kit / 'SKILL.md').write_text('---\nname: project-memory-kit\nmetadata:\n  kit-version: "test-1"\n---\n', encoding='utf-8')

    def install(self, component='all', apply=True):
        return mt.install(self.source, self.home, component, ['codex', 'claude', 'cursor'], apply)

    def test_preview_has_no_writes(self):
        self.install(apply=False)
        self.assertFalse(self.home.exists())

    def test_bad_package_stops_before_skill_or_binary_write(self):
        (self.source / 'materials/tools/aoci/aoci.zip').write_bytes(b'corrupt')
        with self.assertRaises(ValueError):
            self.install()
        self.assertFalse(self.home.exists())

    def test_skill_replacement_backs_up_old_tree_and_is_identical(self):
        old = self.home / '.cursor/skills/project-memory-kit'
        old.mkdir(parents=True)
        (old / 'custom-old.txt').write_text('preserve me')
        self.install()
        self.assertFalse((old / 'custom-old.txt').exists())
        copies = list((self.home / '.local/share/ai-agent-config/backups').rglob('custom-old.txt'))
        self.assertEqual(len(copies), 1)
        self.assertEqual(copies[0].read_text(), 'preserve me')
        for rel in ('.agents/skills', '.claude/skills', '.cursor/skills'):
            self.assertEqual((self.home / rel / 'project-memory-kit/SKILL.md').read_bytes(),
                             (self.source / 'materials/agent-skills/claude/project-memory-kit/SKILL.md').read_bytes())

    def test_components_update_independently(self):
        self.install('kit')
        self.assertFalse((self.home / '.local/share/ai-agent-config/aoci').exists())
        skill = self.home / '.agents/skills/project-memory-kit/SKILL.md'
        before = skill.stat().st_mtime_ns
        self.install('aoci')
        self.assertEqual(skill.stat().st_mtime_ns, before)

    def test_configs_preserve_others_ignore_machine_paths_and_are_idempotent(self):
        self.install()
        (self.repo / '.cursor').mkdir()
        (self.repo / '.cursor/mcp.json').write_text(json.dumps({'other': 1, 'mcpServers': {'keep': {'command': 'keep'}}}))
        (self.repo / '.codex').mkdir()
        prefix = '# retain comment\nmodel = "keep"\n[mcp_servers.keep]\ncommand = "keep"\n'
        (self.repo / '.codex/config.toml').write_text(prefix)
        mt.configure(self.home, self.repo, ['codex', 'claude', 'cursor'], True)
        d = json.loads((self.repo / '.cursor/mcp.json').read_text())
        self.assertEqual(d['other'], 1)
        self.assertEqual(d['mcpServers']['keep'], {'command': 'keep'})
        self.assertEqual(d['mcpServers']['aoci']['args'], ['--repo', str(self.repo.resolve()), 'mcp'])
        self.assertTrue((self.repo / '.codex/config.toml').read_text().startswith(prefix))
        files = ['.cursor/mcp.json', '.codex/config.toml', '.mcp.json', '.gitignore']
        before = {p: (self.repo / p).read_bytes() for p in files}
        mt.configure(self.home, self.repo, ['codex', 'claude', 'cursor'], True)
        self.assertEqual(before, {p: (self.repo / p).read_bytes() for p in files})
        for p in files[:3]:
            self.assertEqual(subprocess.run(['git', '-C', str(self.repo), 'check-ignore', '-q', p]).returncode, 0)
        self.assertFalse((self.repo / 'aoci.code.txt').exists())
        self.assertFalse((self.repo / '.aoci').exists())

    def test_conflict_stops_all_config_writes(self):
        self.install()
        (self.repo / '.cursor').mkdir()
        path = self.repo / '.cursor/mcp.json'
        path.write_text('{"mcpServers":{"aoci":{"command":"other"}}}')
        old = path.read_bytes()
        with self.assertRaises(ValueError):
            mt.configure(self.home, self.repo, ['codex', 'claude', 'cursor'], True)
        self.assertEqual(path.read_bytes(), old)
        self.assertFalse((self.repo / '.mcp.json').exists())
        self.assertFalse((self.repo / '.gitignore').exists())

    def test_tracked_absolute_config_is_not_silently_rewritten(self):
        self.install()
        (self.repo / '.mcp.json').write_text('{}')
        subprocess.run(['git', '-C', str(self.repo), 'add', '.mcp.json'], check=True)
        with self.assertRaises(ValueError):
            mt.configure(self.home, self.repo, ['claude'], True)
        self.assertEqual((self.repo / '.mcp.json').read_text(), '{}')

    def test_package_path_escape_is_rejected(self):
        self.manifest['archive'] = '../../outside.zip'
        (self.source / 'materials/tools/aoci/manifest.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):
            self.install()
        self.assertFalse(self.home.exists())

    def test_upgrade_is_explicit_and_retains_old_binary(self):
        self.install('aoci')
        old = mt.read_state(self.home)['aoci']['binary']
        self.manifest['version'] = 'test-2'
        (self.source / 'materials/tools/aoci/manifest.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):
            self.install('aoci')
        self.assertEqual(mt.read_state(self.home)['aoci']['binary'], old)
        mt.install(self.source, self.home, 'aoci', ['codex'], True, upgrade_aoci=True)
        self.assertTrue(Path(old).exists())
        self.assertNotEqual(mt.read_state(self.home)['aoci']['binary'], old)

    def test_explicit_config_update_keeps_custom_options(self):
        self.install()
        (self.repo / '.mcp.json').write_text('{"mcpServers":{"aoci":{"command":"old","env":{"KEEP":"yes"}}}}')
        mt.configure(self.home, self.repo, ['claude'], True, replace_aoci=True)
        d = json.loads((self.repo / '.mcp.json').read_text())
        self.assertEqual(d['mcpServers']['aoci']['env'], {'KEEP': 'yes'})

    def test_linked_config_path_is_rejected_without_writes(self):
        self.install()
        outside = self.repo / 'outside'
        outside.mkdir()
        try:
            (self.repo / '.cursor').symlink_to(outside, target_is_directory=True)
        except OSError:
            import sys
            if sys.platform != 'win32':
                self.skipTest('symlink creation unavailable')
            created = subprocess.run(['cmd', '/c', 'mklink', '/J', str(self.repo / '.cursor'), str(outside)], capture_output=True)
            self.assertEqual(created.returncode, 0, 'junction fixture creation failed')
        with self.assertRaises(ValueError):
            mt.configure(self.home, self.repo, ['cursor'], True)
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
