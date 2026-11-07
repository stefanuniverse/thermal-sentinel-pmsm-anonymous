# Engineering and rights audit / 工程审查

## Original project inventory (read-only)

The existing independent research tree contains dataset.py, experiment.py,
tnn.py, serve.py, index.html, protocol tests and smoke.mjs; data/audit/results/
literature documents; locally downloaded Kaggle v3 and public-source metadata;
five-method full results plus Ridge-only results; two trained TorchScript
weights; local temporal replay; local screenshots; and separate open-data
audits/one-node LPTN experiments. Runtime used Python3.12.3, NumPy1.26.4,
SciPy1.13.1, sklearn1.5.2, threadpoolctl3.8.0, matplotlib3.9.4, torch2.7.1+cpu.
The old requirements omitted Torch/plotting and depended on external/local
site-packages; the old TNN loaded reviewed classes dynamically from a notebook.

The new publication tree is separate. There is no old Git history, copied
application deployment configuration, authentication/database client, personal
journal/chat/memory record, external data archive, research PDF, CAD, or old
model weight. Only reviewed scientific source and aggregate evidence are retained.
235 original non-cache/non-environment files were fingerprinted for preservation
checking; the private fingerprint file remains outside the upload set.

## Changes made in publication copy only

- Installable src-layout package; project-root-relative local data/results.
- Exact main dependencies plus resolved clean-environment lock.
- Original TNN class ASTs verified identical to pinned notebook; imports/context
  made explicit. No runtime exec of external notebook cells.
- Official-v3 acquisition and ZIP/CSV SHA-256 guard.
- Local-only allowlisted demo endpoint; raw data, keys and weights denied.
- Reproducibility comparator, CSV/plot export, tests, source/license documentation.
- All30scenario rows and240profile rows preserved. Individual measured
  extrema/sample positions are stripped from the published scalar reference;
  local experiments retain their complete outputs.

## Rights decision

The project owner explicitly confirmed authority to publish project-original
code and selected MIT on2026-11-07. The owner subsequently authorized the developer
pseudonym StefanUniverse for original-code attribution. It does not assert a legal
identity or institutional affiliation. Advisers are not automatically claimed as coauthors.

Bundled TNN classes remain Wilhelm Kirchgässner copyright2021/MIT. The
upstream notebook's unrelated cells, MATLAB subdirectory and Git history are
excluded. deep-pmsm is cited only, not bundled or run. Raw data stay separately
CC BY-SA4.0; aggregate report assets have an explicit CC BY-SA4.0 notice.

No publication decision is made for separate CREATOR/GalFer/other-motor material;
none of that raw material or vendor code is imported into this repository.

## Security audit scope

Allowlisted publication source/config/docs and scalar reports are inspected.
Token/PEM/JWT/credential-URL/personal-path patterns, disallowed extensions and
file sizes are checked without printing matched secret values. New Git staging
is checked again before push. Raw-data/environment/cache/tool directories are
ignored and excluded, not merely hidden by an informal convention.

No exposed credential has been identified within the inspected source and
candidate set. That is not a proof about old histories or unrelated projects;
no old history is copied. If a historical token is independently discovered,
revoke/rotate it at its issuer first, inspect access logs and then sanitize
history/artifacts; deleting one visible file alone would not invalidate it.

The current GitHub identity must match the user's own stefanuniverse account
before repository creation/push. CLI device authorization is independent of
the already connected GitHub read connector. Never transfer passwords, cookies
or tokens into source, commits or documentation. Initial repository visibility
must be Private; public conversion remains a separate final user decision.
