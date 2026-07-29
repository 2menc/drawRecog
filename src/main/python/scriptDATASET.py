import os
import urllib.request
import numpy as np
from PIL import Image

# 1. Configurazione: inserisci la categoria che vuoi (es: 'cat', 'airplane', 'car', 'apple', 'dog')
CATEGORIE = [
    "apple", "banana", "star", "sun", "cloud", 
    "moon", "flower", "tree", "fish", "bird", 
    "butterfly", "car", "cup", "umbrella", "key", 
    "pencil", "clock", "book", "house", "heart"
]
NUM_IMMAGINI = 5000  # Quanti file PNG vuoi creare

for CATEGORIA in CATEGORIE:
    # Crea la cartella per i PNG
    cartella_output = f"dataset/{CATEGORIA}"
    os.makedirs(cartella_output, exist_ok=True)

    # 2. Scarica il file .npy direttamente da Google Cloud Storage (se non già presente)
    file_npy = f"{CATEGORIA}.npy"
    url = f"https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{CATEGORIA}.npy"

    if not os.path.exists(file_npy):
        print(f"Download in corso per la categoria '{CATEGORIA}'...")
        urllib.request.urlretrieve(url, file_npy)
        print("Download completato!")

    # 3. Estrai e salva le immagini in PNG (griglia 28x28 pixel)
    print(f"Generazione delle prime {NUM_IMMAGINI} immagini PNG...")
    dati = np.load(file_npy)

    for i in range(min(NUM_IMMAGINI, len(dati))):
        # Ripristina la matrice 28x28 dell'immagine
        matrice = dati[i].reshape(28, 28)
        
        # Crea e salva il file PNG
        img = Image.fromarray(matrice)
        img.save(f"{cartella_output}/{CATEGORIA}_{i+1}.png")

print(f"\nFatto! Le immagini sono state salvate nella cartella '{cartella_output}'.")