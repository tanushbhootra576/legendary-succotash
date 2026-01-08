import os
import sys

# -------------------------------------------------
# 🔑 FORCE project root into Python path
# -------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import cv2
import numpy as np

from src.video.face_crop import extract_face
from src.features.face_split import split_face
from src.models.asymmetry_predictor import FacialAsymmetryPredictor

print("=== test_separation.py STARTED ===")

# -------------------------------------------------
# Setup
# -------------------------------------------------
predictor = FacialAsymmetryPredictor()
CLIPS_DIR = "data/processed/clips"


def score_from_clip(path):
    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print(f"⚠️ Could not read frame: {path}")
        return None

    face = extract_face(frame)
    if face is None:
        print(f"⚠️ No face detected: {path}")
        return None

    left, right = split_face(face)
    return predictor.predict(left, right)


actor1_scores = []
actor2_scores = []

for fname in os.listdir(CLIPS_DIR):
    fpath = os.path.join(CLIPS_DIR, fname)

    if "Actor_01" in fname:
        s = score_from_clip(fpath)
        if s is not None:
            actor1_scores.append(s)

    elif "Actor_02" in fname:
        s = score_from_clip(fpath)
        if s is not None:
            actor2_scores.append(s)


if len(actor1_scores) == 0 or len(actor2_scores) == 0:
    raise RuntimeError("❌ Not enough valid clips for separation test")


a1_mean = np.mean(actor1_scores)
a2_mean = np.mean(actor2_scores)

intra_std = np.std(actor1_scores)
inter_diff = abs(a1_mean - a2_mean)

print("\n=== SEPARATION RESULTS ===")
print(f"Actor 1 clips      : {len(actor1_scores)}")
print(f"Actor 2 clips      : {len(actor2_scores)}")
print(f"Actor 1 mean score : {a1_mean:.4f}")
print(f"Actor 2 mean score : {a2_mean:.4f}")
print(f"Intra-user std     : {intra_std:.4f}")
print(f"Inter-user diff    : {inter_diff:.4f}")

if inter_diff > intra_std:
    print("✅ Separation looks PROMISING")
else:
    print("⚠️ Separation weak (expected for untrained model)")
