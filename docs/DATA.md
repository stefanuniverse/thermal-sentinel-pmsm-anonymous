# Data / 数据与获取

Source: https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature

Wilhelm Kirchgässner / Paderborn University LEA, Electric Motor Temperature,
version3, published update2021-04-26, CC BY-SA4.0. Cite the dataset page and
the2021 deep-residual temperature-estimation paper linked in SOURCES.md.

| Item | Reference identity |
|---|---|
| ZIP bytes | 122212134 |
| ZIP SHA-256 | 10e49e6220fa3c8a9d22c8bab8280ffe2d5e1e3380a6a18bcfc64ea2e8b56b92 |
| Sole CSV | measures_v2.csv,300061411bytes |
| CSV SHA-256 | 78f3d150f0f2ad9c5dc7ff24dd12c00d386ad530f48c1589ad24fcd88867d3ad |
| Native rows/columns/profiles | 1330816 /13 /69 |
| Native sampling | 0.5s (2Hz), from data documentation |

The downloader pins datasetVersionNumber=3 and refuses mismatching hashes.
`--source` is an equally documented acquisition path for an existing official
ZIP or a browser download under the user's own Kaggle account. No account
password/token is requested by this repository, embedded in URLs, or stored in
code. Do not weaken the checksum guard if Kaggle changes packaging; audit the
new release as a distinct dataset identity.

| Columns | Meaning / unit | Use |
|---|---|---|
| i_d,i_q | dq currents,A | inference inputs |
| u_d,u_q | dq voltages,V | inference inputs; production availability not assumed |
| motor_speed | rpm | inference input |
| ambient,coolant | °C | measured boundary inputs |
| pm | PM temperature,°C | training/evaluation target only |
| stator_yoke,stator_tooth,stator_winding | °C | TNN training labels only |
| torque | N·m,bench measurement | excluded from model inputs |
| profile_id | unitless group identifier | split/index only |

v3 values are de-anonymized physical-unit values, not ready-standardized
z-scores. The original audit found no nonfinite values or duplicate complete
rows/blocks. Tails and jumps are retained; source lacks labels to distinguish
true transients from acquisition anomalies. The timestamp is reconstructed from
row order, so missed acquisition frames cannot be independently excluded.

No raw ZIP/CSV, derived per-sample replay, learned weights, third-party research
PDF/CAD or unrelated motor datasets are pushed. Reports expose only aggregate
scalar metrics and figures, with attribution and CC BY-SA4.0 notice. Code MIT
does not change dataset rights. CREATOR, GalFer, and induction-motor data from
separate audits are not included or combined with this PMSM.
