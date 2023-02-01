from getpass import getpass
import hashlib
import json
import re
import socket
import sqlite3
from tabnanny import check
from tkinter import messagebox
from utils.Utilisateur import Utilisateur
import ssl


class Authentification:
    def __init__(self):
        
        """ context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

        context.load_cert_chain(certfile="path/to/certificate.pem", keyfile="chatroom_keys/server_key.pem")
        
        with socket.create_connection(("127.0.0.1", 443)) as sock:
            with context.wrap_socket(sock, server_hostname="example.com") as ssock:
                # Send registration details over the SSL connection
                ssock.sendall(json.dumps({"username": username, "password": password}).encode())
                response = json.loads(ssock.recv(1024).decode())
                if response["status"] == "success":
                # Open a connection to the SQLite3 database
                    self.connection = sqlite3.connect("utilisateurs_bd.db")
                    self.cursor = self.connection.cursor()
                    self.cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='UTILISATEUR';")
                    if (self.cursor.fetchone()[0] != 'UTILISATEUR'):
                     print("Pas de compte trouvé.")
                    exit()
                else:
                    messagebox.showerror("Signup", "Invalid certificate") """
        
        self.connection = sqlite3.connect("utilisateurs_bd.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='UTILISATEUR';")
        if (self.cursor.fetchone()[0] != 'UTILISATEUR'):
            print("Pas de compte trouvé.")
            exit()
        
        

    def authentifier(self,username,password):
        utilisateur = Utilisateur()
        essais = 0
        
        
        
            
            
        utilisateur.setUsername(username)
        motdepasse = hashlib.sha256(password.encode()).hexdigest()
        utilisateur.setPassword(motdepasse)
           
        credentials_valides,message = self.trouver_utilisateur(utilisateur)
        return credentials_valides,message

    

    def trouver_utilisateur(self, utilisateur: Utilisateur):
        sql_query = 'SELECT * FROM utilisateur WHERE username=? and password=?;'
        utilisateur_a_trouver=(
            utilisateur.username,
            utilisateur.password
        )
        self.cursor.execute(sql_query, utilisateur_a_trouver)
        if (self.cursor.fetchall() == []):
            
            return False,"Credentials invalides."
       

        self.cursor.execute(sql_query, utilisateur_a_trouver)
        utilisateur_trouve=self.cursor.fetchone()
        return True, "welcome to our trinodchatbot"

    def verifier_token(self, token, username):
        sql_query='SELECT * FROM utilisateur WHERE token=? and username=?'
        self.cursor.execute(sql_query, (token,username,))
        return self.cursor.fetchall() != []
