#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
CONF="${ROOT_DIR}/tests/phaseA_pose_only/configs/phaseA.config.json"

echo "[PhaseA] Using config: $CONF"

# sanity check
python - <<'PY' "$CONF"
import json,sys
conf=json.load(open(sys.argv[1]))
assert "atlas_path" in conf and "timelines" in conf
print("[PhaseA] Config ok. Pose:", conf["timelines"]["pose"])
PY

# === Runner呼び出し（M0_2仕様） ===
python m0_runner.py --config "$CONF"

OUT_DIR=$(python - <<'PY' "$CONF"
import json,sys
conf=json.load(open(sys.argv[1]))
print(conf["output"]["dir"])
PY
)
echo "[PhaseA] Outputs under: $OUT_DIR"
ls -la "$OUT_DIR" || true
