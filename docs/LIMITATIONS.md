# Known limitations / 已知限制

- Research prototype, not an industrial product, protection function, certified
  temperature limit checker, real-time controller or thermal derating system.
- One motor/dataset. All abnormal sensor measurements are synthetic injections.
  No real hardware failure trial or cross-motor transfer validation.
- Ten-second stride replay is not original2Hz fidelity, MCU execution, desktop
  worst-case latency, or field deployment. No interpolation restores discarded
  temporal detail.
- One split seed and short10epoch TNN budget. Validation learning still improves;
  no claim to reproduce or beat the author's complete TNN/KTNN paper scores.
- Test profiles have been examined repeatedly in exploratory development. No new
  preregistered external blind benchmark is claimed.
- Unknown hot initialization remains serious. No target-label initialization or
  discarded warm-up hides the error. No validated new initial-state estimator.
- Physical-looking proxies are not measured losses. Neither absolute thermal
  R/C identification nor same-motor loss-and-temperature validation is available.
- Only i_q and one stress magnitude are tested. Reconstruction assumes the
  missing mask is known; it cannot detect a plausible but biased sensor.
- Empirical residual intervals use only12calibration profiles and correlated
  samples. Width/coverage trade-offs, undercoverage under bias, and profile46
  failure remain. No universal calibrated probability or guaranteed safety bound.
- Browser reveal/hide is visual only; local replay already contains labels.
  Server is loopback-only, not hardened for internet publication.
- Fresh remote Kaggle retrieval can require authentication or fail transiently.
  The local official-ZIP/hash path is fully testable; the verification report
  distinguishes it from an actual fresh network download.
- Bundled results are frozen aggregates; regenerating exact CPU timings across
  hardware is not expected. All unsuccessful cases remain in reports.
- Public repository conversion is not authorized yet, even though the owner
  approved MIT for original code. The final visibility gate is independent.

## Subsequent research, not completed features

Prioritize unknown hot-start state uncertainty/rejection; separately examine
sensor fault and operating-domain shift; broaden channel/severity and seeds;
train an adequate author baseline; pre-register an untouched external evaluation;
then examine whether any reliability mechanism offers narrow useful intervals
or meaningful abstention under hardware-confirmed failures. Do not add a larger
network merely to claim novelty.
