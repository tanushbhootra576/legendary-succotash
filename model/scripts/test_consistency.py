import os
import sys

# Add the parent directory to sys.path to import src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import cv2
from src.video.face_crop import extract_face
from src.features.face_split import split_face
from src.models.asymmetry_predictor import FacialAsymmetryPredictor

predictor = FacialAsymmetryPredictor()

CLIPS_DIR = "data/raw_videos/depvidmood/"
actor_prefix = "Video_Speech_Actor_01"  # pick one actor

scores = []

for file in os.listdir(CLIPS_DIR):
    if actor_prefix in file:
        cap = cv2.VideoCapture(os.path.join(CLIPS_DIR, file))
        ret, frame = cap.read()
        cap.release()

        face = extract_face(frame)
        if face is None:
            continue

        left, right = split_face(face)
        score = predictor.predict(left, right)
        scores.append(score)

print("Scores:", scores)
print("Mean:", np.mean(scores))
print("Std Dev:", np.std(scores))

# Todo: Add option to save these results to a file
