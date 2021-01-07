import socket
import threading
from Crypto.Cipher import AES

def encrypt(encrypt_data):
    obj = AES.new(b"1122334456789001", AES.MODE_CFB, b"2299225510784791")
    data = obj.encrypt(encrypt_data)
    return data

def decrypt(decrypt_data):
    obj = AES.new(b"1122334456789001", AES.MODE_CFB, b"2299225510784791")
    data = obj.decrypt(decrypt_data)
    return data

PORT = 8888

SERVER = socket.gethostbyname(socket.gethostname())

addr = (SERVER, PORT)

sixt = "utf-16"

clients, names = [], []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(addr)

def startChat():

    print("server is working on " + SERVER)

    server.listen()

    while True:

        conn, addr = server.accept()
        conn.send("NAME".encode(sixt))

        name = conn.recv(1024).decode(sixt)

        names.append(name)
        clients.append(conn)

        print(f"Name is :{name}")

        broadcastMessage(f"{name} has joined the chat!".encode(sixt))

        conn.send('Connection successful!'.encode(sixt))

        thread = threading.Thread(target=handle, args=(conn, addr))
        thread.start()

        print(f"active connections {threading.activeCount()-1}")

def handle(conn, addr):

    print(f"new connection {addr}")
    connected = True

    while connected:

        msg = conn.recv(1024)
        temp = decrypt(message)
        message = temp.decode(sixt)
        broadcastMessage(message)

    conn.close()

def broadcastMessage(message):
    for client in clients:
        msg = encrypt(message)
        client.send(msg)
startChat()
