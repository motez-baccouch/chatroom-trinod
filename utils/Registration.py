import re
import secrets
import sqlite3
import hashlib
import string
from utils.Utilisateur import Utilisateur
from getpass import getpass


class Registration:
    def __init__(self):
        self.connection = sqlite3.connect("utilisateurs_bd.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='UTILISATEUR';")
        if (self.cursor.fetchall() == []):
            self.cursor.execute(
                "CREATE TABLE UTILISATEUR(username VARCHAR2, password VARCHAR2, token VARCHAR2)")

    def registrer(self,username,password,passwordRepeat):
        utilisateur = Utilisateur()
        utilisateur_existe = self.verifier_utilisateur_existant(username)
        if (not self.verifier_username(username) or utilisateur_existe):
            if (not self.verifier_username(username)):
                return "usename invalide."
            if (utilisateur_existe):
                return "username existe deja."
    
            utilisateur_existe = self.verifier_utilisateur_existant(
                username)
        utilisateur.setUsername(username)

        


       
        if(password != passwordRepeat):
            return "passwords does not match"
        else:    
            motdepasse = hashlib.sha256(password.encode()).hexdigest()
            utilisateur.setMotdepasse(motdepasse)

        token = self.generer_token()
        utilisateur.setToken(token)

        print()
        print("Le token associé à ce compte est: ", utilisateur.token)
        token_path = input(
            "Donner le path du fichier pour sauvegarder le token:\n> ")
        with open(token_path, 'a') as f:
            f.write(''+utilisateur.username+': '+utilisateur.token+"\n")
        self.enregistrer_bd(utilisateur)

        return True, utilisateur

  

    def verfier_username(self, nom):
        regex = re.compile(r'^[a-zA-Z]+$')
        return re.fullmatch(regex, nom)

    def verifier_motdepasse(self, passwd):
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$')
        return re.fullmatch(regex, passwd)

    def verifier_utilisateur_existant(self, email):
        self.cursor.execute(
            'SELECT * FROM utilisateur WHERE username=?', (email,))
        return self.cursor.fetchall() != []

    def enregistrer_bd(self, utilisateur: Utilisateur):
        sql_query = 'INSERT INTO utilisateur VALUES(?,?,?);'
        utilisateur_insertion = (
            utilisateur.username,
            utilisateur.password,
            utilisateur.token
        )
        self.cursor.execute(sql_query, utilisateur_insertion)
        self.connection.commit()

    def generer_token(self):
        num = 8
        token = ''.join(secrets.choice(string.ascii_letters +
                                       string.digits) for x in range(num))
        return token


