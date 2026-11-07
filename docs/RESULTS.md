# Results / 全部结果与失败案例

The reviewed frozen scalar report includes all five methods×six scenarios×eight
test profiles, not only favourable cases. CSV files are scalar aggregates, not
raw measurements. Fresh-run comparison is in reports/reproduction.json.

## Clean data, point-weighted °C

| Method | MAE | RMSE | MaxAE | Equal-profile MAE | 90%coverage / interval width |
|---|---:|---:|---:|---:|---:|
| Ridge raw+history |3.37|5.31|52.98|5.96|96.0% /18.66°C|
| Ridge proxies+history |2.75|5.25|57.35|6.34|97.2% /16.73°C|
| TNN author cell |7.88|10.00|29.02|10.21|93.8% /35.46°C|
| TNN signed |8.51|10.09|26.60|10.16|93.4% /38.32°C|
| TNN reconstruction |7.88|10.00|29.02|10.21|93.8% /35.46°C|

These are local10epoch CPU-budget results, not the author's paper results.
Point-weighted and equal-profile MAE differ substantially, so both are kept.

## Fault degradation and calibration failure

Heat-proxy Ridge improves clean MAE3.37→2.75°C but worsens sustained outage
3.65→7.38°C and constant bias3.73→7.47°C relative to raw-feature Ridge.
Its clean90%empirical band covers only75.2%under outage and67.6%under bias.
Using physically motivated regressors does not guarantee fault robustness.

TNN reconstruction changes outage whole-profile MAE only8.0567→8.0401°C,
but the active outage-window MAE worsens about6.00→6.34°C. Missing-specific
interval calibration does not produce useful demonstrated gain. No-hidden-fault
detector exists; clean/bias/drift/noise reconstruction point outputs equal TNN.
The signed ablation is worse in clean MAE but better under bias/drift and some
high-temperature metrics, so nonnegativity is not uniformly beneficial here.

Sample-wise empirical interval error across50/80/90/95%levels is not a validated
probability for arbitrary domain shift. Calibration profile-max bands can
cover8/8whole test profiles while being extremely wide; that is not compelling
precision or a safety guarantee. See all widths and coverage levels in JSON.

## Unknown hot start and other failures

Profile46 has109evaluated points and starts hot while the boundary-only initial
estimate is much colder. The TNN profile MAE≈23.74°C; heat-proxy Ridge≈31.49°C.
Reconstructed TNN under outage covers0/109points with its nominal90%band.
No warm-up exclusion or measured test-target initialization removes this case.
Its small sample count makes point-weighted averages hide a severe failure.

Profile23 also shows a large TNN transient mismatch, with MaxAE≈29.02°C.
Thermal structure alone does not give a safe upper bound.

Supplementary effective one-node baseline:clean MAE5.7662,RMSE7.6289,
MaxAE24.0832°C (I²+speed), versus I²-only MAE7.0629°C. It remains worse
than Ridge in average clean error and has serious unknown-initial-state errors.
It identifies ratios, not measured absolute thermal R/C. No universal win is claimed.

No original negative result, failed scenario, short profile, or ablation is
deleted. This is evidence for targeted future research, not evidence of an
industrial-ready or novel universally robust estimator.
