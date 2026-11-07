# Final public publication report / 正式公开发布报告

## Publication record

- **Repository:** https://github.com/stefanuniverse/thermal-sentinel-pmsm-anonymous
- **Publication date:** 2026-11-07, Asia/Shanghai.
- **Visibility:** **Public**, verified by authenticated GitHub CLI and independent unauthenticated HTTP/API requests.
- **Version:** 0.1.0; public research prototype, not an industrial product.
- **Author/maintainer:** StefanUniverse, developer pseudonym.
- **Default/only branch:** `codex/anonymous-release`; no tags.
- **HEAD at visibility conversion:** `0db0154e46fd745e52bfc4977aaebf53f9260916`.
- **Scientific code audited:** `c65f7314be28cb3c44f36c5bd5a0a6680f350b3a`.
- **Latest documentation commit:** see the [default branch history](https://github.com/stefanuniverse/thermal-sentinel-pmsm-anonymous/commits/codex/anonymous-release). This report's own commit hash is provided in the delivery receipt rather than a circular self-referencing hash inside the file.

The owner explicitly replied “确认公开” after reviewing the final audit outcome.
The target was rechecked as Private with the expected account, admin permission,
single branch and no tags. Previously blocked report commits were synchronized
using an ordinary fast-forward push. All 60 remote file blob hashes matched the
audited local tree before conversion.

Only the exact target was converted through GitHub CLI with the explicit
visibility-consequence acknowledgement. No old repository, Universe or MotorVerse
code/configuration was modified. No force push, history rebuild, GitHub Release,
PyPI publication or service deployment was performed.

## Anonymous-access verification

The checks below were actually run after Public visibility was confirmed. HTTP
requests supplied no Authorization or Cookie headers. Git clone disabled
credential helpers, interactive authentication, extra headers, cookie files and
global/system Git configuration; it used the public HTTPS URL.

| Check | Actual result |
|---|---|
| Repository API without authentication | Public; exact owner/name and expected HEAD |
| GitHub page | HTTP 200; README rendered in the page |
| README API | HTTP 200; correct project content |
| LICENSE page/API | HTTP 200; full own MIT text and scope statements present |
| Source ZIP | HTTP 200; all 60 initial-publication file blob hashes matched local Git |
| Full anonymous clone | Succeeded; checked-out HEAD matched local and remote |
| Commit history | All four initial-publication commits present, approved pseudonymous Author/Committer identities |
| Branch/tag inventory | Exactly one branch and zero tags; no accidental refs |

The final report/status documentation is added by a subsequent ordinary
pseudonymous commit and checked again after its push. Counts above describe the
60-file tree at the exact visibility-conversion point, not an unrecorded later
scientific version. The final checkout/download also verifies the added report.

Network failures during the earlier report push and one TLS-reset episode during
anonymous verification were resolved with normal retries. Certificate checks
were never disabled, and no alternate account or repository was used.

## Privacy and rights

The pre-publication recheck covered the full staged tree and all reachable
history, including both report commits added after the scientific audit. It
found no known private-name variants, unexpected emails, personal paths,
credentials or prohibited raw artifacts. The exact account-confirmed noreply
email and StefanUniverse name are used for Author and Committer.

PDF/image/SVG and built-wheel metadata checks passed. No Office document,
Notebook output, original research PDF, raw dataset, pretrained model weight,
CAD or commercial engineering project was uploaded. Local private-name rules,
environments, downloaded data, replay sequences and weights remain ignored.

- **Project-original code/text:** MIT, owner-authorized pseudonym attribution.
- **Original TNN classes:** upstream MIT notice and original author credit retained in `third_party/LICENSE-TNN` and pinned provenance.
- **Paderborn data:** separately CC BY-SA 4.0; original data are not bundled.
- **Aggregate report assets:** separate CC BY-SA 4.0 notice, source attribution and analysis-change description in `reports/LICENSE`.

**License-display WARN:** GitHub's automatic license API currently reports
`NOASSERTION`, while the LICENSE page displays the reviewed MIT text plus its
scope statement. This classifier result is not silently replaced with a claim
that GitHub detected MIT. Project/third-party/report licensing remains explicitly
documented; no declaration or third-party attribution was rewritten for a badge.

Pseudonymous Git metadata is not proof that an account is untraceable. External
links, previous clones, avatars, unknown aliases and any applicable institutional
requirements remain owner-review concerns. The separate old backup must not be
made public or merged into this history.

## Actual test and reproducibility record

The same-day [final pre-publication audit](FINAL_PUBLIC_RELEASE_AUDIT.md) ran in a
new Python 3.12.3 environment using the audited snapshot, not old weights or an
unverified historical “passed” statement:

- README dependency installation, editable installation and `pip check` passed.
- **16/16 tests passed, zero skipped**, including profile isolation, causal
  features/imputation, metrics, TNN model execution, LPTN and identity regressions.
- Official local v3 ZIP acquisition verified both ZIP and CSV SHA-256; preprocessing
  confirmed **1,330,816 rows / 69 profiles**, split 40/9/12/8.
- Both TNN variants trained from scratch for ten epochs; all five methods and six
  conditions evaluated. **4212 non-timing reference values matched exactly,
  maximum absolute difference 0**.
- All 30 method/condition rows and 240 profile rows matched the frozen CSV values.
  Both LPTN structures and SVG/PDF/PNG export ran successfully.
- CFF 1.2 schema and 18-member wheel privacy/Author checks passed.
- Headless Edge 1440×1060 and 390×844 interaction tests passed with no page errors
  or horizontal overflow; reveal, five comparison rows, seek, play/pause and
  denial of raw-data/weight/environment/Git URLs were exercised.

Public conversion did not change scientific code, raw data or frozen results.
The final documentation-only commit does not claim a new model-training run.

## Known limitations

- One motor, one dataset, one seed and a short TNN training budget; no cross-motor
  generalization, native 2 Hz real-time validation, hardware deployment or PM
  protection-control certification is claimed.
- Test profiles were used in exploratory analysis; no new preregistered blind
  benchmark is asserted. Negative sensor-outage/bias, interval and hot-start
  results remain visible.
- Ten-second replay and synthetic i_q faults do not establish industrial fault
  prevalence or all-channel robustness. Intervals are empirical diagnostics, not
  universally calibrated safety bounds. Absolute physical R/C is not identified.
- The demo is the existing local Python HTTP/HTML application, **not Streamlit**.
  The loopback server is not hardened as an internet production service.
- Fresh remote Kaggle ZIP transfer, real iPhone/Safari, other operating systems,
  full dependency-advisory audit and industrial validation were not falsely
  labelled passed. The supported local official-ZIP acquisition path was tested.
- LF/CRLF notebook-byte hashes differ as explained in the final audit; the pinned
  two-class AST and upstream MIT notice independently matched.

## Follow-up research, not current capabilities

Prioritize independent preregistered profiles, more seeds and fault severities,
an adequately trained original baseline, unknown-hot-start uncertainty/rejection
and hardware-measured failure tests. Then assess cross-motor transfer separately.
Retain negative outcomes and avoid increasing model size merely for novelty.

This publication makes a reproducible research prototype available; it does not
turn existing methods into novel foundation algorithms or validated industrial
protection software.
