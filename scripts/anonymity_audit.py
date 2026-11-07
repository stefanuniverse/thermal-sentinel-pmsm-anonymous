"""Fail-closed publication privacy audit. Never print matched private values.

Known private spellings belong in an ignored, local rules file, not this source.
Git history is inspected, never rewritten. --github is read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.local', '.tools', '.venv', 'node_modules', '__pycache__',
        '.pytest_cache', 'build', 'dist'}
EMAIL = re.compile(r'(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}')
PRIVATE_PATH = re.compile(
    r'(?i)(?:[a-z]:[\\/]+Users[\\/]+[^\s<>"\x00\x27]+|'
    r'/(?:Users|home)/[^\s<>"\x00\x27]+|file:' r'//[^\s<>"\x00\x27]+)')
TEXT_SUFFIXES = {'.md', '.py', '.toml', '.json', '.txt', '.yaml', '.yml', '.cff',
                 '.csv', '.svg', '.html', '.js', '.mjs', '.xml', '.cfg', '.ini'}
MEDIA_SUFFIXES = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.webp'}


def run(args, *, cwd=ROOT):
    p = subprocess.run(args, cwd=cwd, capture_output=True)
    if p.returncode:
        # stderr may contain a private path, credential URL or identity.
        raise RuntimeError(f'command_failed_exit_{p.returncode}')
    return p.stdout


def git(*args):
    return run(['git', '-c', f'safe.directory={ROOT.as_posix()}', *args], cwd=ROOT)


def canonical(value):
    return unicodedata.normalize('NFKC', value).casefold()


class Auditor:
    def __init__(self, rules):
        self.rules = rules
        self.names = [canonical(s) for s in rules['personal_identifiers'] if s.strip()]
        self.email = rules['noreply_email'].casefold()
        self.pseudonym = rules['pseudonym']
        self.findings = []
        self.notes = []
        self.metadata = []
        self.counts = {}

    def finding(self, location, category, line=None):
        for name in self.rules['personal_identifiers']:
            if name:
                location = re.sub(re.escape(name), '[PRIVATE]', location, flags=re.I)
        location = EMAIL.sub(lambda m: m.group() if m.group().casefold() == self.email else '[EMAIL]', location)
        location = PRIVATE_PATH.sub('[LOCAL_PATH]', location)
        item = {'location': location, 'category': category}
        if line is not None:
            item['line'] = line
        if item not in self.findings:
            self.findings.append(item)

    def text(self, value, location):
        normalized = canonical(value)
        for name in self.names:
            # Compact/spaced/romanized spellings are explicitly seeded privately.
            if not name:
                continue
            pattern = re.escape(name)
            if name.isascii():
                pattern = r'(?<![a-z])' + pattern + r'(?![a-z])'
            for m in re.finditer(pattern, normalized):
                self.finding(location, 'personal_name', normalized[:m.start()].count('\n') + 1)
        for m in EMAIL.finditer(value):
            address = m.group().casefold()
            if address == self.email or address.endswith(('@example.invalid', '@example.com')):
                continue
            if address in self.rules.get('reviewed_third_party_emails', []):
                continue
            self.finding(location, 'unexpected_email', value[:m.start()].count('\n') + 1)
        for m in PRIVATE_PATH.finditer(value):
            self.finding(location, 'private_local_path', value[:m.start()].count('\n') + 1)

    def author(self, name, email, location):
        self.text(name + '\n' + email, location)
        if name != self.pseudonym:
            self.finding(location, 'non_pseudonymous_git_identity')
        if email.casefold() != self.email:
            self.finding(location, 'non_approved_git_email')

    def creator(self, value, location):
        self.text(str(value), location)
        if str(value).strip() and str(value).strip() != self.pseudonym:
            self.finding(location, 'unreviewed_authorship_metadata')

    def blob(self, path, data, location):
        self.text(path, location + ':filename')
        suffix = Path(path).suffix.lower()
        if suffix == '.pdf':
            try:
                from pypdf import PdfReader
                reader = PdfReader(io.BytesIO(data))
                info = dict(reader.metadata or {})
                for key, value in info.items():
                    self.text(str(value), location + ':pdf-info:' + key)
                for key in ('/Author', '/LastModifiedBy'):
                    if info.get(key):
                        self.creator(info[key], location + ':pdf-info:' + key)
                # Include XMP as well as the visible page text and attachments.
                meta = reader.trailer['/Root'].get('/Metadata')
                if meta:
                    self.text(meta.get_object().get_data().decode('utf-8', 'replace'), location + ':pdf-xmp')
                for index, page in enumerate(reader.pages):
                    self.text(page.extract_text() or '', f'{location}:page:{index + 1}')
                for key, attachments in reader.attachments.items():
                    self.text(key, location + ':attachment-name')
                    for attachment in attachments:
                        self.blob(key, attachment, location + ':attachment')
                self.metadata.append({'location': location, 'format': 'PDF', 'checked': True})
            except Exception:
                self.finding(location, 'pdf_metadata_not_fully_inspected')
        elif suffix in MEDIA_SUFFIXES:
            try:
                from PIL import Image
                with Image.open(io.BytesIO(data)) as image:
                    for key, value in image.info.items():
                        if isinstance(value, (str, bytes)) and key != 'icc_profile':
                            s = value.decode('utf-8', 'replace') if isinstance(value, bytes) else value
                            self.text(s, location + ':image-info:' + key)
                            if key.casefold() in {'author', 'artist', 'creator', 'copyright'}:
                                self.creator(s, location + ':image-info:' + key)
                    exif = image.getexif()
                    for key, value in exif.items():
                        self.text(str(value), location + ':exif:' + str(key))
                        if key in (315, 33432, 40093):
                            self.creator(value, location + ':exif:' + str(key))
                    if exif.get_ifd(34853):
                        self.finding(location, 'geolocation_metadata')
                self.metadata.append({'location': location, 'format': 'image', 'checked': True})
            except Exception:
                self.finding(location, 'image_metadata_not_fully_inspected')
        elif suffix in {'.docx', '.pptx', '.xlsx', '.odt', '.ods', '.odp'}:
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    for name in archive.namelist():
                        if name.endswith(('.xml', '.rels')):
                            value = archive.read(name).decode('utf-8', 'replace')
                            self.text(value, location + ':' + name)
                            for creator in re.findall(r'<(?:dc:creator|cp:lastModifiedBy)[^>]*>(.*?)</', value):
                                self.creator(creator, location + ':' + name)
                self.metadata.append({'location': location, 'format': 'Office/ODF', 'checked': True})
            except Exception:
                self.finding(location, 'office_metadata_not_fully_inspected')
        elif suffix in {'.doc', '.ppt', '.xls', '.zip', '.ipynb'}:
            self.finding(location, 'manual_binary_review_required')
        elif suffix in TEXT_SUFFIXES or suffix == '' or Path(path).name.startswith('.'):
            value = data.decode('utf-8', 'replace')
            self.text(value, location)
            if path == 'CITATION.cff':
                # Split family/given names must not evade a full-name rule.
                authors = value.split('authors:', 1)[-1].split('version:', 1)[0]
                if re.search(r'(?:family-names|given-names):', authors) or not re.search(
                        r'-\s*name:\s*["\x27]?' + re.escape(self.pseudonym) + r'["\x27]?\s*$', authors, re.M):
                    self.finding(location, 'non_pseudonymous_citation_author')
            if path == 'pyproject.toml':
                import tomllib
                authors = tomllib.loads(value).get('project', {}).get('authors', [])
                if authors != [{'name': self.pseudonym}]:
                    self.finding(location, 'non_pseudonymous_package_author')
        else:
            self.finding(location, 'unreviewed_file_format')

    def working_tree(self):
        # Includes untracked publishable files; ignored research data is excluded.
        paths = git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split(b'\0')
        seen = set()
        for encoded in paths:
            if not encoded:
                continue
            path = encoded.decode('utf-8')
            if path in seen:
                continue
            seen.add(path)
            target = ROOT / path
            if target.is_symlink():
                self.finding(path, 'symlink_requires_review')
            elif target.is_file():
                self.blob(path, target.read_bytes(), path)
        self.counts['working_tree_files'] = len(seen)
        for setting in ('user.name', 'user.email'):
            try:
                value = git('config', '--local', '--get', setting).decode().strip()
                expected = self.pseudonym if setting == 'user.name' else self.email
                if value != expected:
                    self.finding('git-config:' + setting, 'non_approved_future_commit_identity')
            except RuntimeError:
                self.finding('git-config:' + setting, 'missing_local_commit_identity')

    def history(self):
        refs = git('for-each-ref', '--format=%(refname)').decode().splitlines()
        self.counts['local_refs'] = len(refs)
        for ref in refs:
            self.text(ref, 'git-ref')
        commits = git('rev-list', '--all').decode().splitlines()
        if not commits:
            self.notes.append('No reachable commits; this is not a history pass for a published repository.')
        self.counts['reachable_commits'] = len(commits)
        for oid in commits:
            raw = git('cat-file', 'commit', oid).decode('utf-8', 'replace')
            self.text(raw, 'git-commit:' + oid[:12])
            for role, name, email in re.findall(r'^(author|committer) (.*?) <([^>]*)>', raw, re.M):
                self.author(name, email, f'git-commit:{oid[:12]}:{role}')
        blob_paths = {}
        for commit in commits:
            tree = git('ls-tree', '-rz', commit)
            for entry in tree.split(b'\0'):
                if not entry:
                    continue
                header, name = entry.split(b'\t', 1)
                mode, kind, oid = header.decode().split()
                path = name.decode('utf-8')
                self.text(path, 'git-history-filename:' + commit[:12])
                if kind == 'blob':
                    blob_paths.setdefault((oid, Path(path).suffix.lower()), path)
                elif kind == 'commit':
                    self.finding('git-history:' + path, 'submodule_not_audited')
        self.counts['historical_blob_versions'] = len(blob_paths)
        for (oid, _), path in blob_paths.items():
            self.blob(path, git('cat-file', 'blob', oid), f'git-blob:{oid[:12]}:{path}')
        for row in git('for-each-ref', '--format=%(refname) %(objecttype) %(objectname)', 'refs/tags').decode().splitlines():
            ref, kind, oid = row.split()
            if kind == 'tag':
                self.text(git('cat-file', 'tag', oid).decode('utf-8', 'replace'), 'git-tag:' + ref)
        self.notes.append('All reachable refs/commits/blobs/tags inspected; reflogs, unreachable objects, remote caches and other people\'s clones are not erased or certified.')

    def index(self):
        entries = git('ls-files', '--stage', '-z').split(b'\0')
        self.counts['index_files'] = 0
        for entry in entries:
            if not entry:
                continue
            header, encoded = entry.split(b'\t', 1)
            mode, oid, stage = header.decode().split()
            path = encoded.decode('utf-8')
            if stage != '0' or mode != '100644':
                self.finding('index:' + path, 'non_regular_index_entry')
                continue
            self.blob(path, git('cat-file', 'blob', oid), 'index:' + path)
            self.counts['index_files'] += 1

    def third_party(self):
        for path, expected in self.rules['third_party_sha256'].items():
            p = ROOT / path
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
                self.finding(path, 'third_party_attribution_changed')
        self.counts['frozen_third_party_files'] = len(self.rules['third_party_sha256'])

    def github(self, gh, repository):
        def api(endpoint, paginated=False):
            args = [str(gh), 'api', endpoint]
            if paginated:
                args.extend(['--paginate', '--slurp'])
            result = json.loads(run(args))
            if paginated and isinstance(result, list):
                return [item for page in result for item in (page if isinstance(page, list) else [page])]
            return result

        repo = api('repos/' + repository)
        self.counts['github_private'] = repo['private']
        if not repo['private']:
            self.finding('github:repository', 'repository_not_private')
        for field in ('description', 'homepage', 'name', 'full_name'):
            self.text(str(repo.get(field) or ''), 'github:repository:' + field)
        profile = api('user')
        for field in ('name', 'email', 'bio', 'company', 'location', 'blog'):
            self.text(str(profile.get(field) or ''), 'github:account:' + field)
        self.counts['github_account_public_name_set'] = bool(profile.get('name'))
        self.counts['github_account_public_email_set'] = bool(profile.get('email'))
        for endpoint in ('branches', 'tags', 'releases', 'issues?state=all&per_page=100',
                         'issues/comments?per_page=100', 'pulls/comments?per_page=100',
                         'comments?per_page=100', 'milestones?state=all&per_page=100',
                         'deployments?per_page=100'):
            records = api(f'repos/{repository}/{endpoint}', True)
            label = endpoint.split('?')[0]
            self.counts['github_' + label.replace('/', '_')] = len(records)
            for record in records:
                # Full JSON inspected internally; identity values never printed.
                self.text(json.dumps(record, ensure_ascii=False), f'github:{label}:record:{record.get("id", "ref")}')
                if label == 'issues' and 'pull_request' in record:
                    reviews = api(f'repos/{repository}/pulls/{record["number"]}/reviews?per_page=100', True)
                    self.text(json.dumps(reviews, ensure_ascii=False), 'github:pull-review')
        for endpoint, key in (('actions/runs?per_page=100', 'workflow_runs'),
                              ('actions/artifacts?per_page=100', 'artifacts')):
            pages = api(f'repos/{repository}/{endpoint}', True)
            rows = [row for page in pages for row in page[key]]
            self.counts['github_' + key] = len(rows)
            self.text(json.dumps(rows, ensure_ascii=False), 'github:' + key)
            if rows:
                self.finding('github:' + key, 'artifact_or_log_contents_require_review')
        # Discussions have an independent GraphQL surface.
        query = ('query($owner:String!,$name:String!,$cursor:String){repository(owner:$owner,name:$name)'
                 '{discussions(first:100,after:$cursor){nodes{id title body comments(first:100)'
                 '{nodes{body} pageInfo{hasNextPage}}} pageInfo{hasNextPage endCursor}}}}')
        owner, name = repository.split('/')
        cursor = None
        discussion_count = 0
        while True:
            args = [str(gh), 'api', 'graphql', '-f', 'query=' + query,
                    '-F', 'owner=' + owner, '-F', 'name=' + name]
            if cursor:
                args.extend(['-F', 'cursor=' + cursor])
            response = json.loads(run(args))
            if response.get('errors'):
                self.finding('github:discussions', 'remote_surface_unavailable')
                break
            discussions = response['data']['repository']['discussions']
            discussion_count += len(discussions['nodes'])
            self.text(json.dumps(discussions['nodes'], ensure_ascii=False), 'github:discussions')
            if any(row['comments']['pageInfo']['hasNextPage'] for row in discussions['nodes']):
                self.finding('github:discussions', 'nested_comment_pagination_required')
            if not discussions['pageInfo']['hasNextPage']:
                break
            cursor = discussions['pageInfo']['endCursor']
        self.counts['github_discussions'] = discussion_count
        self.counts['github_wiki_enabled'] = repo.get('has_wiki', False)
        if repo.get('has_wiki'):
            self.notes.append('Wiki enabled flag is not evidence of an existing wiki; separate wiki Git endpoint must be checked before public release.')
        self.notes.append('Remote issue/release/ref/account metadata checked read-only; no account or repository visibility settings changed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rules', type=Path, default=ROOT / '.local/privacy-rules.json')
    parser.add_argument('--history', action='store_true')
    parser.add_argument('--index', action='store_true', help='Inspect all index blobs, not just working files.')
    parser.add_argument('--github', action='store_true')
    parser.add_argument('--gh', type=Path, default=ROOT / '.tools/gh/bin/gh.exe')
    parser.add_argument('--repository', default='stefanuniverse/thermal-sentinel-pmsm-anonymous')
    parser.add_argument('--output', type=Path, default=ROOT / '.local/anonymity-latest.json')
    args = parser.parse_args()
    if not args.rules.is_file():
        print(json.dumps({'passed': False, 'category': 'private_rules_missing',
                          'instruction': 'Create ignored local rules; never put personal spellings in tracked code.'}))
        return 2
    rules = json.loads(args.rules.read_text(encoding='utf-8'))
    auditor = Auditor(rules)
    if not rules.get('personal_identifiers'):
        auditor.finding('audit-rules', 'empty_private_name_rules')
    try:
        auditor.working_tree()
        auditor.third_party()
        if args.history:
            auditor.history()
        if args.index:
            auditor.index()
        if args.github:
            auditor.github(args.gh, args.repository)
    except Exception as exc:
        # No exception repr: parsers/CLI can echo sensitive source material.
        auditor.finding('audit', 'incomplete_scan_' + type(exc).__name__)
    result = {'passed': not auditor.findings, 'counts': auditor.counts,
              'findings': auditor.findings, 'metadata': auditor.metadata, 'notes': auditor.notes,
              'known_private_spellings': len(rules['personal_identifiers']),
              'privacy': 'Matched values and identity spellings are never included in this report.',
              'limits': 'Known spellings/patterns and metadata inspection are not proof of anonymity; raster pixels, unknown aliases, external links, browser account settings and server caches require human review.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
