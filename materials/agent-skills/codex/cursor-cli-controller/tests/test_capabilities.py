"""Bounded, read-only prerequisite observations using real workspace entries."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from cursor_runtime import Controller


class ProjectMemoryCapabilitiesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name) / 'workspace'
        self.work.mkdir()
        self.controller = Controller(Path(self.temp.name) / 'data')

    def observe(self):
        # Doctor probes are tested separately; this suite never calls a live agent.
        with patch.object(self.controller, 'doctor', return_value={'available': False}):
            observed = self.controller.capabilities(str(self.work), [])
        self.assertIn('project_memory', observed)
        return observed['project_memory']

    def entry(self, relative, text):
        path = self.work / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def test_no_kit_is_normal_and_does_not_initialize(self):
        memory = self.observe()
        self.assertIs(memory['present'], False)
        self.assertIsNone(memory['entrypoint'])
        self.assertIsNone(memory['root'])
        self.assertIsNone(memory['layout'])
        self.assertIsNone(memory['memory_schema_version'])
        self.assertEqual(memory['aoci_state'], 'unknown')
        self.assertEqual(list(self.work.iterdir()), [])

    def test_docs_memory_reports_explicit_schema_and_enabled_aoci(self):
        entry = self.entry('docs/memory/MEMORY.md', '> **本记忆按 kit v1.5.0 建立。**\n- AOCI：已启用。<!-- kit:aoci-status -->\n')
        memory = self.observe()
        self.assertTrue(memory['present'])
        self.assertEqual(memory['entrypoint'], str(entry.resolve()))
        self.assertEqual(memory['root'], str(entry.parent.resolve()))
        self.assertEqual(memory['layout'], 'docs/memory')
        self.assertEqual(memory['memory_schema_version'], 'v1.5.0')
        self.assertEqual(memory['aoci_state'], 'enabled')

    def test_repository_layout_does_not_take_progress_version_for_schema(self):
        entry = self.entry('memory/kit/MEMORY.md', '- 当前进度：Kit v1.7.1 已部署。\n> **本记忆按 kit v1.5.0 建立。**\n- AOCI：MCP 已绑定本仓，索引未初始化；新项目单独选择。<!-- kit:aoci-status -->\n')
        memory = self.observe()
        self.assertEqual(memory['entrypoint'], str(entry.resolve()))
        self.assertEqual(memory['layout'], 'memory/kit')
        self.assertEqual(memory['memory_schema_version'], 'v1.5.0')
        self.assertEqual(memory['aoci_state'], 'configured_not_initialized')
        self.assertIn('索引未初始化', memory['aoci_status_line'])

    def test_enabled_but_unavailable_remains_enabled(self):
        self.entry('ROOT-MEMORY.md', '- AOCI：已启用但不可用/待维护。<!-- kit:aoci-status -->\n')
        memory = self.observe()
        self.assertEqual(memory['layout'], 'workspace_root')
        self.assertEqual(memory['aoci_state'], 'enabled')
        self.assertIn('不可用/待维护', memory['aoci_status_line'])

    def test_only_explicit_aoci_marker_is_authoritative(self):
        self.entry('docs/memory/ROOT-MEMORY.md', '# Kit v9.8.7\nAOCI 已启用\n')
        memory = self.observe()
        self.assertTrue(memory['present'])
        self.assertEqual(memory['aoci_state'], 'unknown')
        self.assertIsNone(memory['memory_schema_version'])

    def test_disabled_marker_and_bounded_status(self):
        self.entry('docs/memory/MEMORY.md', 'AOCI：未启用。' + '说明' * 1000 + '<!-- kit:aoci-status -->\n')
        memory = self.observe()
        self.assertEqual(memory['aoci_state'], 'disabled')
        self.assertLessEqual(len(memory['aoci_status_line']), 1000)

    def test_unreadable_entry_reports_diagnostic_instead_of_absence(self):
        entry = self.entry('docs/memory/MEMORY.md', '# memory')
        open_original = Path.open

        def denied(path, *args, **kwargs):
            if path == entry:
                raise PermissionError('isolated unreadable fixture')
            return open_original(path, *args, **kwargs)

        with patch.object(Path, 'open', denied):
            memory = self.observe()
        self.assertTrue(memory['present'])
        self.assertEqual(memory['aoci_state'], 'unknown')
        self.assertEqual(memory['diagnostic']['code'], 'entry_unreadable')

    def test_relative_entry_symlink_resolves_only_inside_workspace(self):
        target = self.entry('memory/kit/MEMORY.md', '> 本记忆按 kit v1.5.0 建立。\n')
        link = self.work / 'ROOT-MEMORY.md'
        try:
            link.symlink_to(Path('memory') / 'kit' / 'MEMORY.md')
        except OSError as error:
            self.skipTest('Local account cannot create symlinks: ' + str(error))
        # Remove other known entry as a candidate by using a nonstandard target.
        target.rename(target.with_name('entry.md'))
        link.unlink()
        link.symlink_to(Path('memory') / 'kit' / 'entry.md')
        memory = self.observe()
        self.assertEqual(memory['entrypoint'], str(target.with_name('entry.md').resolve()))
        self.assertEqual(memory['layout'], 'workspace_root')

    def test_outside_entry_symlink_returns_diagnostic_without_reading(self):
        outside = Path(self.temp.name) / 'outside.md'
        outside.write_text('AOCI enabled <!-- kit:aoci-status -->', encoding='utf-8')
        try:
            (self.work / 'ROOT-MEMORY.md').symlink_to(Path('..') / 'outside.md')
        except OSError as error:
            self.skipTest('Local account cannot create symlinks: ' + str(error))
        memory = self.observe()
        self.assertIsNone(memory['present'])
        self.assertEqual(memory['aoci_state'], 'unknown')
        self.assertEqual(memory['diagnostic']['code'], 'entry_outside_workspace')
