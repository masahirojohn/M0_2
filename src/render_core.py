from __future__ import annotations
import json, os
from typing import Dict, Any
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

# Dummy renderer to validate the pipeline end-to-end.
# Replace the draw logic with your M0 integrated renderer later.

def _ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def _text_img(text: str, w: int, h: int) -> np.ndarray:
    # Create a plain image with overlaid text (no external fonts required)
    img = Image.new("RGBA", (w, h), (30, 30, 30, 255))
    d = ImageDraw.Draw(img)
    lines = text.split("\n")
    y = 10
    for line in lines:
        d.text((10, y), line, fill=(240, 240, 240, 255))
        y += 20
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)


def crossfade(a: np.ndarray, b: np.ndarray, alpha: float) -> np.ndarray:
    return (a.astype(np.float32) * (1 - alpha) + b.astype(np.float32) * alpha).astype(np.uint8)


def render_video(
    out_mp4: str,
    width: int,
    height: int,
    fps: int,
    duration_s: int,
    crossfade_frames: int,
    timeline_value_fn,
):
    _ensure_dir(os.path.dirname(out_mp4) or ".")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    vw = cv2.VideoWriter(out_mp4, fourcc, fps, (width, height))

    total_frames = int(duration_s * fps)
    prev_frame = None

    for i in range(total_frames):
        t_ms = int(1000 * i / fps)
        vals: Dict[str, Any] = timeline_value_fn(t_ms)
        mouth = vals.get("mouth", "close")
        yaw = vals.get("yaw", 0)
        emo = vals.get("emo_id", 0)
        blink = vals.get("blink", 0)

        txt = f"t={t_ms}ms\nmouth={mouth}\nyaw={yaw}\nemo={emo}\nblink={blink}"
        frame = _text_img(txt, width, height)

        if crossfade_frames > 0 and prev_frame is not None and i % (fps//2 or 1) == 0:
            # periodic crossfade demo
            for k in range(crossfade_frames):
                alpha = (k + 1) / crossfade_frames
                vw.write(cv2.cvtColor(crossfade(prev_frame, frame, alpha), cv2.COLOR_BGRA2BGR))
            prev_frame = frame
        else:
            vw.write(cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR))
            prev_frame = frame

    vw.release()
