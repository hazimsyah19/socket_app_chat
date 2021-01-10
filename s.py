import socket 
import threading 
from Crypto.Cipher import AES
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

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
clients ,names = [] ,[]

# BIND the SERVER and PORT to SOCKET
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(addr)

# FUNCTION for CHATROOM connection
def startChat():

    clear()

    print("\n [+] CHATROOM SERVER is up and running : " + SERVER) 

    print("\n [+] CHATROOM SERVER is waiting for connection... ")
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

        thread = threading.Thread(target = handle, args = (conn, addr,name)) 
        thread.start() 

        print(f" [+] Active connections : {threading.activeCount()-1}") 

# FUNCTION to hande incoming connection and messages 

def handle(conn, addr , name): 


    print(f" [+] New connection : {addr}") 
    connected = True

    while connected: 
        
        msg = conn.recv(1024)
        temp = decrypt(msg)
        message = temp.decode()
        #print(len(message))
        g = message[message.index(" ") + 1:]
        if g != '!bye':
            broadcastMessage(message)
        else:
            broadcastMessage('%s left the chat' % name)
            conn.close()
            server.close()
            break

# FUNCTION to send and display messages to other CLIENTS
def broadcastMessage(message):
    for client in clients:
        msg = encrypt(message)
        client.send(msg)
# FUNCTION call for  CHATROOM server
startChat() 
