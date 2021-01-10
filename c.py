import socket
import threading 
from tkinter import *
from tkinter import font 
from tkinter import ttk
from PIL import ImageTk, Image 
from Crypto.Cipher import AES

# SERVER address and PORT number, fill in beforehand
PORT = 5050
SERVER = "192.168.0.117"
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
        self.login.title("    LOG IN")
        self.login.resizable(width = 0, height = 0)
        self.login.configure(width = 300, height = 400, bg = "#1A1A1A")

	# CHATROOM APP LOGO, set the logo's directory beforehand
        image0 = Image.open("/home/iman//CHAT/socket_app_chat/161026056787944340.png")
        image1 = image0.resize((120,120), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image1)
        self.canvas = Label(self.login, width = 120, height = 120,image = self.img, bg = "#1A1A1A")
        self.canvas.image = self.img
        self.canvas.place(x = 80, y = 10)

	# LABEL for entering CHATROOM by sending NAME to the server
        self.labelLogin = Label(self.login, text = "To join the chat room,\n enter your name", 
                       justify = CENTER, font = "Verdana 14 bold", fg = "#F8F8F8", bg = "#1A1A1A") 
        self.labelLogin.place(relheight = 0.3, relx = 0.1, rely = 0.28) 

        self.labelName = Label(self.login, text = " NAME  ", font = "Verdana 14 bold", fg = "#F8F8F8", bg = "#FBAD34") 
        self.labelName.place(relheight = 0.1, relx = 0.1, rely = 0.55) 

        # ENTRY for NAME
        self.entryName = Entry(self.login, font = "Verdana 14", bg = "#F8F8F8") 
        self.entryName.place(relwidth = 0.5, relheight = 0.1, relx = 0.38, rely = 0.55) 
        self.entryName.focus() 

        # BUTTON to send NAME to the server
        self.sendName = Button(self.login, text = "JOIN", font = "Verdana 15 bold", fg = "#F8F8F8", bg = "#FBAD34" ,
                         command = lambda: self.enterCHAT(self.entryName.get()))
        self.sendName.place(relwidth = 0.5, relheight = 0.15, relx = 0.25, rely = 0.75)

	# LOOP for ROOT
        self.root.mainloop()

    # FUNCTION to enter CHATBOX and create thread to receive messages
    def enterCHAT(self, name): 
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
        self.root.configure(width = 470, height = 530, bg = "#1A1A1A")

        self.labelTop = Label(self.root, bg = "#1A1A1A", fg = "#F8F8F8", 
                              text = self.name , font = "Verdana 12 bold", pady = 3)
        self.labelTop.place(relwidth = 1, rely = 0.01)

        self.line = Label(self.root, width = 450, bg = "#FBAD34")
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)

        self.textCons = Text(self.root, width = 20, height = 2, bg = "#1A1A1A", 
                             fg = "#FBAD34", font = "Verdana 12", padx = 5, pady = 3)
        self.textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08) 

        self.labelBottom = Label(self.root, bg = "#4E4E4E", height = 75) 
        self.labelBottom.place(relwidth = 1, rely = 0.825)

	# ENTRY for message
        self.entryMsg = Entry(self.labelBottom, bg = "#F8F8F8", fg = "#1A1A1A", font = "Verdana 13")
        self.entryMsg.place(relwidth = 0.74, relheight = 0.05, rely = 0.0075, relx = 0.011)
        self.entryMsg.focus()

        # BUTTON for sending message
        self.buttonMsg = Button(self.labelBottom, text = "SEND", font = "Verdana 12 bold",  
                                width = 20, bg = "#FBAD34", fg = "#F8F8F8", 
                                command = lambda : self.sendButton(self.entryMsg.get())) 
        self.buttonMsg.place(relx = 0.77, rely = 0.0092, relheight = 0.047, relwidth = 0.22)

        self.textCons.config(cursor = "arrow") 

        # SCROLL BAR for CHATBOX
        scrollbar = Scrollbar(self.textCons, bg = "#FBAD34") 
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
		elif message == '!bye':
		    self.textCons.config(state = NORMAL) 
                    self.textCons.insert(END, message+"\n") 
                    self.textCons.config(state = DISABLED) 
                    self.textCons.see(END)
		    client.close()
                    self.root.destroy()
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
            msg = (f" {self.name} : {self.msg}") 
            message = encrypt(msg)
            client.send(message)
            break

# CLASS for CHATROOM GUI created
chatGUI = GUI() 
