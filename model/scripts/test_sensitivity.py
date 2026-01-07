import cv2
import numpy as np
from src.video.face_crop import extract_face
from src.features.face_split import split_face
from src.models.asymmetry_predictor import FacialAsymmetryPredictor

predictor = FacialAsymmetryPredictor()

cap = cv2.VideoCapture("data/processed/clips/.mp4")
ret, frame = cap.read()
cap.release()

face = extract_face(frame)
left, right = split_face(face)

# Original
base_score = predictor.predict(left, right)

# Artificial asymmetry: shift right face
shifted = np.roll(right, shift=15, axis=1)
shifted_score = predictor.predict(left, shifted)

print("Original score:", base_score)
print("Shifted score:", shifted_score)

#Todo: Add more systematic sensitivity 
