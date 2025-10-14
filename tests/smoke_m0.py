"""
Smoke test that auto-creates minimal dummy assets under tests/assets_min/
Then runs the pipeline via m0_runner.py with exp_baseline.
"""
from __future__ import annotations
import os, json, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "tests", "assets_min")
OUT = os.path.join(ROOT, "tests", "out")


def ensure_dummy_assets():
    os.makedirs(ASSETS, exist_ok=True)
    # Dummy atlas.png/json placeholders (renderer dummy doesn't actually read pixels now)
    # We still create tiny files so that future real renderer finds them.
    import numpy as np, cv2, json as pyjson
    atlas_png = os.path.join(ASSETS, "atlas.png")
    img = (255 * np.ones((64, 128, 3), dtype=np.uint8))
    cv2.putText(img, "atlas", (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2, cv2.LINE_AA)
    cv2.imwrite(atlas_png, img)

    atlas_json = os.path.join(ASSETS, "atlas.json")
    pyjson.dump({"front": {"close": [0,0,32,32], "a": [32,0,32,32]}}, open(atlas_json, "w"))

    # Mouth timeline (every 400ms alternate a/i/u/e/o/close)
    mouths = ["a","i","u","e","o","close"]
    mouth_tl = [{"t_ms": i*400, "mouth": mouths[i % len(mouths)]} for i in range(20)]
    json.dump(mouth_tl, open(os.path.join(ASSETS, "mouth_timeline.json"), "w"))

    # Pose timeline (yaw toggles)
    pose_tl = [{"t_ms": i*500, "yaw": (-15 if i%2==0 else 15)} for i in range(16)]
    json.dump(pose_tl, open(os.path.join(ASSETS, "pose_timeline.json"), "w"))

    # Expression timeline (emo/blink)
    expr_tl = [{"t_ms": i*600, "emo_id": (i%4), "blink": (1 if i%5==0 else 0)} for i in range(14)]
    json.dump(expr_tl, open(os.path.join(ASSETS, "expression_timeline.json"), "w"))


def run_baseline():
    cfg = os.path.join(ROOT, "configs", "m0.yaml")
    exp = os.path.join(ROOT, "experiments", "exp_baseline.yaml")
    cmd = [sys.executable, os.path.join(ROOT, "m0_runner.py"), "--config", cfg, "--override", exp]
    print("RUN:", " ".join(cmd))
    subprocess.check_call(cmd)


if __name__ == "__main__":
    ensure_dummy_assets()
    os.makedirs(OUT, exist_ok=True)
    run_baseline()
    print("Smoke OK. See tests/out/exp_baseline/")
