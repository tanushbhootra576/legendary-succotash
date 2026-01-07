import os
import sys

# Add the parent directory to sys.path to import src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.model import build_facial_asymmetry_model

os.makedirs("models", exist_ok=True)

model = build_facial_asymmetry_model()
model.save("models/facial_asymmetry.keras")

print("Model saved to models/facial_asymmetry.keras")
