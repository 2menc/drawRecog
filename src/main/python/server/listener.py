import sys
import socket
import yaml
import struct
import predict

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

        ###CODICE MODELLO###
        modelPath = "src/main/resources/save_at_5.keras"
        classNames, floats, preds = predict.predict(modelPath, image_bytes)
        print(preds)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connectionSocket.close()