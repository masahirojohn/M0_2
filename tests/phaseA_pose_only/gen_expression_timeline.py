import json, sys

pose = json.load(open(sys.argv[1], "r", encoding="utf-8"))
timeline = []
for it in pose["timeline"]:
    timeline.append({
        "t_ms": it["t_ms"],
        "emo_id": 0,          # neutral
        "blink": 0,           # 0=開眼, 1=閉眼（PhaseAでは常に開眼）
        "intensity": 0.0
    })
json.dump({"timeline": timeline}, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
