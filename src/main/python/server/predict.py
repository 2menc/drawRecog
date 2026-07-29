"""
Script per interrogare il modello save_at_5.keras
Uso: python predict.py percorso_immagine.jpg
"""

import sys
import numpy as np
import keras
from keras.utils import load_img, img_to_array

# --- Configurazione ---
MODEL_PATH = "save_at_5.keras"
IMG_SIZE = (224, 224)
# Sostituisci con i nomi reali delle tue 4 classi, nell'ordine
# usato durante l'addestramento (es. quello di ImageDataGenerator
# o keras.utils.image_dataset_from_directory, in ordine alfabetico
# di sottocartelle)
CLASS_NAMES = ["rectangle", "rhombus", "square", "triangle"]


def load_model(model_path=MODEL_PATH):
    return keras.models.load_model(model_path)


def preprocess_image(img_path, target_size=IMG_SIZE):
    img = load_img(img_path, target_size=target_size)
    arr = img_to_array(img)
    arr = np.expand_dims(arr, axis=0)  # shape: (1, 224, 224, 3)
    return arr


def predict(model, img_path):
    x = preprocess_image(img_path)
    preds = model.predict(x, verbose=0)[0]  # array di 4 probabilità (softmax)
    idx = int(np.argmax(preds))
    return CLASS_NAMES[idx], float(preds[idx]), preds


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python predict.py percorso_immagine.jpg")
        sys.exit(1)

    img_path = sys.argv[1]
    model = load_model()
    label, confidence, all_probs = predict(model, img_path)

    print(f"Classe predetta: {label}  (confidenza: {confidence:.2%})")
    print("Probabilità per classe:")
    for name, p in zip(CLASS_NAMES, all_probs):
        print(f"  {name}: {p:.2%}")
