# M0 Integrated Renderer – Jules/Colab Ready Skeleton

## What is this?
- Single entry CLI `m0_runner.py` to run the M0 pipeline both on local/Jules VM and Google Colab.
- Config-first design: default `configs/m0.yaml` + experiment overrides under `experiments/`.
- A tiny smoke test `tests/smoke_m0.py` that **auto-generates dummy assets** so the pipeline runs without any external files.

## Quickstart (Local / Jules VM)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
# baseline
python m0_runner.py --config configs/m0.yaml --override experiments/exp_baseline.yaml
# outputs in tests/out/exp_baseline/
