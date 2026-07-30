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

CATEGORIES = data["categories"]
IMAGE_NUMBER = data["imagesNumber"]

os.makedirs("dataset/npyFiles", exist_ok=True)

for CATEGORY in CATEGORIES:
    outputFolder = f"dataset/{CATEGORY}"
    os.makedirs(outputFolder, exist_ok=True)

    # 1. Se la categoria è già completata, salta subito
    last_png = f"{outputFolder}/{CATEGORY}_{IMAGE_NUMBER}.png"
    if os.path.exists(last_png):
        print(
            f"category '{CATEGORY}' already completed ({IMAGE_NUMBER} images). skipping ..."
        )
        continue

    file_npy = f"dataset/npyFiles/{CATEGORY}.npy"

    category_encoded = urllib.parse.quote(CATEGORY)
    url = f"https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{category_encoded}.npy"

    # 2. Download del file .npy se manca sul disco
    if not os.path.exists(file_npy):
        print(f"Downloading for category '{CATEGORY}'...")
        try:
            urllib.request.urlretrieve(url, file_npy)
            print("Download completed")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(
                    f"Error 404: the category '{CATEGORY}' does not exist on QuickDraw, skipping ..."
                )
                continue
            else:
                raise e

    if os.path.exists(file_npy):
        try:
            data_npy = np.load(file_npy)
        except Exception as e:
            print(
                f"'{file_npy}' is corrupter or incomplete ({e}). deleting and re-downloading ..."
            )
            if os.path.exists(file_npy):
                os.remove(file_npy)
            try:
                urllib.request.urlretrieve(url, file_npy)
                data_npy = np.load(file_npy)
                print("Riscaricato con successo!")
            except Exception as err:
                print(
                    f"ERROR: cannot download correctly '{CATEGORY}': {err}"
                )
                continue

        print(f"Generating PNG images for '{CATEGORY}'...")
        total_target = min(IMAGE_NUMBER, len(data_npy))

        for i in range(total_target):
            png_filename = f"{outputFolder}/{CATEGORY}_{i+1}.png"
            if os.path.exists(png_filename):
                continue

            matrice = data_npy[i].reshape(28, 28)
            img = Image.fromarray(matrice)
            img.save(png_filename)

print("\nDone! Scraping completed successfully.")