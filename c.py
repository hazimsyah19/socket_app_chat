import socket
import threading 
from tkinter import *
from tkinter import font 
from tkinter import ttk
from PIL import ImageTk, Image 
from Crypto.Cipher import AES

# SERVER address and PORT number, fill in beforehand
PORT = 5050
SERVER = "192.168.42.152"
ADDRESS = (SERVER, PORT) 
sixt = "utf-8"
  
# CLIENT socket created and connection initiated
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect(ADDRESS) 

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

# CLASS for CHATROOM GUI
class GUI:

    def __init__(self):

        # CHATROOM hidden until LOG IN is completed
        self.root = Tk()
        self.root.withdraw()

        # Display LOG IN
        self.login = Toplevel()
        # TITLE for the LOG IN display
        self.login.title("LOG IN")
        self.login.resizable(width = 0, height = 0)
        self.login.configure(width = 400, height = 600, bg = "black")

        # LABEL for entering CHATROOM by sending NAME to the server
        image0 = Image.open("/home/khai/Desktop/socket_app_chat/161026056787944340.png")
        image1 = image0.resize((200,200), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image1)
        self.canvas = Label(self.login, width = 200, height = 200,image = self.img, bg = "black")
        self.canvas.image = self.img
        self.canvas.place(x =100, y = 10)

        self.labelLogin = Label(self.login, text = "To join the chat room,\n enter your name", 
                       justify = CENTER, font = "courier 14 bold", fg = "green", bg = "black") 
        self.labelLogin.place(relheight = 0.3, relx = 0.20, rely = 0.30) 

        self.labelName = Label(self.login, text = " NAME : ", font = "courier 14", fg = "green", bg = "black") 
        self.labelName.place(relheight = 0.09, relx = 0.1, rely = 0.6) 

        # ENTRY for NAME
        self.entryName = Entry(self.login, font = "courier 14", bg = "grey") 
        self.entryName.place(relwidth = 0.5, relheight = 0.09, relx = 0.38, rely = 0.6) 
        self.entryName.focus() 

        # BUTTON to send NAME to the server
        self.sendName = Button(self.login, text = "ENTER", font = "courier 14 bold",
                         command = lambda: self.goAhead(self.entryName.get()))

        self.sendName.place(relx = 0.4, rely = 0.8)

        self.root.mainloop()

    def goAhead(self, name): 
        self.login.destroy() 
        self.layout(name) 

        # THREAD to receive messages
        rcv = threading.Thread(target=self.receive) 
        rcv.start() 

    # FUNCTION for CHATBOX
    def layout(self,name): 

        self.name = name

        # Display CHATBOX 
        self.root.deiconify() 
        self.root.title("CHATROOM") 
        self.root.resizable(width = 0, height = 0) 
        self.root.configure(width = 470, height = 550, bg = "black")

        self.labelTop = Label(self.root, bg = "black", fg = "green", 
                              text = "\n" + self.name , font = "courier 15 bold", pady = 3)

        self.labelTop.place(relwidth = 1)

        self.line = Label(self.root, width = 450, bg = "green")

        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)

        self.textCons = Text(self.root, width = 20, height = 2, bg = "black", 
                             fg = "green", font = "courier 12", padx = 5, pady = 3)

        self.textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08) 

        self.labelBottom = Label(self.root, bg = "#2f3133", height = 79) 

        self.labelBottom.place(relwidth = 1, rely = 0.825)

	# ENTRY for message
        self.entryMsg = Entry(self.labelBottom, bg = "grey", fg = "black", font = "courier 13")
        self.entryMsg.place(relwidth = 0.74, relheight = 0.05, rely = 0.0075, relx = 0.011)
        self.entryMsg.focus()

        # BUTTON for sending message
        self.buttonMsg = Button(self.labelBottom, text = "SEND", font = "courier 10 bold",  
                                width = 20, bg = "green", fg = "black", 
                                command = lambda : self.sendButton(self.entryMsg.get())) 

        self.buttonMsg.place(relx = 0.77, rely = 0.0097, relheight = 0.04, relwidth = 0.22)

        self.textCons.config(cursor = "arrow") 

        # SCROLL BAR for CHATBOX
        scrollbar = Scrollbar(self.textCons, bg = "green") 
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.config(command = self.textCons.yview) 

        self.textCons.config(state = DISABLED) 

    # FUNCTION to create thread to send message to the server 
    def sendButton(self, msg): 
        self.textCons.config(state = DISABLED) 
        self.msg=msg 
        self.entryMsg.delete(0, END) 
        snd= threading.Thread(target = self.sendMessage) 
        snd.start() 

    # FUNCTION to receive messages from the server
    def receive(self): 
        while True: 
            try: 
                msg = client.recv(2048)
                temp = decrypt(msg)
                message = temp.decode()
                # If the messages from the server is NAME then send the client's name 
                if message == 'NAME': 
                    client.send(encrypt(self.name)) 
                else: 
                    # INSERT messages into CHATBOX
                    self.textCons.config(state = NORMAL) 
                    self.textCons.insert(END, message+"\n") 
                    self.textCons.config(state = DISABLED) 
                    self.textCons.see(END) 
            except: 
                # PRINT error on the terminal
                print("An error occured!") 
                client.close() 
                break

    # FUNCTION for sending message to the server
    def sendMessage(self):
        self.textCons.config(state=DISABLED) 
        while True: 
            msg = (f"{self.name}: {self.msg}") 
            message = encrypt(msg)
            client.send(message)
            break

# CLASS for CHATROOM GUI created
chatGUI = GUI() 
