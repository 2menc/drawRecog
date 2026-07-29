import os
# 🔴 FONDAMENTALE: Forza Keras ad usare solo NumPy (niente AVX, compatibile al 100% con il MacBook 2010!)
os.environ["KERAS_BACKEND"] = "numpy"

import numpy as np
import cv2
import keras  # Usiamo direttamente Keras anziché TensorFlow

CATEGORIES = [
    'apple', 'banana', 'bird', 'book', 'butterfly', 
    'car', 'clock', 'cloud', 'cup', 'fish', 
    'flower', 'heart', 'house', 'key', 'moon', 
    'pencil', 'star', 'sun', 'tree', 'umbrella'
]

def load_model(model_path):
    # Carica il modello con Keras 3
    return keras.models.load_model(model_path)

def predict(model, image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    
    if image is None:
        raise ValueError("Impossibile decodificare i byte dell'immagine.")

    # Sfondo trasparente -> Bianco
    if len(image.shape) == 3 and image.shape[2] == 4:
        alpha_channel = image[:, :, 3]
        rgb_channels = image[:, :, :3]
        white_background = np.ones_like(rgb_channels, dtype=np.uint8) * 255
        alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0
        image = rgb_channels * alpha_factor + white_background * (1 - alpha_factor)
        image = image.astype(np.uint8)

    # Grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Inverti colori: sfondo nero, tratto bianco
    gray = cv2.bitwise_not(gray)

    # Ingrossa il tratto
    kernel = np.ones((10, 10), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)

    # Ritaglia bordi vuoti
    coords = cv2.findNonZero(gray)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        padding = 15
        x, y = max(0, x - padding), max(0, y - padding)
        w = min(gray.shape[1] - x, w + padding * 2)
        h = min(gray.shape[0] - y, h + padding * 2)
        gray = gray[y:y+h, x:x+w]

    # Resize a 28x28
    image_resized = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)

    # Salva immagine di debug
    cv2.imwrite("debug_input.png", image_resized)

    # Prepara input
    input_data = image_resized.reshape(1, 28, 28, 1)

    # Predizione con NumPy backend
    prediction = model.predict(input_data, verbose=0)
    
    predicted_idx = np.argmax(prediction[0])
    class_name = CATEGORIES[predicted_idx]
    confidence = prediction[0][predicted_idx] * 100
    
    return class_name, confidence, prediction[0]