import sys
import socket
import yaml
import threading

def waitForInterrupt():
    try:
        print("server active on port", serverPort)
    except KeyboardInterrupt:
        print("\nshutting off server...")
    finally:
        connectionSocket.close()
        print("Server down.")

with open("src/main/resources/serverConfig.yaml") as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

serverPort = data["serverPort"]
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = data["serverAddress"], serverPort

serverSocket.bind(serverAddress)

#1: backlog queue: not completed connections
serverSocket.listen(1)


while True:
    print("server listening...")
    connectionSocket, address = serverSocket.accept()
    print("connection accepted from", connectionSocket, address)


    try:
        closeConnectionThread = threading.Thread(target=waitForInterrupt)
        print("ctrl+C to turn off the server")

        ###TODO
        print("TODO")

    except IOError:

        connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n","UTF-8"))
        connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        connectionSocket.close()
