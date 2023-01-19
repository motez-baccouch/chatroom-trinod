import os, datetime
import json, socket, threading

from termcolor import colored
from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox



DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


class Client(tk.Frame):
    
    
    def __init__(self, server, port, username,container):
        super().__init__(container)
        
        self.server = server
        self.port = port
        self.username = username
        self.isStopped = False
        
        

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
        self.message_box.config(state=tk.DISABLED)
        self.message_box.pack(side=tk.TOP)

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server, self.port))
        except Exception as e:
            print(colored('[!] ' + e.__str__(), 'red'))

        self.s.send(self.username.encode())
        self.add_message("[+] Connecte avec succes!")
        self.add_message("[+] Echangement de cles...")
       

        self.create_key_pairs()
        self.exchange_public_keys()
        global secret_key
        secret_key = self.handle_secret()

        self.add_message("[+] Initiation complete")
        self.add_message("[+] Vous pouvez echanger des messages")

        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.input_handler, args=())
        input_handler.start()
        while not self.isStopped:
            continue

    def handle_messages(self):
        while not self.isStopped:
            message = self.s.recv(1024).decode()
            if message:
                key = secret_key
                decrypt_message = json.loads(message)
                iv = b64decode(decrypt_message['iv'])
                cipherText = b64decode(decrypt_message['ciphertext'])
                cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                msg = cipher.decrypt(cipherText)
                current_time = datetime.datetime.now()
                self.add_message(current_time.strftime('%Y-%m-%d %H:%M:%S ') + msg.decode())
                print(current_time.strftime('%Y-%m-%d %H:%M:%S ') + msg.decode())
            else:
                self.add_message("[!] Connection au serveur perdue")
                self.add_message("[!] Fermeture de connection")
                print('[!] Connection au serveur perdue', 'red')
                print('[!] Fermeture de connection', 'red')
                self.s.shutdown(socket.SHUT_RDWR)
                self.isStopped = True

    def input_handler(self):
       
        message = self.message_textbox.get()
       
        key = secret_key
        cipher = AES.new(key, AES.MODE_CFB)
        message_to_encrypt = self.username + ": " + message
        msgBytes = message_to_encrypt.encode()
        encrypted_message = cipher.encrypt(msgBytes)
        iv = b64encode(cipher.iv).decode('utf-8')
        message = b64encode(encrypted_message).decode('utf-8')
        result = json.dumps({'iv': iv, 'ciphertext': message})
        self.s.send(result.encode())

        self.s.shutdown(socket.SHUT_RDWR)
        self.isStopped = True

    def handle_secret(self):
        secret_key = self.s.recv(1024)
        private_key = RSA.importKey(open(f'keys/{self.username}_private_key.pem', 'r').read())
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(secret_key)

    def exchange_public_keys(self):
        try:
            self.add_message("[+] Recevoir la cle publique du serveur")
            print('[+] Recevoir la cle publique du serveur', 'yellow')
            server_public_key = self.s.recv(1024).decode()
            server_public_key = RSA.importKey(server_public_key)

            self.add_message("[+] Envoyement de cle publique au serveur")
            print('[+] Envoyement de cle publique au serveur')
            public_pem_key = RSA.importKey(open(f'keys/{self.username}_public_key.pem', 'r').read())
            self.s.send(public_pem_key.exportKey())
            self.add_message("[+] Echangement complete!")
            print('[+] Echangement complete!')

        except Exception as e:
            print(colored('[!] ERROR, you messed up something.... ' + str(e), 'red'))

    def create_key_pairs(self):
        try:
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_pem = private_key.exportKey().decode()
            public_pem = public_key.exportKey().decode()
            with open(f'keys/{self.username}_private_key.pem', 'w') as priv:
                priv.write(private_pem)
            with open(f'keys/{self.username}_public_key.pem', 'w') as pub:
                pub.write(public_pem)

        except Exception as e:
            print(colored('[!] ERROR, you messed up something.... ' + e.__str__(), 'red'))


def initialize_and_start_client(username):
    client = Client('127.0.0.1', 8081, username)
    client.create_connection()
    

initialize_and_start_client("motez")