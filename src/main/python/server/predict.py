import numpy as np
import cv2
import onnxruntime as ort

CATEGORIES = [
    'apple', 'banana', 'bird', 'book', 'butterfly',
    'car', 'clock', 'cloud', 'cup', 'fish',
    'flower', 'heart', 'house', 'key', 'moon',
    'pencil', 'star', 'sun', 'tree', 'umbrella'
]

_session = ort.InferenceSession("src/main/resources/models/model.onnx", providers=["CPUExecutionProvider"])
_input_name = _session.get_inputs()[0].name
_output_name = _session.get_outputs()[0].name


def preprocess_image(image):
    """
    Prende l'immagine decodificata (es. da cv2.imdecode) e la trasforma
    nell'array 28x28x1 pronto per l'inferenza.
    """
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
    kernel = np.ones((10, 10), np.uint8)  # Aumenta a 15 se il tratto scompare ancora
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

    # 🔴 DEBUG: SALVA L'IMMAGINE PER CAPIRE COSA VEDE LA RETE NEURALE
    cv2.imwrite("debug/debug_input.png", image_resized)

    # 7. PREPARA PER IL MODELLO (senza dividere per 255, ci pensa la rete)
    input_data = image_resized.reshape(1, 28, 28, 1).astype(np.float32)
    return input_data


def predict(input_data):
    """
    input_data: array numpy già preprocessato, shape (1, 28, 28, 1), dtype float32.
    """
    result = _session.run([_output_name], {_input_name: input_data})
    prediction = result[0]

    predicted_idx = np.argmax(prediction[0])
    class_name = CATEGORIES[predicted_idx]
    confidence = prediction[0][predicted_idx] * 100

    return class_name, confidence, prediction[0]


def predict_from_image(image):
    """
    Funzione di comodo: prende l'immagine grezza (es. da cv2.imdecode)
    e restituisce direttamente il risultato della predizione.
    """
    input_data = preprocess_image(image)
    return predict(input_data)