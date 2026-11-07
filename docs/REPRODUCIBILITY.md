# Reproduction / 复现与验证

1. Python3.12.3 fresh venv, `include-system-site-packages=false`.
2. `pip install -r requirements.txt`; exact resolved transitive versions in
   requirements-lock.txt. `pip check` must pass.
3. `pip install --no-deps --no-build-isolation -e .`.
4. Acquire official v3 via `python -m thermal_sentinel.acquire --download`,
   or `--source /path/to/official-v3.zip`. Both hashes are enforced.
5. `python -m thermal_sentinel.data` audits and confirms the complete split.
6. `python -m thermal_sentinel.experiment --stride 20 --epochs 10`.
7. `python scripts/verify_results.py` compares every non-timing reference scalar
   with rtol/atol1e-5. Do not silently replace the reference on failure.
8. Export all scalar rows and plots via modules in root README; run
   `python -m thermal_sentinel.lptn` for the independent effective-node supplement.
9. `python -m unittest discover -s tests -v` needs no raw data for its unit fixtures;
   real-data train/evaluate commands above are the integration verification.
10. Run `python -m thermal_sentinel.demo --port 4382`.

## Browser verification

Optional Node tools are not required for scientific computation. Install the
fixed Playwright dependency with `pnpm install --frozen-lockfile`, then use an
installed Edge browser: `node scripts/browser_smoke.mjs`. Set BROWSER_CHANNEL
to `chrome` if using installed Chrome. Chromium viewport simulation is not
physical-iPhone/Safari testing. The script exercises390×844and1440×1060,
profile selection, outage, reveal, all five rows, play/pause, no horizontal
overflow, browser errors, and denial of raw data/weights/secret paths.

Screenshots and complete temporal replay remain under ignored results/. The
Git repository ships aggregate plots, not temperature-sequence screenshots.

## What was actually exercised

The private release preparation used a new venv, installed fixed scientific
dependencies, and reused the already acquired **official hash-verified ZIP**
through the documented --source path. It did not re-download the122MBdata
through a fresh Kaggle network transfer. Thus authentication/network behaviour
of that optional --download path is not asserted fully validated.

Both TNN variants were trained from scratch for10epochs in the new environment;
no old model weights or other project's Python site-packages were loaded.
All five models and all six scenarios were regenerated. Refer to actual
reports/reproduction.json and docs/VERIFICATION.md for the final pass/fail data.

CPU timing differs with hardware/load. Do not demand identical timing or
mistake this10-second replay for native2Hzor embedded deployment verification.
