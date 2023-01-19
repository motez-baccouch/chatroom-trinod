# import required modules
import socket, json, datetime
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP,AES
from base64 import b64encode, b64decode



HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class ClientFrame(tk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)

        self.top_frame = tk.Frame(self, width=600, height=100, bg=DARK_GREY)
        self.top_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.middle_frame = tk.Frame(self, width=600, height=400, bg=MEDIUM_GREY)
        self.middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.bottom_frame = tk.Frame(self, width=600, height=100, bg=DARK_GREY)
        self.bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

        self.username_label = tk.Label(self.top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
        self.username_label.pack(side=tk.LEFT, padx=10)

        self.username_textbox = tk.Entry(self.top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
        self.username_textbox.pack(side=tk.LEFT)

        self.username_button = tk.Button(self.top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.connect)
        self.username_button.pack(side=tk.LEFT, padx=15)

        self.message_textbox = tk.Entry(self.bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
        self.message_textbox.pack(side=tk.LEFT, padx=10)

        self.message_button = tk.Button(self.bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.send_message)
        self.message_button.pack(side=tk.LEFT, padx=10)

        self.message_box = scrolledtext.ScrolledText(self.middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
        self.message_box.config(state=tk.DISABLED, fg="green")
        self.message_box.pack(side=tk.TOP)


    def add_message(self, message:str):
        self.message_box.config(state=tk.NORMAL)
        if(len(message.split(':')) > 1):
            self.message_box.insert(tk.END, '['+message.split(":")[0]+ ']: '+ message.split(':')[1] + '\n')
        else: 
            self.message_box.insert(tk.END, message + '\n')
        self.message_box.config(state=tk.DISABLED)

    def connect(self):

        # connecting to socket
        try:
            # Connect to the server
            client.connect((HOST, PORT))
            print("Successfully connected to server")
            self.add_message("[SERVER] Successfully connected to the server")
        except:
            messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

        #sending username
        username = self.username_textbox.get()
        self.username= username
        if username != '':
            client.sendall(username.encode())
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")

        #generating keys
        self.generate_keys(username)

        #receiving server public key
        self.server_public_key = client.recv(1024).decode('utf-8')

        #sending public key to server
        self.send_pub_key(client, username)

        #receiving encrypted secret from serve
        self.server_secret= self.handle_secret(client)

        print(self.server_secret)

        #runnling listen thread
        threading.Thread(target=self.listen_for_messages_from_server, args=(client, )).start()


        self.username_textbox.config(state=tk.DISABLED)
        self.username_button.config(state=tk.DISABLED)

    def send_message(self):
        message = self.message_textbox.get()
        if message != '':
            cipher= AES.new(self.server_secret,AES.MODE_CFB)
            message_to_encrypt = self.username + ": " + message
            encrypted_msg = cipher.encrypt(message_to_encrypt.encode())
            iv = b64encode(cipher.iv).decode('utf-8')
            message = b64encode(encrypted_msg).decode('utf-8')
            self.message_textbox.delete(0, len(message))
            result = json.dumps({'iv': iv, 'ciphertext': message})
            client.send(result.encode())
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")

    def listen_for_messages_from_server(self, client):

        while 1:
            print("listening for message")
            message = client.recv(1024).decode()
            print(message)
            if message != '':
                key = self.server_secret
                print("testing receive")
                print(message)
                decrypt_message = json.loads(message)
                print("loaded json")
                iv = b64decode(decrypt_message['iv'])
                print("got iv")
                cipherText = b64decode(decrypt_message['ciphertext'])
                cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                msg = cipher.decrypt(cipherText)
                current_time = datetime.datetime.now()

                print(msg)
                self.add_message(msg.decode())
                
            else:
                messagebox.showerror("Error", "Message recevied from client is empty")
        
    def generate_keys(self, username):
        try:
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_key_pem = private_key.exportKey().decode()
            public_key_pem = public_key.exportKey().decode()
            print("creating keys")
            with open('chatroom_keys/{username}_private_key.pem'.format(username= username), 'wb') as priv:
                priv.write(private_key_pem.encode())
            with open('chatroom_keys/{username}_public_key.pem'.format(username= username), 'wb') as pub:
                pub.write(public_key_pem.encode())
            return public_key

        except Exception as e:
            print(e)

    def send_pub_key(self, c,username):
        try:
            public_key = RSA.importKey(open('chatroom_keys/{username}_public_key.pem'.format(username=username), 'r').read())
            c.send(public_key.exportKey())
            print('[+] Cle publique envoyé', 'yellow')
            return

        except Exception as e:
            print(e)
    
    def handle_secret(self,client):
        secret_key = client.recv(1024)
        private_key = RSA.importKey(open(f'chatroom_keys/{self.username}_private_key.pem', 'r').read())
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(secret_key)

