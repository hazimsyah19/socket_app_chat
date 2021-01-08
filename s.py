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

PORT = 5050
 
SERVER = "192.168.42.152" #socket.gethostbyname(socket.gethostname()) 
  
addr = (SERVER, PORT) 
 
sixt = "utf-8"
  
clients, names = [], [] 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
server.bind(addr) 
 
def startChat(): 
    
    print("server is working on " + SERVER) 
        
    server.listen(5) 
      
    while True: 
        
        conn, addr =  server.accept() 
        conn.send(encrypt("NAME")) 

        n = conn.recv(2048)
        temp = decrypt(n)
        name = temp.decode()
 
        names.append(name) 
        clients.append(conn) 
          
        print(f"Name is :{name}") 
          

        broadcastMessage(f"{name} has joined the chat!") 
          
        conn.send(encrypt('Connection successful!'))

        thread = threading.Thread(target = handle, args = (conn, addr)) 
        thread.start() 
 
        print(f"active connections {threading.activeCount()-1}") 
  
def handle(conn, addr): 
    
    print(f"new connection {addr}") 
    connected = True
      
    while connected: 

        msg = conn.recv(1024) 
        temp = decrypt(msg)
        message = temp.decode()  
        broadcastMessage(message) 
       
    conn.close() 
 
def broadcastMessage(message): 
    for client in clients:
        msg = encrypt(message)
        client.send(msg)  
startChat() 
