class Utilisateur:
    def __init__(self):
        self.username = None
        self.password = None
        self.token = None

    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def setToken(self, token):
        self.token = token

    def afficher(self):
        print()
        print("Bienvenue " + self.prenom + " " + self.nom + " :D")
