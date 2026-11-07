"""Synthetic privacy fixtures are not project author identities."""
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/anonymity_audit.py'
spec = importlib.util.spec_from_file_location('privacy_audit', SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def rules():
    return {'pseudonym': 'StefanUniverse',
            'noreply_email': '306132924+stefanuniverse@users.noreply.github.com',
            'personal_identifiers': ['Example Person', 'ExamplePerson', '\u6d4b\u8bd5\u59d3\u540d'],
            'third_party_sha256': {}, 'reviewed_third_party_emails': []}


class AnonymityTests(unittest.TestCase):
    def test_private_variants_report_categories_only(self):
        worker = audit.Auditor(rules())
        worker.text('exampleperson and \u6d4b\u8bd5\u59d3\u540d', 'test.md')
        self.assertTrue(worker.findings)
        self.assertNotIn('ExamplePerson', str(worker.findings))
        self.assertTrue(all(q['category'] == 'personal_name' for q in worker.findings))

    def test_noreply_only_and_private_paths(self):
        worker = audit.Auditor(rules())
        worker.text(rules()['noreply_email'], 'allowed')
        self.assertEqual(worker.findings, [])
        worker.text('private' + '@' + 'mail.test', 'mail')
        worker.text('C:' + '/Users/' + 'someone/project', 'path')
        self.assertEqual({q['category'] for q in worker.findings}, {'unexpected_email', 'private_local_path'})

    def test_split_citation_and_package_authorship(self):
        worker = audit.Auditor(rules())
        worker.blob('CITATION.cff', b'authors:\n  - family-names: Example\n    given-names: Person\nversion: 0.1.0', 'citation')
        self.assertIn('non_pseudonymous_citation_author', {q['category'] for q in worker.findings})
        worker = audit.Auditor(rules())
        worker.blob('CITATION.cff', b'authors:\n  - name: "StefanUniverse"\nversion: 0.1.0', 'citation')
        worker.blob('pyproject.toml', b'[project]\nauthors = [{name = "StefanUniverse"}]', 'package')
        self.assertEqual(worker.findings, [])

    def test_third_party_identity_is_not_blanket_redacted(self):
        worker = audit.Auditor(rules())
        worker.text('Wilhelm Kirchg\u00e4ssner, MIT; doi:10.1016/j.engappai.2022.105537', 'third-party')
        self.assertEqual(worker.findings, [])
        worker.author('Example Person', rules()['noreply_email'], 'git-author')
        self.assertIn('non_pseudonymous_git_identity', {q['category'] for q in worker.findings})

    def test_metadata_hidden_identity(self):
        try:
            from pypdf import PdfWriter
            from PIL import Image, PngImagePlugin
        except ImportError:
            self.skipTest('Install requirements-audit.txt for binary metadata tests.')
        worker = audit.Auditor(rules())
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        writer.add_metadata({'/Author': 'Example Person'})
        output = io.BytesIO()
        writer.write(output)
        worker.blob('figure.pdf', output.getvalue(), 'pdf')
        image = Image.new('RGB', (2, 2))
        info = PngImagePlugin.PngInfo()
        info.add_text('Author', 'Example Person')
        output = io.BytesIO()
        image.save(output, format='PNG', pnginfo=info)
        worker.blob('figure.png', output.getvalue(), 'png')
        self.assertTrue(any(q['location'].startswith('pdf:') for q in worker.findings))
        self.assertTrue(any(q['location'].startswith('png:') for q in worker.findings))

    def test_side_branch_and_removed_historical_file_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def command(*args):
                return subprocess.run(['git', '-c', f'safe.directory={root.as_posix()}', *args],
                                      cwd=root, capture_output=True, check=True)
            command('init', '--initial-branch=codex/test')
            command('config', 'user.name', 'StefanUniverse')
            command('config', 'user.email', rules()['noreply_email'])
            (root / 'test.md').write_text('Example Person', encoding='utf-8')
            command('add', 'test.md')
            command('commit', '-m', 'Synthetic fixture')
            command('branch', 'codex/side')
            (root / 'test.md').write_text('StefanUniverse', encoding='utf-8')
            command('add', 'test.md')
            command('commit', '-m', 'Remove visible fixture')
            worker = audit.Auditor(rules())
            with patch.object(audit, 'ROOT', root):
                worker.history()
            self.assertEqual(worker.counts['reachable_commits'], 2)
            self.assertTrue(any(q['location'].startswith('git-blob:') for q in worker.findings))

    def test_license_fingerprint_changes_are_blocked(self):
        worker = audit.Auditor(rules())
        worker.rules['third_party_sha256'] = {'third_party/LICENSE-TNN': '0' * 64}
        worker.third_party()
        self.assertEqual(worker.findings[0]['category'], 'third_party_attribution_changed')


if __name__ == '__main__':
    unittest.main()
