# Pseudonymous publication checks

Project-original attribution is **StefanUniverse**. This is a developer pseudonym,
not a claim about a legal person, institution or ORCID. The owner confirmed rights
to the original code and MIT licensing; third-party ownership is unchanged.

## Local-only private rules

1. Install `requirements-audit.txt` in an audit environment (not the frozen
   scientific environment).
2. Copy `configs/privacy-rules.example.json` to `.local/privacy-rules.json`.
3. Put known legal-name spellings, separated/compact Chinese forms and romanized
   aliases in `personal_identifiers` **locally only**. Do not commit this file.
   The owner's actual eleven variants are retained in the local audit copy.
4. Confirm the exact noreply address from GitHub Settings > Emails. The current
   address was supplied by the owner from that setting, not guessed from a name.
5. Retain the reviewed third-party file fingerprints. Do not remove private-name
   rules, weaken patterns or edit copyright notices to obtain a green result.

Run before committing and again after committing:

```bash
python scripts/anonymity_audit.py --history --index
python scripts/security_scan.py
python -m unittest discover -s tests -p test_anonymity.py -v
```

`--index` inspects the **entire staged tree**, including unchanged staged files.
`--history` walks every locally reachable branch, remote ref, tag and historical
blob; it checks author, committer, commit messages and annotated tag content.
Fetch every remote branch and tag first. A nonzero exit code means the audit
failed or could not inspect a required surface; it is not a pass.

With owner-authorized GitHub CLI credentials, also run:

```bash
python scripts/anonymity_audit.py --history --index --github \
  --gh /path/to/gh --repository stefanuniverse/thermal-sentinel-pmsm-anonymous
```

The API pass is read-only. It checks Private visibility, profile public fields,
repository description/homepage, branch/tag/release metadata, all issues and
comments, review comments, discussions, deployments and workflow/artifact
inventory. Nonempty artifact/log or nested discussion surfaces fail closed for
further review. It does not change account privacy settings.

## Metadata and attribution

The scanner inspects PDF Info/XMP/text/attachments, PNG/JPEG EXIF and text fields,
and Office/ODF XML including creator and last editor. Unknown binary formats and
inspection failures block a pass. SVG text and metadata are inspected as XML
text. Current release assets contain no Office files, no personal-author EXIF
and no location metadata. Raster image pixels still require visual inspection.

TNN code, its MIT notice and pinned provenance are fingerprinted before edits.
Legitimate third-party names, DOI references and dataset acknowledgements remain.
Their presence is not a personal-identity finding.

## Important boundaries

- Never push this `.local/` directory, raw data, local environments or audit keys.
- A normal new commit cannot remove identity from its parents. Do not make the
  old Private backup public. Do not merge/cherry-pick its commits into the clean
  repository; transfer reviewed file content only.
- No force push, deletion, tag rewrite or Public conversion is part of this work.
- History scanners cannot erase GitHub caches, earlier clones, external links,
  existing account associations or information a third party already received.
- Pseudonymity is not untraceability. Account ID, public handle and commit times
  remain linkable; unrelated account settings need separate owner review.
- The actual `.local/` rules and per-run findings are deliberately not published.

## Source specifications

- [CFF 1.2 schema](https://github.com/citation-file-format/citation-file-format/blob/1.2.0/schema.json): named-entity author form preserves a developer alias without inventing given/family names.
- [GitHub commit email setting](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address).
- [GitHub noreply format](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference).
