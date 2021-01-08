import socket
import tkinter
from threading import Thread
from Crypto.Cipher import AES

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            message = decrypt(msg)
            msg_list.insert(tkinter.END,message)
        except OSError:
            break

def send(event=None):
    """Handle sending of messages"""
    msg = my_msg.get()
    message = encrypt(msg)
    my_msg.set("")
    client.send(bytes(msg,"utf-16"))
    if msg =="{quit}":
        client.close()
        top.quit()

def on_closing(event=None):
    my_msg.set("{quit}")
    send()

def encrypt(encrypt_data):
    obj = AES.new(b"1122334456789001", AES.MODE_CFB, b"2299225510784791")
    data = obj.encrypt(encrypt_data)
    return data

def decrypt(decrypt_data):
    obj = AES.new(b"1122334456789001", AES.MODE_CFB, b"2299225510784791")
    data = obj.decrypt(decrypt_data)
    return data


top = tkinter.Tk()
top.title("Group Chat")
top.geometry("500x400")
top.resizable(0,0)
message_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type your message here")
scrollbar = tkinter.Scrollbar(message_frame)
msg_list = tkinter.Listbox(message_frame, height=15 , width=65, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
msg_list.pack(side = tkinter.RIGHT, fill=tkinter.BOTH)
msg_list.pack()
message_frame.pack()

entry_field = tkinter.Entry(top,width=40,textvariable=my_msg)
entry_field.bind("<Return>",send)
entry_field.pack(side=tkinter.LEFT)
send_button = tkinter.Button(top,text = "Send", command = send , height=7,width=5)
send_button.pack(side=tkinter.RIGHT)

top.protocol("WM_DELETE_WINDOW", on_closing)


host = input("Enter host : ")
port = input("Enter port : ")
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
if not port:
    port = 8888
else:
    port = int(port)

try:
    client.connect((host,port))
except socket.error as e:
    print(str(e))

receive_thread = Thread(target=receive)
receive_thread.start()

tkinter.mainloop()
