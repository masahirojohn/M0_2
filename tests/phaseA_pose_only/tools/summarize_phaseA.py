import json, csv, sys, pathlib

runlog = json.load(open(sys.argv[1], "r", encoding="utf-8"))
# 例: viewsの切替フレーム/フォールバック率/所要時間を拾う
views = runlog.get("views", {})
fallback_frames = runlog.get("fallback_frames", 0)
total = runlog.get("total_frames", 1)
elapsed = runlog.get("elapsed_s", None)
bucket_miss_rate = fallback_frames / max(1,total)

row = {
  "exp_name": runlog.get("exp_name"),
  "elapsed_s": elapsed,
  "views_front": views.get("front",0),
  "views_left30": views.get("left30",0),
  "views_right30": views.get("right30",0),
  "fallback_frames": fallback_frames,
  "bucket_miss_rate": round(bucket_miss_rate, 3)
}

out_csv = pathlib.Path(sys.argv[2])
with out_csv.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=row.keys())
    w.writeheader()
    w.writerow(row)
print("Wrote:", out_csv)
