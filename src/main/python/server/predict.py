import numpy as np
import cv2
import onnxruntime as ort
import modelSettings

CATEGORIES = [
    'apple', 'banana', 'bird', 'book', 'butterfly',
    'car', 'clock', 'cloud', 'cup', 'fish',
    'flower', 'heart', 'house', 'key', 'moon',
    'pencil', 'star', 'sun', 'tree', 'umbrella'
]

_session = ort.InferenceSession("src/main/resources/models/", modelSettings.CHOSEN_MODEL + "onnx", providers=["CPUExecutionProvider"])
_input_name = _session.get_inputs()[0].name
_output_name = _session.get_outputs()[0].name


def preprocess_image(image):
    """
    Takes the decoded image (e.g., from cv2.imdecode) and transforms it
    into the 28x28x1 array ready for inference.
    """
    if image is None:
        raise ValueError("Unable to decode image bytes.")

    # 2. IF THE IMAGE HAS A TRANSPARENT BACKGROUND, MAKE THE BACKGROUND WHITE
    if len(image.shape) == 3 and image.shape[2] == 4:
        alpha_channel = image[:, :, 3]
        rgb_channels = image[:, :, :3]
        white_background = np.ones_like(rgb_channels, dtype=np.uint8) * 255
        alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0
        image = rgb_channels * alpha_factor + white_background * (1 - alpha_factor)
        image = image.astype(np.uint8)

    # 3. CONVERT TO GRAYSCALE
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Now we surely have a white background with black strokes.
    # INVERT: Black background (0), White stroke (255)
    gray = cv2.bitwise_not(gray)

    # 4. THICKEN THE STROKE (Dilation)
    kernel = np.ones((10, 10), np.uint8)  # Increase to 15 if the stroke disappears again
    gray = cv2.dilate(gray, kernel, iterations=1)

    # 5. CROP BORDERS (Bounding Box)
    coords = cv2.findNonZero(gray)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        padding = 15
        x, y = max(0, x - padding), max(0, y - padding)
        w = min(gray.shape[1] - x, w + padding * 2)
        h = min(gray.shape[0] - y, h + padding * 2)
        gray = gray[y:y+h, x:x+w]

    # 6. 28x28 resize
    image_resized = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)

    # 🔴 DEBUG: SAVE THE IMAGE TO UNDERSTAND WHAT THE NEURAL NETWORK SEES
    cv2.imwrite("debug/debug_input.png", image_resized)

    # 7. PREPARE FOR THE MODEL (without dividing by 255, the network handles it)
    input_data = image_resized.reshape(1, 28, 28, 1).astype(np.float32)
    return input_data


def predict(input_data):
    """
    input_data: preprocessed numpy array, shape (1, 28, 28, 1), dtype float32.
    """
    result = _session.run([_output_name], {_input_name: input_data})
    prediction = result[0]

    predicted_idx = np.argmax(prediction[0])
    class_name = CATEGORIES[predicted_idx]
    confidence = prediction[0][predicted_idx] * 100

    return class_name, confidence, prediction[0]


def predict_from_image(image):
    """
    Convenience function: takes the raw image (e.g., from cv2.imdecode)
    and directly returns the prediction result.
    """
    input_data = preprocess_image(image)
    return predict(input_data)