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

Run a parameter sweep (manually)
python m0_runner.py --config configs/m0.yaml --override experiments/exp_fast_mode.yaml
python m0_runner.py --config configs/m0.yaml --override experiments/exp_high_quality.yaml

かしこまりました。コピペの手間を省き、ダウンロードしてそのままGitHubにアップロードできるように、指定された各ファイルをコードブロック形式で個別に提供します。

お手数ですが、それぞれのコードブロックの内容をコピーし、指定されたファイル名でローカルに保存してください。

1. ベースフォルダ (m0/ 直下)
README.md
Markdown

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
Run a parameter sweep (manually)
Bash

python m0_runner.py --config configs/m0.yaml --override experiments/exp_fast_mode.yaml
python m0_runner.py --config configs/m0.yaml --override experiments/exp_high_quality.yaml
Google Colab (thin wrapper)
In Colab, install the same pinned requirements and call the CLI
!pip install -r [https://raw.githubusercontent.com/](https://raw.githubusercontent.com/)<your-org>/<repo>/main/requirements.txt
!python m0_runner.py --config configs/m0.yaml --override experiments/exp_baseline.yaml

Files
m0_runner.py – CLI entry. Loads YAMLs, merges timelines, calls renderer.

src/render_core.py – Rendering core (dummy now; replace with your M0 integrated renderer).

src/timeline.py – t_ms-based timeline utilities (merge/align/crossfade hooks).

tests/smoke_m0.py – builds minimal dummy assets and kicks a short run; saves MP4 & logs to tests/out/.

Outputs
MP4: tests/out/<exp_name>/demo.mp4

Log JSON: tests/out/<exp_name>/run.log.json

Summary CSV: tests/out/<exp_name>/summary.csv

Notes for Jules
Ask Jules to fix requirements.txt/Dockerfile until tests/smoke_m0.py passes and open a PR with the changes.

Ask Jules to run a matrix over all YAMLs in experiments/ and attach short MP4s & a comparison table in the PR.


