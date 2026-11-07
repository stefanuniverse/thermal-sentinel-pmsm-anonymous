# Anonymity audit / 笔名发布审计

Date: 2026-11-07. Public project identity: **StefanUniverse**.
Visibility decision: **Private only**. Public conversion is not authorized.
Findings disclose locations/categories, never the private matched strings.

## Findings and remediation

| Location | Issue category | Action |
|---|---|---|
| `README.md` | Own copyright attribution | Replaced with developer pseudonym |
| `LICENSE` | Own MIT copyright attribution | Pseudonym used with owner-confirmed rights; MIT terms unchanged |
| `reports/LICENSE` | Own analysis/figure attribution | Pseudonym used; dataset/CC BY-SA attribution retained |
| `docs/ENGINEERING_AUDIT.md`, `docs/SOURCES.md` | Own author references | Pseudonym used; third-party authors and DOI unchanged |
| `CITATION.cff` | Own split personal name fields | Replaced by CFF named-entity author `StefanUniverse`; no invented identity |
| `pyproject.toml` | Package author metadata | Pseudonym used; generated wheel metadata checked separately |
| Earlier Private repository: both reachable commits | Author/committer personal-name attribution | Must not be released; no rewrite, deletion or force push |
| Earlier Private repository: historical file blobs | Earlier versions of the own attributions above | Not imported into the new repository |
| Local repository configuration | Non-pseudonymous future author name | Set locally to StefanUniverse; no global Git configuration changed |

The earlier history used the approved GitHub noreply email, not a private contact
email, but its author and committer **names** still disclosed personal identity.
Changing `user.name` or editing current files cannot fix parent commits.

## Repository decision

The owner explicitly authorized a separately initialized clean **Private**
repository named `stefanuniverse/thermal-sentinel-pmsm-anonymous`, keeping the
earlier Private repository as backup. Only reviewed file content is transferred;
no old Git objects, branches, tags, environment, raw dataset, weights or audit
rule values are transferred. No force push or old repository deletion is used.

New commit identity:

- Author and committer: `StefanUniverse`.
- Email: the exact GitHub noreply address copied by the owner from Settings >
  Emails; also matches the authenticated account ID/login. No private mailbox.
- Per-repository configuration only; no changes to any other project's identity.

## Scope and checks

- All release Markdown, licenses, citation/package metadata, source and tests.
- Known private Chinese, spaced/compact and romanized name variants, unexpected
  emails, personal filesystem paths, filenames and binary-file metadata.
- Reachable commits on all local/remote refs, all historical file versions,
  author/committer records, messages and annotated tags. Both old commits and
  all 54 historical blob versions were inspected before copying.
- PDF Info/XMP/page text, image text/EXIF/GPS; SVG XML inspected. There are no
  Office documents in the release set. Aggregate plots are unchanged.
- Third-party MIT notice, provenance and extracted TNN source have unchanged
  SHA-256 values. No blanket removal of third-party names is permitted.
- GitHub API: description/homepage, public account fields, branches, tags,
  releases, issues/comments/reviews, discussions, deployments and workflows.
  Earlier repository: Private; one branch; no tags, releases, issues, comments,
  discussions, deployments, workflow runs or artifacts; wiki disabled. Public
  account name and contact-email fields were unset at audit time.
- Browser-based settings inspection stopped because the safety check could not
  verify the current URL. No browser-policy bypass or account-setting change was
  attempted. The owner then supplied the exact noreply address directly.

## Reproducible audit

`scripts/anonymity_audit.py` checks working files, the complete index (`--index`),
all reachable history (`--history`) and GitHub metadata (`--github`). Private
spellings live only in ignored `.local/privacy-rules.json`; eleven variants
are preserved rather than removed to pass. `tests/test_anonymity.py` exercises
name/email/path findings, split citation authors, metadata-hidden identities,
side-branch historical files and third-party fingerprint tampering.

`scripts/validate_citation.py` validates against the official CFF 1.2 schema.
Optional audit tools are isolated from the frozen scientific dependency set.
See [execution instructions](docs/ANONYMITY.md).

## Remaining public-release risks

1. **Do not make the old backup public.** Its reachable history remains unsafe
   by design; never merge or cherry-pick that history into the clean repository.
2. A pseudonym/noreply address does not anonymize the whole GitHub account.
   External profiles, linked repositories, prior clones, caches and activity may
   still associate the handle with a person; they are not erased by this work.
3. Raster pixels, unknown aliases, future Office metadata, new commit trailers,
   Releases, PRs, artifacts and web edits need repeated review before release.
4. Dataset and third-party license obligations remain. Pseudonymous project
   authorship is not a relicense or removal of their attribution.
5. Institution/adviser authorship obligations, if any, and final Public approval
   remain with the owner. No industrial reliability claim is introduced.

Final execution counts, remote commit equality and test outcomes are recorded
in `docs/RELEASE_STATUS.md` after the new Private push is verified. A file-only
pass is deliberately not presented as an old-history pass.

Observed Private publication verification: new root has zero parents; all 59
remote file blob hashes match the audited local commit; approved Author and
Committer identities pass; the old Private backup HEAD is unchanged. GitHub's
other listed publication surfaces are empty and the account public name/email
fields are unset. A final audit-record commit is rechecked after its push.

## Actual change list relative to the earlier release tree

Modified (10): `CITATION.cff`, `LICENSE`, `README.md`, `pyproject.toml`,
`reports/LICENSE`, `docs/ENGINEERING_AUDIT.md`, `docs/SOURCES.md`,
`docs/PUBLIC_RELEASE_CHECKLIST.md`, `docs/RELEASE_STATUS.md`, `docs/VERIFICATION.md`.

Added (7): `ANONYMITY_AUDIT.md`, `configs/privacy-rules.example.json`,
`docs/ANONYMITY.md`, `requirements-audit.txt`, `scripts/anonymity_audit.py`,
`scripts/validate_citation.py`, `tests/test_anonymity.py`.

26 protected source/protocol/test/dependency/result/figure files match their
pre-anonymization hashes exactly. The 18-file built wheel passes the same
private-name/email/path checks and has the pseudonymous package Author field.
All 235 original research-file fingerprints remain unchanged. Local audit rules,
logs and wheel files remain ignored, outside the 59-file publication set.
