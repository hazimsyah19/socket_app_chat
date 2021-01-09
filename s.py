import socket 
import threading 
from Crypto.Cipher import AES

# FUNCTION for ENCRYPTION
def encrypt(encrypt_data):
    obj = AES.new(b"1122334456789001", AES.MODE_CFB, b"2299225510784791")
    data = obj.encrypt(encrypt_data)
    return data

# FUNCTION for DECRYPTION
def decrypt(decrypt_data):
    obj = AES.new(b"1122334456789001", AES.MODE_CFB, b"2299225510784791")
    data = obj.decrypt(decrypt_data)
    return data

# SERVER address and PORT number, fill in beforehand
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) 

addr = (SERVER, PORT) 
 
sixt = "utf-8"

# LIST of CLIENTS and their NAMES for multithreading
clients, names = [], [] 

# BIND the SERVER and PORT to SOCKET
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(addr)

# FUNCTION for CHATROOM connection
def startChat():

    print("\n [+] CHATROOM SERVER is up and running : " + SERVER) 

    server.listen(5) 

    while True:

        conn, addr =  server.accept() 
        conn.send(encrypt("NAME")) 

        n = conn.recv(2048)
        temp = decrypt(n)
        name = temp.decode()
 
        names.append(name) 
        clients.append(conn) 
          
        print(f" [+] Name :{name}") 
          

        broadcastMessage(f"\n [+] {name} has joined the chat!") 
          
        conn.send(encrypt(' [+] Connection successful! \n'))

        thread = threading.Thread(target = handle, args = (conn, addr)) 
        thread.start() 

        print(f" [+] Active connections : {threading.activeCount()-1}") 

# FUNCTION to hande incoming connection and messages 
def handle(conn, addr): 

    print(f" [+] New connection : {addr}") 
    connected = True

    while connected: 

        msg = conn.recv(1024)
        temp = decrypt(msg)
        message = temp.decode()
        broadcastMessage(message)

    conn.close() 

# FUNCTION to send and display messages to other CLIENTS
def broadcastMessage(message):
    for client in clients:
        msg = encrypt(message)
        client.send(msg)

# FUNCTION call for  CHATROOM server
startChat() 
