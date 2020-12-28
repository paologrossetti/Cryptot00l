import os
import logging
from Crypto.Cipher import Salsa20
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes


class Salsa20Class:
    key = get_random_bytes(32)
    nonce = get_random_bytes(8)

    def __good_key(self):
        len_ley = len(self.key)
        if (len_ley % 16 == 0) or (len_ley % 32 == 0):
            return True
        else:
            return False

    def encrypt_string(self, string):
        try:
            if not self.__good_key():
                print("Lenght key must be 16 or 32 bytes long")
                return
            cipher = Salsa20.new(self.key, self.nonce)
            ct_bytes = cipher.encrypt(string.encode())
            ct = b64encode(ct_bytes).decode('utf-8')
            res = {'ciphertext': ct}
            print(res)
            return res
        except Exception as err:
            logging.error(f"Error in string encryption: {err}")
            return None

    def decrypt_string(self, res_enc):
        try:
            ciphertext = b64decode(res_enc.get('ciphertext'))
            cipher = Salsa20.new(self.key, self.nonce)
            plaintext = cipher.decrypt(ciphertext)
            print(f"String decrypted is: {plaintext.decode('utf-8')}")
        except Exception as err:
            logging.error(f"Error in string decryption: {err}")
            return None

    def encrypt_file(self, filepath):
        try:
            if not os.path.exists(filepath):
                print(f"Sorry: {filepath} does not exist")
                return
            if not self.__good_key():
                print("Lenght key must be 16 or 32 bytes long")
                return
            cipher = Salsa20.new(self.key, self.nonce)
            filepath_enc = f"{filepath}_enc"
            with open(filepath_enc, mode='wb+') as writer:
                with open(filepath, mode='rb') as reader:
                    ct_bytes = cipher.encrypt(reader.read())
                    writer.write(ct_bytes)
            res = {"file_enc": filepath_enc}
            print(res)
            return res
        except Exception as err:
            logging.error(f"Error in file encryption: {err}")
            return None

    def decrypt_file(self, res_enc):
        try:
            filepath_enc = res_enc.get('file_enc')
            if not os.path.exists(filepath_enc):
                print(f"Sorry: {filepath_enc} does not exist")
                return
            cipher = Salsa20.new(self.key, self.nonce)
            filepath_dec = f"{filepath_enc[:-4]}_dec"
            with open(filepath_dec, mode='wb+') as writer_dec:
                with open(res_enc.get('file_enc'), mode='rb') as reader_enc:
                    writer_dec.write(cipher.decrypt(reader_enc.read()))
            print(f"File decrypted is: {filepath_dec}")
        except Exception as err:
            logging.error(f"Error in file decryption: {err}")
            print(f"Error in file decryption: {err}")
