from __future__ import annotations
import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / 'skills/superCoder/scripts/coder_knowledge.py'
FIXTURE = ROOT / 'tests/skill-behavior/fixtures/completion-materialization/valid-repo/.coder'
PROJECT = 'demo-20260715'

class ArtifactRootTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name).resolve()
        self.repo = self.base / 'repo'
        self.repo.mkdir()
        self.shared = self.base / 'shared ledger' / '.coder'
        shutil.copytree(FIXTURE, self.shared)

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, command, *args, repo=None, root=None):
        argv = [sys.executable, '-B', str(CLI), command, '--repo', str(repo or self.repo), *args]
        if root is not None:
            argv += ['--artifact-root', str(root)]
        result = subprocess.run(argv, text=True, capture_output=True)
        return result.returncode, json.loads(result.stdout)

    def test_two_git_worktrees_share_read_write_and_index(self):
        def git(*args):
            subprocess.run(['git', '-C', str(self.repo), *args], check=True, capture_output=True)
        git('init')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.test', 'commit', '--allow-empty', '-m', 'fixture')
        other = self.base / 'worktree'
        git('worktree', 'add', '-b', 'second', str(other))
        for repo in (self.repo, other):
            code, body = self.cli('locate', '--project-id', PROJECT, repo=repo, root=self.shared)
            self.assertEqual(0, code, body)
            self.assertEqual(str(self.shared / PROJECT / 'requirement-knowledge-card.md'), body['data']['path'])
        code, body = self.cli('materialize', '--project-id', PROJECT, repo=other, root=self.shared)
        self.assertEqual(0, code, body)
        self.assertTrue((self.shared / PROJECT / 'requirement-delivery-summary.md').is_file())
        self.assertEqual(0, self.cli('validate-index', root=self.shared)[0])
        code, body = self.cli('metadata', '--project-id', PROJECT, root=self.shared)
        self.assertEqual('ACCEPTED', body['data']['resource']['status'])
        self.assertFalse((self.repo / '.coder').exists())
        self.assertFalse((other / '.coder').exists())

    def test_root_inside_one_worktree_has_portable_index(self):
        local = self.repo / '.coder'
        shutil.copytree(FIXTURE, local)
        other = self.base / 'other'
        other.mkdir()
        self.assertEqual(0, self.cli('rebuild-index', root=local)[0])
        code, body = self.cli('validate-index', repo=other, root=local)
        self.assertEqual(0, code, body)
        code, body = self.cli('find', '--module', 'module-1', repo=other, root=local)
        self.assertEqual(0, code, body)
        self.assertTrue(Path(body['data']['requirements'][0]['source_path']).is_absolute())

    def test_relative_root_is_based_on_repo_and_all_queries_use_it(self):
        for command, args in [('rebuild-index', []), ('validate-index', []),
                              ('find', ['--module', 'module-1']),
                              ('tree', ['--module', 'module-1']),
                              ('validate-module', ['--module-id', 'module-1']),
                              ('section', ['--project-id', PROJECT, '--section', 'changes'])]:
            code, body = self.cli(command, *args, root='../shared ledger/.coder')
            self.assertEqual(0, code, body)

    def test_no_fallback_to_default_when_selected_root_is_missing(self):
        shutil.copytree(FIXTURE, self.repo / '.coder')
        self.assertEqual(0, self.cli('locate', '--project-id', PROJECT)[0])
        code, body = self.cli('locate', '--project-id', PROJECT, root='missing')
        self.assertNotEqual(0, code)
        self.assertEqual('NOT_FOUND', body['issues'][0]['code'])

    def test_traversal_and_symlink_escape_are_blocked(self):
        for selector in ('../shared ledger/.coder/' + PROJECT, str(self.shared / PROJECT)):
            code, body = self.cli('locate', '--project-id', selector, root=self.shared)
            self.assertNotEqual(0, code)
            self.assertEqual('INVALID_SCOPE', body['issues'][0]['code'])
        (self.shared / 'escape').symlink_to(self.shared.parent.parent / 'repo', target_is_directory=True)
        code, body = self.cli('locate', '--project-id', 'escape', root=self.shared)
        self.assertEqual('INVALID_SCOPE', body['issues'][0]['code'])
        input_path = self.shared / PROJECT / 'records/completion-input.json'
        outside = self.base / 'input.json'
        input_path.rename(outside)
        input_path.symlink_to(outside)
        code, body = self.cli('materialize', '--project-id', PROJECT, root=self.shared)
        self.assertEqual('INVALID_SCOPE', body['issues'][0]['code'])
        self.assertFalse((self.shared / PROJECT / 'requirement-delivery-summary.md').exists())

if __name__ == '__main__':
    unittest.main()
