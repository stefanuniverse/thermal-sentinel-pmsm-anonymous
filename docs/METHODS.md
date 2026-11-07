# Methods / 实验方法

## Fixed complete-profile protocol

Original recordings contain 69 contiguous profile blocks. The four disjoint
groups in `configs/split.json` were established before stride sampling or
causal feature generation. Train:40 / validation:9 / calibration:12 / test:8.
Seed260711; test profiles23,46,52,58,60,62,73,74. Native row counts respectively
842122 / 144268 / 212592 / 131834. Evaluated test rows after independent
stride20 sampling:6596. No test warm-up deletion.

Each profile is restarted independently. Time is row order ×0.5s; the source
CSV has no explicit timestamps. Stride20 keeps real rows at 10s intervals,
without interpolation. Therefore the CPU replay is not a 2Hz online experiment.
All preprocessing parameters are fitted only on train groups. Full-data EDA
statistics do not enter model fitting. Validation selects a TNN checkpoint;
calibration only selects interval widths. Inherited test profiles have already
been inspected in exploratory development and are not a newly preregistered blind set.

## Inputs, features, initialization

Seven inference inputs:ambient,coolant,u_d,u_q,motor_speed,i_d,i_q. Torque and
profile_id are excluded. PM and three stator temperatures are training/evaluation
labels only. A TNN may use its own predicted thermal state, never measured test
target temperature. Initial four-state estimate = mean of first ambient and
coolant. This is deliberately not an oracle warm start.

Ridge_raw:7 raw signals plus60/600/1800s causal EWMAs,28 features+intercept.
Ridge_proxies:11 signals with the same histories,44 features+intercept. The
four additional signals are |speed|, i_d²+i_q², |u_d i_d+u_q i_q|, u_d²+u_q².
They are predictive proxies, not measured copper/iron/PM losses in W. Ridge
alpha30; StandardScaler statistics only from train features.

## TNN and ablations

Author's pinned MIT TNNCell/DiffEqLayer:4 thermal states,506 parameters. CPU,
one Torch thread, Adam0.004, ten epochs,128-step truncated BPTT, gradient
norm clipping1.0, explicit Euler step10s. Electrical input scale is train
max-absolute; temperature scale200 is a fixed declared constant. Current and
voltage magnitudes are formed from scaled dq signals exactly as in this local
reference harness. Validation PM MAE selects the best epoch.

Signed ablation keeps topology, capacitance and solver but removes nonnegative
conductance/heat parameterization. It changes the conductance activation too;
not a perfect single-factor causal ablation. This is not a full upstream
100-epoch protocol or a KTNN reproduction.

Reconstruction:freeze the same TNN weights; fit quadratic Ridge(alpha10) on
train only to reconstruct i_q from the other six measured inputs. Apply only
at known missing positions. Baseline missing values use causal forward-fill,
with train median for missing start values. No detector for concealed bias/drift.
Reconstruction adds28 coefficients; its missing-specific calibration uses
calibration-profile random-missing/outage residuals only.

## Sensor stress tests

Every perturbation is synthetic, applied only to i_q on each complete held-out
profile; all other inputs and ground truth stay unchanged. Per-profile RNG is
seed260711+profile_id. Train i_q SD≈88.70A.

| Condition | Injection |
|---|---|
| clean | none |
| random_missing | independently mark20% positions missing |
| outage | middle third missing |
| bias | final two-thirds add one train SD |
| drift | final two-thirds ramp0→one train SD |
| noise | zero-mean Gaussian, SD0.25 train SD, all positions |

Missing sensor data and unseen operating conditions are separate factors:
even the clean column is already out-of-training-profile. These tests do not
establish fault prevalence or all-channel/all-severity robustness.

## Metrics and calibration

MAE=mean|y−p|; RMSE=sqrt(mean((y−p)²)); MaxAE=max|y−p|. Point-weighted
aggregate and equal-profile macro-MAE are both retained. Fault-window and
measured PM≥80°C subsets are also retained. 80°C is descriptive, not a material
or certified safety limit. All five methods×six conditions×eight test profiles
remain in the scalar report, including failures.

Intervals use calibration absolute-residual empirical quantiles at50/80/90/95%,
with NumPy `method="higher"`. Mean absolute coverage error compares those
four nominal and observed levels. Samples are temporally dependent; this is
not a distribution-free guarantee under a new operating regime or sensor drift.
A profile-max conservative band is separately reported and can be unusably wide.

CPU latency is profile total preprocessing/inference time divided by samples,
then median over profiles. It is neither worst-case per-frame latency nor
embedded/industrial hard-real-time proof.

## Supplementary effective LPTN

One nonnegative node is fitted to training target derivatives with boundary
temperature terms and current/speed heat proxies; exact zero-order-hold rollout
starts only from measured boundary temperatures. Models I² and I²+speed have3
and5 effective ratios. Without measured heat power and an absolute parameter
anchor, simultaneously scaling C,G and heat coefficients leaves temperature
unchanged. Fitted ratios are not physical R in K/W or C in J/K. This supplement
is independent of any other motor's loss, geometry or FEM data.
