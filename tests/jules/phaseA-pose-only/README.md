# Phase A – Pose Only Test (mouth=close, expression off)

## What this tests
- Pose bucket stability (front / left30 / right30 + up15/down15)
- Hysteresis & smoothing effects
- Sprite switch latency
- Bucket miss rate
- Expression/mouth timelines are disabled in Phase A

## Prepare
1. Put images:
   - tests/phaseA_pose_only/assets/front/mouth_close.png
   - tests/phaseA_pose_only/assets/left30/mouth_close.png
   - tests/phaseA_pose_only/assets/right30/mouth_close.png
   - tests/phaseA_pose_only/assets/up15/mouth_close.png
   - tests/phaseA_pose_only/assets/down15/mouth_close.png
2. Replace `timelines/pose_timeline.sample.json` with your DLC-exported pose_timeline.json
   (t_ms, yaw, pitch, roll).
3. Edit thresholds in `configs/phaseA.config.json` if needed.

## Run
```bash
bash tests/phaseA_pose_only/scripts/run_phaseA.sh
