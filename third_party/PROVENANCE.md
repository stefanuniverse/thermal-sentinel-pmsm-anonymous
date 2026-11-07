# Third-party code provenance

The two classes in `src/thermal_sentinel/third_party/thermal_nn_cell.py` were
extracted from `TNN_pytorch.ipynb` at:

- Repository: https://github.com/wkirgsn/thermal-nn
- Commit: `531f2275adcbb9ad562dd59cb1c8043630ae0e11`
- Notebook SHA-256: `1ac66752b066394c821eda6ecad6c163e984df10b959760fe646fef2050aa329`
- License: MIT, copyright (c) 2021 Wilhelm Kirchgässner; full notice: `LICENSE-TNN`.

`DiffEqLayer` and `TNNCell` class bodies are unchanged. Imports and the reviewed
CPU/column-name context previously supplied by the experiment harness are now
explicit module constants. No other notebook cells, data preprocessing,
training loop, MATLAB code, notebook outputs, or Git history are bundled.
The project harness overrides sample_time to 10 s and uses its own split,
train-only scaling, no-target initialization, checkpoint selection and stress
tests. These modifications are not the upstream paper's full protocol.

The deep-pmsm project (MIT) was reviewed as literature/code provenance but is
not bundled or executed. References to it do not claim a deep-residual-model
reproduction. External raw datasets, research PDFs and vendor CAD files from
other audit work are not included in this repository.
