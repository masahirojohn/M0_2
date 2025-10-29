#!/usr/bin/env python
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration_ms", type=int, required=True)
    ap.add_argument("--emo_seq", default="0,1,2,3,4")  # comma: emo_id sequence
    ap.add_argument("--emo_step_ms", type=int, default=2000)
    ap.add_argument("--blink_interval_ms", type=int, default=5000)
    ap.add_argument("--blink_dur_ms", type=int, default=150)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    seq = [int(x) for x in args.emo_seq.split(",") if x.strip()!=""]
    t = 0
    events = []
    sidx = 0
    next_blink = args.blink_interval_ms

    while t <= args.duration_ms:
        emo = seq[sidx % len(seq)]
        events.append({"t_ms": t, "emo_id": emo, "blink": 0})
        if t >= next_blink:
            events.append({"t_ms": t, "emo_id": emo, "blink": 1})
            events.append({"t_ms": t+args.blink_dur_ms, "emo_id": emo, "blink": 0})
            next_blink += args.blink_interval_ms
        t += args.emo_step_ms
        sidx += 1

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

