# 呼び出し側で: from adapters.m0_logging_patch import PhaseALogger

import csv, os, time

class PhaseALogger:
    def __init__(self, out_dir, enable=True):
        self.enable = enable
        self.path = os.path.join(out_dir, "frame_events.csv")
        if self.enable:
            os.makedirs(out_dir, exist_ok=True)
            with open(self.path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["t_ms","yaw_deg","pitch_deg","roll_deg",
                            "bucket_expected","bucket_selected",
                            "selected_at_ms","expected_from_ms","latency_ms"])

    def write(self, t_ms, yaw, pitch, roll,
              bucket_expected, bucket_selected,
              selected_at_ms, expected_from_ms):
        if not self.enable: return
        latency = max(0, selected_at_ms - expected_from_ms) if selected_at_ms and expected_from_ms else ""
        with open(self.path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                t_ms, yaw, pitch, roll,
                bucket_expected, bucket_selected,
                selected_at_ms, expected_from_ms, latency
            ])
# This file is a placeholder for any logging patches that may be needed.
