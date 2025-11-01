# Phase A – Pose Only Test (mouth=close, expression off)

## 0) What this tests
- Pose bucket stability (front / left30 / right30 + optional up15/down15)
- Hysteresis & smoothing effects
- Sprite switch latency
- Bucket miss rate
- *Expression and mouth timelines are disabled in Phase A*

## 1) Prepare
- Put your atlas images as referenced by `assets/atlas.min.json`.
- Replace `timelines/pose_timeline.sample.json` with DLC-exported pose_timeline.json (t_ms,yaw,pitch,roll).
- Edit `configs/phaseA.config.json` thresholds as needed.

## 2) Run
```bash
bash tests/phaseA_pose_only/scripts/run_phaseA.sh
