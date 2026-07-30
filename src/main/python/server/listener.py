import socket
import struct
import sys
from pathlib import Path

import numpy as np
import cv2
import yaml

import predict

MAX_BYTES = 20000
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
serverAddress = "0.0.0.0", serverPort

serverSocket.bind(serverAddress)

# 1: backlog queue: not completed connections
serverSocket.listen(1)

while True:
    print("server listening...")
    connectionSocket, address = serverSocket.accept()
    print("connection accepted from", connectionSocket, address)

    try:
        size_data = connectionSocket.recv(4)
        if not size_data or len(size_data) < 4:
            print("Errore: cannot read image dimension.")
            connectionSocket.close()
            continue

        image_size = struct.unpack('>i', size_data)[0]
        print(f"image dim: {image_size} byte")

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

        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

        className, confidence, probabilities = predict.predict_from_image(image)
        print("-------")
        print(f"{className} with {confidence}% confidence")
        print("-------")

        response = f"{className}:{confidence:.2f}"
        response_bytes = response.encode("utf-8")
        connectionSocket.sendall(struct.pack('>i', len(response_bytes)))
        connectionSocket.sendall(response_bytes)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connectionSocket.close()