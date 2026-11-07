# Sources, rights and contributions / 来源与自主贡献

## Data

Electric Motor Temperature v3:Wilhelm Kirchgässner/Paderborn University LEA,
https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature .
CC BY-SA4.0, https://creativecommons.org/licenses/by-sa/4.0/ .
No raw dataset or per-sample derivative is bundled. Aggregate result figures
and scalar tables retain dataset attribution and their own report license.

## Original algorithms and code

- Kirchgässner,Wallscheid,Böcker. *Thermal neural networks:Lumped-parameter
  thermal modeling with state-space machine learning*. Engineering Applications
  of Artificial Intelligence(2023),doi:10.1016/j.engappai.2022.105537.
  https://github.com/wkirgsn/thermal-nn , pinned commit
  531f2275adcbb9ad562dd59cb1c8043630ae0e11 . Two reviewed Python classes are
  bundled under the author's MIT notice. See third_party/PROVENANCE.md.
- *Estimating Electric Motor Temperatures With Deep Residual Machine Learning*
  (2021): https://ieeexplore.ieee.org/document/9296842 .
  https://github.com/upb-lea/deep-pmsm (MIT), reviewed pinned commit
  1f6acc0c690bd3f3c9e645eee5b4577ce612dd2a . Not copied or trained here.
- Ridge regression, causal exponential smoothing, nonnegative least squares
  and lumped thermal networks are established methods, not invented here.
- KTNN,2026: https://ieeexplore.ieee.org/abstract/document/11735260 . This
  repository does not implement or experimentally compare KTNN.

## Software dependencies

NumPy/SciPy/scikit-learn:BSD-family; PyTorch:BSD-style; threadpoolctl:BSD3;
matplotlib:PSF-based matplotlib license; Playwright:Apache2.0. They are installed
as dependencies, not copied into Git. Their packaged notices and upstream
licenses remain applicable; this project does not relicense their source.
Exact validated versions are in requirements.txt and requirements-lock.txt.

## Project-original work

StefanUniverse(StefanUniverse):experiment organization, complete-profile protocol, train-only
preprocessing, fault harness, metrics/calibration diagnostics, ablation harness,
effective one-node comparison, report generation, local interaction and release
audits. Code/text MIT per owner's explicit confirmation; original TNN copyright
remains separate. No adviser is silently added as a software coauthor.

The software's contribution is reproducible reliability/failure-mode analysis
and integration. It does not claim novel foundation algorithms, independently
measured fault data, new FEM measurements, or industrial validation.
