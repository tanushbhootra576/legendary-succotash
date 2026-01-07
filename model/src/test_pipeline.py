from src.video.face_crop import extract_face
from src.features.face_split import split_face
from src.models.asymmetry_predictor import FacialAsymmetryPredictor
import cv2

predictor = FacialAsymmetryPredictor()

cap = cv2.VideoCapture("data/processed/clips/01-01-01-01-01-01-01_c0.mp4")
ret, frame = cap.read()
cap.release()

face = extract_face(frame)
left, right = split_face(face)

score = predictor.predict(left, right)
print("Deviation score:", score)
