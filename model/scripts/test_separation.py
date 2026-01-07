import os
import numpy as np
import cv2
from src.video.face_crop import extract_face
from src.features.face_split import split_face
from src.models.asymmetry_predictor import FacialAsymmetryPredictor

predictor = FacialAsymmetryPredictor()
CLIPS_DIR = "data/processed/clips"

def score_from_clip(path):
    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    cap.release()
    face = extract_face(frame)
    if face is None:
        return None
    left, right = split_face(face)
    return predictor.predict(left, right)

actor1 = []
actor2 = []

for file in os.listdir(CLIPS_DIR):
    if "Actor_01" in file:
        s = score_from_clip(os.path.join(CLIPS_DIR, file))
        if s: actor1.append(s)
    if "Actor_02" in file:
        s = score_from_clip(os.path.join(CLIPS_DIR, file))
        if s: actor2.append(s)

print("Actor 1 mean:", np.mean(actor1))
print("Actor 2 mean:", np.mean(actor2))
print("Intra-user std:", np.std(actor1))
print("Inter-user diff:", abs(np.mean(actor1) - np.mean(actor2)))
