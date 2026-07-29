import numpy as np
import cv2
import tensorflow as tf

CATEGORIES = [
    'apple', 'banana', 'bird', 'book', 'butterfly', 
    'car', 'clock', 'cloud', 'cup', 'fish', 
    'flower', 'heart', 'house', 'key', 'moon', 
    'pencil', 'star', 'sun', 'tree', 'umbrella'
]

def load_model(model_path):
    return tf.keras.models.load_model(model_path)

def predict(model, image_bytes):
    # 1. Leggi l'immagine, supportando anche il canale Alpha (trasparenza)
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    
    if image is None:
        raise ValueError("Impossibile decodificare i byte dell'immagine.")

    # 2. SE L'IMMAGINE HA UNO SFONDO TRASPARENTE, FATTI BIANCO LO SFONDO
    if len(image.shape) == 3 and image.shape[2] == 4:
        alpha_channel = image[:, :, 3]
        rgb_channels = image[:, :, :3]
        white_background = np.ones_like(rgb_channels, dtype=np.uint8) * 255
        alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0
        image = rgb_channels * alpha_factor + white_background * (1 - alpha_factor)
        image = image.astype(np.uint8)

    # 3. CONVERTI IN SCALA DI GRIGI
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Ora abbiamo di sicuro uno sfondo bianco con tratto nero.
    # INVERTIAMO: Sfondo nero (0), Tratto bianco (255)
    gray = cv2.bitwise_not(gray)

    # 4. INGROSSA IL TRATTO (Dilation)
    # Fondamentale: evita che il disegno scompaia rimpicciolendolo a 28x28!
    kernel = np.ones((10, 10), np.uint8) # Aumenta a 15 se il tratto scompare ancora
    gray = cv2.dilate(gray, kernel, iterations=1)

    # 5. RITAGLIA I BORDI (Bounding Box)
    coords = cv2.findNonZero(gray)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        padding = 15
        x, y = max(0, x - padding), max(0, y - padding)
        w = min(gray.shape[1] - x, w + padding * 2)
        h = min(gray.shape[0] - y, h + padding * 2)
        gray = gray[y:y+h, x:x+w]

    # 6. RESIZE ESATTO A 28x28
    image_resized = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)

    # ==============================================================
    # 🔴 DEBUG: SALVA L'IMMAGINE PER CAPIRE COSA VEDE LA RETE NEURALE
    cv2.imwrite("debug/debug_input.png", image_resized)
    # ==============================================================

    # 7. NORMALIZZA E PREVIDI
# 7. PREPARA PER IL MODELLO (Senza dividere per 255, lo fa già la rete!)
    input_data = image_resized.reshape(1, 28, 28, 1)

    prediction = model.predict(input_data, verbose=0) # verbose=0 toglie le scritte 1/1 ━━━
    
    predicted_idx = np.argmax(prediction[0])
    class_name = CATEGORIES[predicted_idx]
    
    # Moltiplichiamo per 100 per avere una percentuale leggibile (es: 98.5%)
    confidence = prediction[0][predicted_idx] * 100
    
    return class_name, confidence, prediction[0]