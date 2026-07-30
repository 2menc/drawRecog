import socket
import struct
import sys
import traceback
from pathlib import Path
import cv2
import numpy as np
import yaml
import predict

REPO_ROOT = Path(__file__).resolve().parents[4]
CONFIG_PATH = REPO_ROOT / "src/main/resources/serverConfig.yaml"

with CONFIG_PATH.open() as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(1)

serverPort = int(data["serverPort"])
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverAddress = "0.0.0.0", serverPort
serverSocket.bind(serverAddress)
serverSocket.listen(5)

print(f"server open on port: {serverPort}...")

while True:
    print("server listening...")
    connectionSocket = None
    try:
        connectionSocket, address = serverSocket.accept()
        
        size_data = connectionSocket.recv(4)
        if not size_data or len(size_data) < 4:
            continue

        image_size = struct.unpack(">i", size_data)[0]
        if image_size <= 0:
            continue

        chunks = []
        bytes_received = 0
        while bytes_received < image_size:
            bytes_to_read = min(image_size - bytes_received, 4096)
            chunk = connectionSocket.recv(bytes_to_read)
            if not chunk:
                break
            chunks.append(chunk)
            bytes_received += len(chunk)

        image_bytes = b"".join(chunks)
        if not image_bytes:
            continue

        # CHANGE MODEL COMMAND CHECK
        if image_bytes.startswith(b"MODEL:"):
            comando = image_bytes.decode("utf-8", errors="ignore")
            nome_modello = comando.replace("MODEL:", "").strip()
            print(f"--> [model change requested from java application] to model: {nome_modello}")
            
            predict.change_model(nome_modello) #changes the model
            
            response = nome_modello

        #IMAGE
        else:
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

            # Esegui la predizione
            className, confidence, probabilities = predict.predict_from_image(image)
            
            print("-------")
            print(f"{className} with {confidence:.2f}% confidence")
            print("-------")
            
            response = f"{className}:{confidence:.2f}"

        # Invia la risposta finale a Java
        response_bytes = response.encode("utf-8")
        connectionSocket.sendall(struct.pack(">i", len(response_bytes)))
        connectionSocket.sendall(response_bytes)

    except Exception as e:
        print(f"Errore durante l'elaborazione: {e}")
        traceback.print_exc()

    finally:
        if connectionSocket:
            try:
                connectionSocket.close()
            except Exception:
                pass