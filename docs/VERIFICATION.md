# Actual verification / 实际验证记录

Date2026-11-07; scientific reference environment:Windows,Python3.12.3,CPU.

| Check | Actual result |
|---|---|
| Fresh isolated environment | Installed pinned deps in new venv; system-site-packages=false |
| Package installation | Editable src-layout installed successfully |
| Dependency integrity | pip check:no broken requirements |
| Data acquisition | Official existing v3ZIP reused through documented --source; ZIP+CSV SHA-256 matched |
| Fresh remote Kaggle ZIP | Not exercised; explicitly not claimed passed |
| Data preprocessing | Full1330816rows/69profiles audited; same40/9/12/8split |
| Full retraining | Both TNN variants10epochs; all5methods×6scenarios evaluated |
| Numeric reproduction |4212non-timing reference values compared; maxabsolute difference0; passed |
| LPTN supplement | Both structures×6scenarios×8profiles rerun; clean5parameter MAE5.7662°C |
| Exports |30aggregate and240profile scalar rows; SVG/PDF/PNG generated |
| Unit/smoke tests |9passed:group isolation,causality,faults,metrics,finite outputs,TNN size,LPTN,HTTP guards |
| Browser |Edge desktop1440×1060and mobile viewport390×844passed; no page errors/overflow |
| Browser interactions |Profile46outage,reveal,5comparison rows,scrub,play/pause,raw/weights/env/git paths404 |
| Original preservation |235original research files matched before/after hashes |
| Stable application |Separate original13hash/90paired-result freeze check passed |
| Third-party code |Extracted TNN class ASTs identical to pinned upstream notebook |

First editable install and Edge launch encountered Windows sandbox permissions;
local verification succeeded with normal host permissions. A server started in
the app container was not reachable from host Edge. Starting the same loopback-only
demo under the browser's host permissions on4383resolved this;browser smoke allows
DEMO_URLoverride. This is an environment limitation, not proof of public hosting.
No firewall setting, stable application, database, or public deployment was changed.

Browser snapshots and logs remain ignored in results/browser to avoid publishing
measured temperature traces. Chromium mobile viewport is not real iPhone/Safari.
Image source QA passed all blocking checks;300dpiPNG/noTIFF are accepted report
previews, not a claim of journal-final600dpiassets. Allmethods/scenarios are shown,
no experimental row removed for aesthetics. Reports contain aggregates only.

Private GitHub creation/push and final staging status are recorded separately
in RELEASE_STATUS.md after remote authorization/verification. They must not be
inferred from successful local tests.

## Pseudonymous release checks (2026-11-07)

All 16 tests pass with optional audit dependencies: the nine existing science/
server tests plus seven privacy regressions. CFF 1.2 validates against the
official tagged schema. A wheel builds for package-author inspection. Metadata,
all reachable history and the full staged tree are checked separately; see
`ANONYMITY_AUDIT.md` and `RELEASE_STATUS.md` for observed publication status.
No scientific model is retrained, data removed or experimental result changed
to accomplish privacy cleanup.
