"""
Script per interrogare il modello save_at_5.keras
Uso: python predict.py percorso_immagine.jpg [percorso_modello.keras]
"""

import io
import sys
from pathlib import Path

import numpy as np
import keras
from keras.utils import img_to_array, load_img

# --- Configurazione ---
REPO_ROOT = Path(__file__).resolve().parents[4]
MODEL_PATH = REPO_ROOT / "src/main/resources/save_at_5.keras"
IMG_SIZE = (224, 224)
CLASS_NAMES = ["rectangle", "rhombus", "square", "triangle"]


def resolve_path(path):
    if path is None:
        return MODEL_PATH

    path = Path(path)
    if not path.is_absolute():
        return (REPO_ROOT / path).resolve()
    return path


def load_model(model_path=None):
    model_path = resolve_path(model_path)
    return keras.models.load_model(model_path)


def preprocess_image(image_source, target_size=IMG_SIZE):
    if isinstance(image_source, (bytes, bytearray)):
        img = load_img(io.BytesIO(image_source), target_size=target_size)
    else:
        img = load_img(resolve_path(image_source), target_size=target_size)

    arr = img_to_array(img)
    arr = np.expand_dims(arr, axis=0)  # shape: (1, 224, 224, 3)
    return arr


def predict(model_or_path, image_source):
    if isinstance(model_or_path, (str, Path)):
        model = load_model(model_or_path)
    else:
        model = model_or_path

    x = preprocess_image(image_source)
    preds = model.predict(x, verbose=0)[0]  # array di 4 probabilità (softmax)
    idx = int(np.argmax(preds))
    return CLASS_NAMES[idx], float(preds[idx]), preds


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python predict.py percorso_immagine.jpg [percorso_modello.keras]")
        sys.exit(1)

    img_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) >= 3 else None
    model = load_model(model_path)
    label, confidence, all_probs = predict(model, img_path)

    print(f"Classe predetta: {label}  (confidenza: {confidence:.2%})")
    print("Probabilità per classe:")
    for name, p in zip(CLASS_NAMES, all_probs):
        print(f"  {name}: {p:.2%}")
