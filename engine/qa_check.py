#!/usr/bin/env python3
"""Objective half of the QA gate. usage: qa_check.py videos/<id>.mp4 -> prints JSON, exit 1 if any hard check fails.

The viewer-rubric half (hook, message, appeal, fact accuracy) is scored by the person/agent running the day and
recorded next to this in qa/<id>.json, see QA_RUBRIC.md. These numbers are measurements; the rubric is judgement.
"""
import json, os, re, subprocess, sys
import numpy as np

v = sys.argv[1]
# A cinematic ad (owner, 2026-11-13) is cut short on purpose: 7 shots and the try-it card run ~30 s, Reels-length.
_ep = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "episodes", os.path.basename(v)[:-4] + ".json")
_cine = "--cine" in sys.argv or (os.path.exists(_ep) and json.load(open(_ep)).get("format") == "cine")   # detected, so no caller can forget the flag
LO = 25 if _cine else 35
def sh(*a): return subprocess.run(a, capture_output=True, text=True)
pr = json.loads(sh("ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", v).stdout)
vs = next(s for s in pr["streams"] if s["codec_type"] == "video"); au = next((s for s in pr["streams"] if s["codec_type"] == "audio"), None)
dur = float(pr["format"]["duration"]); fps = eval(vs["avg_frame_rate"]); size_mb = float(pr["format"]["size"]) / 1e6
r = {"duration_s": round(dur, 2), "resolution": f'{vs["width"]}x{vs["height"]}', "fps": round(fps, 2), "size_mb": round(size_mb, 1), "has_audio": au is not None}
loud = sh("ffmpeg", "-nostats", "-i", v, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
m = re.findall(r"I:\s+(-?[\d.]+) LUFS", loud); tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", loud)
r["loudness_lufs"] = float(m[-1]) if m else None; r["true_peak_dbfs"] = float(tp[-1]) if tp else None

# motion / pace: sample 2 fps at small size, count seconds where nothing visibly changes
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", "fps=2,scale=160:90,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(np.float32)
d = np.abs(np.diff(fr, axis=0)).mean((1, 2)); still = d < 0.35; run = best = 0
for s in still: run = run + 1 if s else 0; best = max(best, run)
r["longest_still_s"] = best / 2

# colour: mean saturation and hue spread over sampled frames
rawc = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", "fps=1,scale=96:54", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
c = np.frombuffer(rawc, np.uint8).reshape(-1, 54, 96, 3).astype(np.float32) / 255
mx, mn = c.max(3), c.min(3); sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
r["mean_saturation"] = round(float(sat[mx > 0.15].mean()), 3)
hue_bins = np.histogram(np.arctan2(np.sqrt(3) * (c[..., 1] - c[..., 2]), 2 * c[..., 0] - c[..., 1] - c[..., 2])[sat > 0.3], bins=12, range=(-np.pi, np.pi))[0]
r["hue_bins_used"] = int((hue_bins > hue_bins.sum() * 0.03).sum())

checks = {f"duration {LO}-65s": LO <= dur <= 65, "4K 3840x2160": (vs["width"], vs["height"]) == (3840, 2160), "30 fps": abs(fps - 30) < 0.1,
          "has audio": au is not None, "loudness -20..-12 LUFS": r["loudness_lufs"] is not None and -20 <= r["loudness_lufs"] <= -12,
          "no clipping (peak <= -0.5 dBFS)": r["true_peak_dbfs"] is not None and r["true_peak_dbfs"] <= -0.5,
          "no still stretch > 3 s": best / 2 <= 3, "colourful (saturation >= 0.25, >= 4 hues)": r["mean_saturation"] >= 0.25 and r["hue_bins_used"] >= 4,
          "under 299 MB (vidIQ import limit)": size_mb < 299}
r["checks"] = checks; r["passed"] = all(checks.values())
print(json.dumps(r, indent=1)); sys.exit(0 if r["passed"] else 1)
