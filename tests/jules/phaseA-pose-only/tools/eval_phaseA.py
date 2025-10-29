#!/usr/bin/env python
import argparse, json, csv, statistics, os, glob

def load_conf(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def expected_bucket(yaw, pitch, conf):
    yawc = conf["pose_buckets"]["yaw_deg"]
    pc   = conf["pose_buckets"]["pitch_deg"]

    # yaw優先（front/±30）
    if yaw >= yawc["right30_min"]:
        b = "right30"
    elif yaw <= yawc["left30_min"]:
        b = "left30"
    elif abs(yaw) <= yawc["front_max_abs"]:
        b = "front"
    else:
        b = "front"  # 安全側

    # pitch補助（enable時）
    if pc.get("enable", True):
        if pitch >= pc["up15_min"]:
            b = "up15"
        elif pitch <= pc["down15_max"]:
            b = "down15"
    return b

def read_frame_csv(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, "r", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        for r in rd:
            try:
                r["yaw_deg"] = float(r["yaw_deg"])
                r["pitch_deg"] = float(r["pitch_deg"])
                r["roll_deg"] = float(r["roll_deg"])
                r["t_ms"] = int(float(r["t_ms"]))
                r["latency_ms"] = float(r["latency_ms"]) if r["latency_ms"] else None
                rows.append(r)
            except Exception:
                continue
    return rows

def read_run_log_json(out_dir, basename):
    p = os.path.join(out_dir, f"{basename}.log.json")
    if not os.path.exists(p):
        # 既存の命名に寄せて run.log.json を探す
        cand = os.path.join(out_dir, "run.log.json")
        if os.path.exists(cand):
            p = cand
        else:
            return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def read_summary_csv(out_dir):
    p = os.path.join(out_dir, "summary.csv")
    if not os.path.exists(p):
        # 予防: *.summary.csv などがあれば拾う
        cands = glob.glob(os.path.join(out_dir, "*summary*.csv"))
        if cands:
            p = cands[0]
        else:
            return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            # 1行サマリー想定
            for r in rd:
                return r
    except Exception:
        pass
    return {}

def p_stats(arr):
    if not arr:
        return {"count": 0, "mean": None, "median": None, "p90": None, "max": None}
    arr_sorted = sorted(arr)
    n = len(arr_sorted)
    p90_idx = max(0, min(n - 1, int(0.9 * n) - 1))
    return {
        "count": n,
        "mean": statistics.mean(arr_sorted),
        "median": statistics.median(arr_sorted),
        "p90": arr_sorted[p90_idx],
        "max": arr_sorted[-1]
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    conf = load_conf(args.config)
    out_dir = args.outdir or conf["output"]["dir"]
    basename = conf["output"]["basename"]
    frame_csv = os.path.join(out_dir, "frame_events.csv")

    rows = read_frame_csv(frame_csv)

    # bucket_miss_rate
    mismatches = 0
    total = 0
    latencies = []
    for r in rows:
        exp_b = expected_bucket(r["yaw_deg"], r["pitch_deg"], conf)
        sel_b = r.get("bucket_selected") or ""
        total += 1
        if exp_b != sel_b:
            mismatches += 1
        if r["latency_ms"] is not None:
            latencies.append(r["latency_ms"])

    miss_rate = (mismatches / total) if total else None
    lat_summary = p_stats(latencies)

    fb = {}
    J = read_run_log_json(out_dir, basename)
    if J:
        for k in ["fb_by_blur", "fb_by_ssim", "fb_both", "SSIM_THR_suggestion"]:
            if k in J:
                fb[k] = J[k]

    summ_csv = read_summary_csv(out_dir)
    if summ_csv:
        fb["summary_csv"] = summ_csv

    report = {
        "bucket_miss_rate": miss_rate,
        "sprite_switch_latency_ms": lat_summary,
        "fallback_metrics": fb,
        "n_frames_logged": total,
        "out_dir": out_dir
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

