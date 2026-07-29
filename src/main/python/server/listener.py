import sys
import socket
import yaml
import threading
import struct

MAX_BYTES = 20000

with open("src/main/resources/serverConfig.yaml") as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

serverPort = int(data["serverPort"])
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = "localhost", serverPort

serverSocket.bind(serverAddress)

#1: backlog queue: not completed connections
serverSocket.listen(1)


while True:
    print("server listening...")
    connectionSocket, address = serverSocket.accept()
    print("connection accepted from", connectionSocket, address)

    try:
        size_data = connectionSocket.recv(4)
        if not size_data or len(size_data) < 4:
            print("Errore: impossibile leggere la dimensione dell'immagine.")
            connectionSocket.close()
            continue

        image_size = struct.unpack('>i', size_data)[0]
        print(f"Dimensione immagine in arrivo: {image_size} byte")

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

        if len(image_bytes) == image_size:
            with open("delete.png", "wb") as f:
                f.write(image_bytes)
            print("Immagine salvata con successo come 'delete.png'\n")
        else:
            print("Errore: i byte ricevuti non corrispondono alla dimensione attesa.\n")

    except Exception as e:
        print(f"Si è verificato un errore: {e}")

    finally:
        connectionSocket.close()