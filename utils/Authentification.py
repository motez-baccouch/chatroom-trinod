from getpass import getpass
import hashlib
import re
import sqlite3
from tabnanny import check
from utils.Utilisateur import Utilisateur


class Authentification:
    def __init__(self):
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
        
        
        
            
            
        utilisateur.username(username)
        motdepasse = hashlib.sha256(password.encode()).hexdigest()
        utilisateur.setMotdepasse(motdepasse)
           
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
        ##token=input("Entrer le token secret associe a ce compte:\n> ")
        ##if (not self.verifier_token(token,utilisateur.username)):
        ##    print("Credentials invalides.")
        ##    return False, None

        self.cursor.execute(sql_query, utilisateur_a_trouver)
        utilisateur_trouve=self.cursor.fetchone()
        return True, "welcome to our chatbot"

    def verifier_token(self, token, username):
        sql_query='SELECT * FROM utilisateur WHERE token=? and username=?'
        self.cursor.execute(sql_query, (token,username,))
        return self.cursor.fetchall() != []
