import os
import urllib.request
import numpy as np
from PIL import Image

# 1. Configuration
CATEGORIE = [
    "apple", "banana", "star", "sun", "cloud", 
    "moon", "flower", "tree", "fish", "bird", 
    "butterfly", "car", "cup", "umbrella", "key", 
    "pencil", "clock", "book", "house", "heart"
]
IMAGE_NUMBER = 5000  # How many PNG files you want to create

for CATEGORIY in CATEGORIE:
    # Create the folder for the PNGs
    outputFolder = f"dataset/{CATEGORIY}"
    os.makedirs(outputFolder, exist_ok=True)

    # 2. Download the .npy file directly from Google Cloud Storage
    file_npy = f"{CATEGORIY}.npy"
    url = f"https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{CATEGORIY}.npy"

    if not os.path.exists(file_npy):
        print(f"Downloading for category '{CATEGORIY}'...")
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
        img.save(f"{outputFolder}/{CATEGORIY}_{i+1}.png")

print(f"\nDone|Images have been saved in the folder '{outputFolder}'.")