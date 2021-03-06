import os
import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class RSAClass:
    def __init__(self, user):
        self.user = user
        self.iskeygen = self.__keygen()

    def __keygen(self):
        try:
            rsa_dir = os.path.join(os.getcwd(), 'rsa_key')
            if not os.path.exists(rsa_dir):
                os.makedirs(rsa_dir, exist_ok=True)
            key = RSA.generate(4096)
            private_key = key.export_key()
            with open(os.path.join(rsa_dir, f'{self.user}_private.pem'), mode='wb+') as private_out:
                private_out.write(private_key)
            public_key = key.publickey().export_key()
            with open(os.path.join(rsa_dir, f'{self.user}_public.key'), mode='wb+') as public_out:
                public_out.write(public_key)
            return True
        except Exception as err:
            logging.error(f"For user {self.user}, error during keygen: {err}")
            return False

    def send_message(self, receiver, message):
        try:
            if not self.iskeygen:
                logging.error("Private and/or public key are not available")
                return None
            receiver_pubkey = RSA.import_key(open(os.path.join(os.getcwd(), 'rsa_key', f"{receiver}_public.key")).read())
            cipher = PKCS1_OAEP.new(receiver_pubkey)
            ciphertext = cipher.encrypt(message.encode())  # ciphertext 4096 length
            print(f"Sent message to {receiver}: {ciphertext}")
            return {"receiver": receiver, "ciphertext": ciphertext}
        except Exception as err:
            logging.error(f"Error during send message RSA: {err}")
            return None

    def receive_message(self, data):
        try:
            if not self.iskeygen:
                logging.error("Private and/or public key are not available")
                return None
            my_privkey = RSA.import_key(open(os.path.join(os.getcwd(), 'rsa_key', f"{data.get('receiver')}_private.pem")).read())
            cipher = PKCS1_OAEP.new(my_privkey)
            plaintext = cipher.decrypt(data.get('ciphertext'))
            print(f"RSA secret is: {plaintext.decode()}")
        except Exception as err:
            logging.error(f"Error during send message RSA: {err}")
