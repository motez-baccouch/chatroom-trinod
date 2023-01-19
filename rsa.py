from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Random import get_random_bytes


#server rsa functions 

def generate_keys():
        try:
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_key_pem = private_key.exportKey().decode()
            public_key_pem = public_key.exportKey().decode()
            with open('keys/Sprivatekeys.pem', 'w') as priv:
                priv.write(private_key_pem)
            with open('keys/Spublickeys.pem', 'w') as pub:
                pub.write(public_key_pem)
            return public_key

        except Exception as e:
            print(e)
            
def encrypt_secret(client_pub_key, secret_key):
        try:
            cpKey = RSA.importKey(client_pub_key)
            cipher = PKCS1_OAEP.new(cpKey)
            encrypted_secret = cipher.encrypt(secret_key)
            return encrypted_secret

        except Exception as e:
            print(e)

def send_secret(c, secret_key):
        try:
            c.send(secret_key)
        except Exception as e:
            print(e)

def send_pub_key( c):
        try:
            public_key = RSA.importKey(open('keys/Spublickeys.pem', 'r').read())
            c.send(public_key.exportKey())
            client_pub_key = c.recv(1024)
            print('[+] Cle publique du client recu')
            return client_pub_key

        except Exception as e:
            print(e)
            

#client rsa things

def handle_secret(self):
        secret_key = self.s.recv(1024)
        private_key = RSA.importKey(open(f'chatroom_keys/{self.username}_private_key.pem', 'r').read())
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(secret_key)

def exchange_public_keys(self):
    try:
        print('[+] Recevoir la cle publique du serveur')
        server_public_key = self.s.recv(1024).decode()
        server_public_key = RSA.importKey(server_public_key)

        print('[+] Envoyement de cle publique au serveur')
        public_pem_key = RSA.importKey(open(f'chatroom_keys/{self.username}_public_key.pem', 'r').read())
        self.s.send(public_pem_key.exportKey())
        print('[+] Echangement complete!')

    except Exception as e:
        print('[!] ERROR, you messed up something.... ' + str(e))

def create_key_pairs(self):
    try:
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()
        private_pem = private_key.exportKey().decode()
        public_pem = public_key.exportKey().decode()
        with open(f'chatroom_keys/{self.username}_private_key.pem', 'w') as priv:
            priv.write(private_pem)
        with open(f'chatroom_keys/{self.username}_public_key.pem', 'w') as pub:
            pub.write(public_pem)

    except Exception as e:
        print('[!] ERROR, you messed up something.... ' + e.__str__())
