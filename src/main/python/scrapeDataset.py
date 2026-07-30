import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
import numpy as np
from PIL import Image
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = REPO_ROOT / "src/main/resources/datasetScrapeOptions.yaml"

with CONFIG_PATH.open() as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(1)


# 1. Configuration
CATEGORIES = data["categories"]
IMAGE_NUMBER = data["imagesNumber"]  # How many PNG files you want to create

os.makedirs("dataset/npyFiles", exist_ok=True)

for CATEGORY in CATEGORIES:
    # Create the folder for the PNGs
    outputFolder = f"dataset/{CATEGORY}"
    os.makedirs(outputFolder, exist_ok=True)

    last_png = f"{outputFolder}/{CATEGORY}_{IMAGE_NUMBER}.png"
    if os.path.exists(last_png):
        print(
            f"category '{CATEGORY}' already completed ({IMAGE_NUMBER} images). skipping ..."
        )
        continue

    # 2. Download the .npy file directly from Google Cloud Storage
    file_npy = f"dataset/npyFiles/{CATEGORY}.npy"
    url = f"https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{CATEGORY}.npy"

    if not os.path.exists(file_npy):
        print(f"Downloading for category '{CATEGORY}'...")
        try:
            urllib.request.urlretrieve(url, file_npy)
            print("Download completed!")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(
                    f"Error 404: the category '{CATEGORY}' does not exist on QuickDraw, skipping ..."
                )
                continue
            else:
                raise e

    # 3. Extract and save images as PNG
    if os.path.exists(file_npy):
        print(f"Generating PNG images for '{CATEGORY}'...")
        data_npy = np.load(file_npy)

        for i in range(min(IMAGE_NUMBER, len(data_npy))):
            png_path = f"{outputFolder}/{CATEGORY}_{i+1}.png"

            if os.path.exists(png_path):
                continue

            # Restore the 28x28 image matrix
            matrice = data_npy[i].reshape(28, 28)

            # Create and save the PNG file
            img = Image.fromarray(matrice)
            img.save(png_path)

print(f"\nDone! Images have been saved in the folder 'dataset/'.")