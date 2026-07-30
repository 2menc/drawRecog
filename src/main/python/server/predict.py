import numpy as np
import cv2
import onnxruntime as ort
import modelSettings
import os

# Inizializziamo le variabili globali vuote
CATEGORIES = []
_session = None
_input_name = None
_output_name = None

def load_categories(model_name):
    """
    Carica le categorie da un file txt con lo stesso nome del modello.
    Esempio: per 'model99.onnx', legge 'model99_labels.txt'
    """
    global CATEGORIES
    labels_path = f"src/main/resources/models/{model_name}.classes"
    
    if not os.path.exists(labels_path):
        print(f"⚠️ ATTENZIONE: File labels non trovato ({labels_path}). Uso categorie fallback.")
        CATEGORIES = [f"Class_{i}" for i in range(1000)] # Fallback fittizio
        return

    with open(labels_path, 'r', encoding='utf-8') as f:
        CATEGORIES = [line.strip() for line in f if line.strip()]
    print(f"Caricate {len(CATEGORIES)} categorie per il modello {model_name}.")

def change_model(model_name):
    """
    Cambia dinamicamente il modello ONNX e aggiorna labels e input/output.
    """
    global _session, _input_name, _output_name
    import onnxruntime as ort
    
    print(f"Caricamento nuovo modello: {model_name}.onnx ...")
    model_path = f"src/main/resources/models/{model_name}.onnx"
    
    try:
        _session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        # FONDAMENTALE: aggiornare i nomi di I/O quando si cambia modello
        _input_name = _session.get_inputs()[0].name
        _output_name = _session.get_outputs()[0].name
        
        # Carichiamo le categorie specifiche per questo modello
        load_categories(model_name)
        
        print("Modello e categorie caricati con successo!")
    except Exception as e:
        print(f"Errore critico nel caricamento del modello {model_name}: {e}")

# Inizializzazione al primo avvio
change_model(modelSettings.CHOSEN_MODEL)


def preprocess_image(image):
    # ... [IL TUO CODICE QUI RIMANE IDENTICO, È PERFETTO PER QUICKDRAW] ...
    # Assicurati solo che tutti i tuoi modelli futuri accettino shape 28x28. 
    # Se in futuro usi reti tipo MobileNet, dovrai cambiare il cv2.resize a (224, 224)
    # ...
    
    if image is None:
        raise ValueError("Unable to decode image bytes.")

    if len(image.shape) == 3 and image.shape[2] == 4:
        alpha_channel = image[:, :, 3]
        rgb_channels = image[:, :, :3]
        white_background = np.ones_like(rgb_channels, dtype=np.uint8) * 255
        alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0
        image = rgb_channels * alpha_factor + white_background * (1 - alpha_factor)
        image = image.astype(np.uint8)

    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    gray = cv2.bitwise_not(gray)

    kernel = np.ones((10, 10), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)

    coords = cv2.findNonZero(gray)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        padding = 15
        x, y = max(0, x - padding), max(0, y - padding)
        w = min(gray.shape[1] - x, w + padding * 2)
        h = min(gray.shape[0] - y, h + padding * 2)
        gray = gray[y:y+h, x:x+w]

    image_resized = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)
    cv2.imwrite("debug/debug_input.png", image_resized)

    input_data = image_resized.reshape(1, 28, 28, 1).astype(np.float32)
    return input_data


def predict(input_data):
    """
    input_data: preprocessed numpy array, shape (1, 28, 28, 1), dtype float32.
    """
    result = _session.run([_output_name], {_input_name: input_data})
    prediction = result[0]

    predicted_idx = np.argmax(prediction[0])
    confidence = prediction[0][predicted_idx] * 100

    # DEBUG UTILE: Stampa quante categorie hai e cosa ha predetto la rete
    print(f"[DEBUG] La rete ha predetto l'indice: {predicted_idx}")
    print(f"[DEBUG] La lista CATEGORIES contiene: {len(CATEGORIES)} elementi")

    # CONTROLLO DI SICUREZZA
    if predicted_idx < len(CATEGORIES):
        class_name = CATEGORIES[predicted_idx]
    else:
        # Se l'indice è fuori scala, non crasha ma restituisce un nome generico
        class_name = f"Unknown_Class_{predicted_idx}"
        print(f"⚠️ ATTENZIONE: Il modello ha predetto l'indice {predicted_idx}, ma hai solo {len(CATEGORIES)} categorie in lista!")

    return class_name, confidence, prediction[0]


def predict_from_image(image):
    input_data = preprocess_image(image)
    return predict(input_data)