from __future__ import annotations
import argparse, os, json
from typing import Dict, Any
import yaml
from src.timeline import Timeline
from src.render_core import render_video


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def deep_update(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            deep_update(base[k], v)
        else:
            base[k] = v
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--override", action="append", default=[])
    args = ap.parse_args()

    cfg = load_yaml(args.config)
    for o in args.override:
        cfg = deep_update(cfg, load_yaml(o))

    assets_dir = cfg["io"]["assets_dir"]
    out_dir = cfg["io"]["out_dir"]
    exp_name = cfg["io"]["exp_name"]

    width = int(cfg["video"]["width"])
    height = int(cfg["video"]["height"])
    fps = int(cfg["video"]["fps"])
    duration_s = int(cfg["video"]["duration_s"])

    crossfade_frames = int(cfg["render"]["crossfade_frames"])  # demo

    # timelines
    mouth_json = os.path.join(assets_dir, cfg["inputs"]["mouth_timeline"])  # [ {t_ms, mouth:"a|i|u|e|o|close"} ]
    pose_json = os.path.join(assets_dir, cfg["inputs"]["pose_timeline"])    # [ {t_ms, yaw:int} ]
    expr_json = os.path.join(assets_dir, cfg["inputs"]["expression_timeline"])  # [ {t_ms, emo_id:int, blink:0|1} ]

    mouth_tl = Timeline.load_json(mouth_json)
    pose_tl = Timeline.load_json(pose_json)
    expr_tl = Timeline.load_json(expr_json)

    def merged_value(t_ms: int) -> Dict[str, Any]:
        m = mouth_tl.value_at(t_ms)
        p = pose_tl.value_at(t_ms)
        e = expr_tl.value_at(t_ms)
        vals = {}
        vals.update(m)
        vals.update(p)
        vals.update(e)
        return vals

    # out paths
    exp_dir = os.path.join(out_dir, exp_name)
    os.makedirs(exp_dir, exist_ok=True)
    out_mp4 = os.path.join(exp_dir, "demo.mp4")

    
    # 旧:
# render_video(out_mp4, width, height, fps, duration_s, crossfade_frames, merged_value)

# 新: atlas 情報を渡す
render_video(
    out_mp4, width, height, fps, duration_s, crossfade_frames, merged_value,
    assets_dir=assets_dir, atlas_json_rel=cfg.get("atlas", {}).get("atlas_json", None)
)


    # save run log & summary
    run_log = {
        "out_mp4": out_mp4,
        "fps": fps,
        "duration_s": duration_s,
        "frames": int(duration_s * fps),
        "assets_dir": assets_dir,
        "exp_name": exp_name,
    }
    with open(os.path.join(exp_dir, "run.log.json"), "w", encoding="utf-8") as f:
        json.dump(run_log, f, ensure_ascii=False, indent=2)

    with open(os.path.join(exp_dir, "summary.csv"), "w", encoding="utf-8") as f:
        f.write("key,value\n")
        for k, v in run_log.items():
            f.write(f"{k},{v}\n")


if __name__ == "__main__":
    main()
