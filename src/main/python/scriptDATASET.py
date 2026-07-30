import os
import urllib.request
import numpy as np
from PIL import Image
import yaml
import sys


REPO_ROOT = Path(__file__).resolve().parents[4]
CONFIG_PATH = REPO_ROOT / "src/main/resources/serverConfig.yaml"

with CONFIG_PATH.open() as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(1)


# 1. Configuration
CATEGORIES = [
    "apple", "banana", "star", "sun", "cloud", 
    "moon", "flower", "tree", "fish", "bird", 
    "butterfly", "car", "cup", "umbrella", "key", 
    "pencil", "clock", "book", "house", "heart",
    "airplane", "ant", "anvil", "axe", "backpack",
    "basket", "bat", "bear", "bed", "bee",
    "bicycle", "brain", "bread", "bridge", "bucket",
    "bus", "bush", "cactus", "cake", "calculator",
    "calendar", "camel", "camera", "candle", "cannon",
    "carrot", "cat", "chair", "circle", "compass",
    "computer", "cookie", "cow", "crab", "crocodile",
    "crown", "diamond", "dog", "dolphin", "donut",
    "door", "dragon", "drums", "duck", "ear",
    "elephant", "envelope", "eye", "face", "fan",
    "feather", "fence", "flashlight", "foot", "fork",
    "frog", "giraffe", "glasses", "grapes", "guitar",
    "hammer", "hand", "hat", "helicopter", "horse",
    "hospital", "jacket", "knife", "laptop", "leaf",
    "leg", "lion", "monkey", "mountain", "mouse",
    "mouth", "mushroom", "nose", "octopus", "piano"
]
IMAGE_NUMBER = 5000  # How many PNG files you want to create

os.makedirs("dataset/npyFiles", exist_ok=True)

for CATEGORY in CATEGORIES:
    # Create the folder for the PNGs
    outputFolder = f"dataset/{CATEGORY}"
    os.makedirs(outputFolder, exist_ok=True)

    # 2. Download the .npy file directly from Google Cloud Storage
    file_npy = f"dataset/npyFiles/{CATEGORY}.npy"
    url = f"https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{CATEGORY}.npy"

    if not os.path.exists(file_npy):
        print(f"Downloading for category '{CATEGORY}'...")
        urllib.request.urlretrieve(url, file_npy)
        print("Download completed!")

    # 3. Extract and save images as PNG (28x28 pixel grid)
    print(f"Generating the first {IMAGE_NUMBER} PNG images...")
    data = np.load(file_npy)

    for i in range(min(IMAGE_NUMBER, len(data))):
        # Restore the 28x28 image matrix
        matrice = data[i].reshape(28, 28)
        
        # Create and save the PNG file
        img = Image.fromarray(matrice)
        img.save(f"{outputFolder}/{CATEGORY}_{i+1}.png")

print(f"\nDone|Images have been saved in the folder '{outputFolder}'.")