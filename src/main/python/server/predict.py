import numpy as np
import cv2
import onnxruntime as ort
import modelSettings
import os

CATEGORIES = []
_session = None
_input_name = None
_output_name = None

def load_categories(model_name):
    global CATEGORIES
    labels_path = f"src/main/resources/models/{model_name}_labels.txt"
    
    if not os.path.exists(labels_path):
        print(f"Warning: File {labels_path} not found. Using fallback.")
        CATEGORIES = [f"Class_{i}" for i in range(500)]
        return

    with open(labels_path, 'r', encoding='utf-8') as f:
        CATEGORIES = [line.strip() for line in f if line.strip()]
        
    print(f"Info: Loaded {len(CATEGORIES)} categories from {labels_path}.")

def change_model(model_name):
    global _session, _input_name, _output_name
    
    print(f"\n--- REQUESTED MODEL CHANGE: {model_name} ---")
    model_path = f"src/main/resources/models/{model_name}.onnx"
    
    if not os.path.exists(model_path):
        print(f"Error: File {model_path} does not exist!")
        return
        
    _session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
    _input_name = _session.get_inputs()[0].name
    _output_name = _session.get_outputs()[0].name
    
    output_shape = _session.get_outputs()[0].shape
    print(f"Info: ONNX loaded! Model output shape: {output_shape}")
    
    load_categories(model_name)
    print("------------------------------------------\n")

change_model(modelSettings.CHOSEN_MODEL)

def preprocess_image(image):
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
    result = _session.run([_output_name], {_input_name: input_data})
    prediction = result[0]

    predicted_idx = np.argmax(prediction[0])
    confidence = prediction[0][predicted_idx] * 100

    if predicted_idx < len(CATEGORIES):
        class_name = CATEGORIES[predicted_idx]
    else:
        class_name = f"Unknown_Class_{predicted_idx}"
        print(f"Alert: Model predicted index {predicted_idx}, but only {len(CATEGORIES)} categories loaded!")

    return class_name, confidence, prediction[0]

def predict_from_image(image):
    input_data = preprocess_image(image)
    return predict(input_data)