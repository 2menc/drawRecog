import numpy as np
import cv2
import tensorflow as tf

# 1. LA LISTA CORRETTA DELLE TUE 20 CATEGORIE (Rigorasamente in ordine alfabetico)
CATEGORIES = [
    'apple', 'banana', 'bird', 'book', 'butterfly', 
    'car', 'clock', 'cloud', 'cup', 'fish', 
    'flower', 'heart', 'house', 'key', 'moon', 
    'pencil', 'star', 'sun', 'tree', 'umbrella'
]

def load_model(model_path):
    # Carica e restituisce il modello Keras
    return tf.keras.models.load_model(model_path)

def predict(model, image_bytes):
    # 2. CONVERTI I BYTE IN IMMAGINE
    # Trasforma i byte ricevuti dal socket in un array NumPy
    nparr = np.frombuffer(image_bytes, np.uint8)
    
    # Decodifica l'array in un'immagine OpenCV (scala di grigi)
    image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        raise ValueError("Impossibile decodificare i byte dell'immagine.")

    # 3. PRE-PROCESSING (Il passaggio fondamentale che mancava!)
    # Supponiamo che il tuo Canvas Java invii tratti neri su sfondo bianco.
    # QuickDraw è allenato su tratti bianchi su sfondo nero. Quindi dobbiamo invertire:
    image = cv2.bitwise_not(image) # Ora lo sfondo è nero (0) e il tratto è bianco (255)

    # Trova i bordi del disegno per rimuovere lo spazio vuoto (Bounding Box)
    coords = cv2.findNonZero(image)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        
        # Aggiungi un piccolo margine per non tagliare il disegno in modo netto
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + padding * 2)
        h = min(image.shape[0] - y, h + padding * 2)
        
        # Ritaglia l'immagine
        image = image[y:y+h, x:x+w]

    # Ora ridimensiona l'immagine tagliata a 28x28 pixel
    image_resized = cv2.resize(image, (28, 28), interpolation=cv2.INTER_AREA)

    # 4. PREPARAZIONE PER IL MODELLO
    # Normalizza i valori dei pixel da 0-255 a 0.0-1.0
    image_normalized = image_resized / 255.0
    
    # Aggiungi le dimensioni per i batch e i canali (1, 28, 28, 1) per Keras
    input_data = image_normalized.reshape(1, 28, 28, 1)

    # 5. PREDIZIONE
    prediction = model.predict(input_data)
    
    # Trova l'indice della classe con la probabilità più alta
    predicted_idx = np.argmax(prediction[0])
    
    # Recupera il nome della classe e la confidenza
    class_name = CATEGORIES[predicted_idx]
    confidence = prediction[0][predicted_idx]
    
    # Ritorna i tre valori richiesti da listener.py
    return class_name, confidence, prediction[0]