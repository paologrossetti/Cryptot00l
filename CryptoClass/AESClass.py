import os
import logging
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class AESClass:
    def __init__(self, mode):
        self.key = get_random_bytes(32)
        modes = {
            "ECB": AES.MODE_ECB,
            "CBC": AES.MODE_CBC,
            "CTR": AES.MODE_CTR,
            "CFB": AES.MODE_CFB,
            "OFB": AES.MODE_OFB
        }
        self.mode = modes.get(mode, AES.MODE_CBC)
        print(f"AES:{mode if mode else 'CBC'} MODE")

    def __good_key(self):
        len_ley = len(self.key)
        if (len_ley % 16 == 0) or (len_ley % 24 == 0) or (len_ley % 32 == 0):
            return True
        else:
            return False

    def encrypt_string(self, data):
        try:
            if not self.__good_key():
                print("Lenght key must be 16, 24 or 32 bytes long")
                return
            cipher = AES.new(self.key, self.mode)
            if self.mode in (AES.MODE_CFB, AES.MODE_CTR, AES.MODE_OFB):
                ct_bytes = cipher.encrypt(data.encode())
            else:
                # pad: the output length is guaranteed to be a multiple of block_size
                ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
            # Must be base64 encode beacuse, probably, there is some non-ascii character and it can't be encoded/decoded
            ct = b64encode(ct_bytes).decode('utf-8')
            res = {'ciphertext': ct}
            if self.mode in (AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB):
                iv = b64encode(cipher.iv).decode('utf-8')
                res.update({'iv': iv})
            if self.mode == AES.MODE_CTR:
                nonce = b64encode(cipher.nonce).decode('utf-8')
                res.update({'nonce': nonce})
            print(res)
            return res
        except Exception as err:
            logging.error(f"Error in string encryption: {err}")
            return None

    def decrypt_string(self, res_enc):
        try:
            # need: key, mode, iv
            if self.mode in (AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB):
                cipher = AES.new(self.key, self.mode, iv=b64decode(res_enc.get("iv")))
            elif self.mode == AES.MODE_CTR:
                cipher = AES.new(self.key, self.mode, nonce=b64decode(res_enc.get("nonce")))
            else:
                cipher = AES.new(self.key, self.mode)

            if self.mode in (AES.MODE_CFB, AES.MODE_CTR, AES.MODE_OFB):
                res = cipher.decrypt(b64decode(res_enc.get("ciphertext"))).decode()
            else:
                res = unpad(cipher.decrypt(b64decode(res_enc.get("ciphertext"))), AES.block_size).decode()
            print(f"String decrypted is: {res}")
        except Exception as err:
            logging.error(f"Error in string decryption: {err}")
            print(f"Error in string decryption: {err}")

    def encrypt_file(self, filepath):
        try:
            if not os.path.exists(filepath):
                print(f"Sorry: {filepath} does not exist")
                return
            if not self.__good_key():
                print("Lenght key must be 16, 24 or 32 bytes long")
                return
            cipher = AES.new(self.key, self.mode)
            filepath_enc = f"{filepath}_enc"
            with open(filepath_enc, mode='wb+') as writer:
                with open(filepath, mode='rb') as reader:
                    block = reader.read(16)
                    while block:
                        if self.mode in (AES.MODE_CFB, AES.MODE_CTR, AES.MODE_OFB):
                            ct_bytes = cipher.encrypt(block)
                        else:
                            # pad: the output length is guaranteed to be a multiple of block_size
                            ct_bytes = cipher.encrypt(pad(block, AES.block_size))
                        writer.write(ct_bytes)
                        block = reader.read(16)
            res = {"file_enc": filepath_enc}
            if self.mode in (AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB):
                iv = b64encode(cipher.iv).decode('utf-8')
                res.update({'iv': iv})
            if self.mode == AES.MODE_CTR:
                nonce = b64encode(cipher.nonce).decode('utf-8')
                res.update({'nonce': nonce})
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
            # need: key, mode, iv
            if self.mode in (AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB):
                cipher = AES.new(self.key, self.mode, iv=b64decode(res_enc.get("iv")))
            elif self.mode == AES.MODE_CTR:
                cipher = AES.new(self.key, self.mode, nonce=b64decode(res_enc.get("nonce")))
            else:
                cipher = AES.new(self.key, self.mode)
            filepath_dec = f"{filepath_enc[:-4]}_dec"
            with open(filepath_dec, mode='wb+') as writer_dec:
                with open(res_enc.get('file_enc'), mode='rb') as reader_enc:
                    block = reader_enc.read(16)
                    while block:
                        writer_dec.write(cipher.decrypt(block))
                        block = reader_enc.read(16)
            print(f"File decrypted is: {filepath_dec}")
        except Exception as err:
            logging.error(f"Error in file decryption: {err}")
            print(f"Error in file decryption: {err}")
