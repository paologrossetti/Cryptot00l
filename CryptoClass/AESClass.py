import logging
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESClass:
    def __init__(self, key, mode):
        self.key = key.encode()
        modes = {
            "ECB": AES.MODE_ECB,
            "CBC": AES.MODE_CBC,
            "CTR": AES.MODE_CTR,
            "CFB": AES.MODE_CFB,
            "OFB": AES.MODE_OFB
        }
        aes_mode = modes.get(mode, None)
        if aes_mode:
            self.mode = aes_mode
        else:
            self.mode = AES.MODE_CBC
        print(f"AES:{mode} MODE")

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
            logging.error(f"Error in string encryption: {err}")
            print(f"Error in string decryption: {err}")

    def encrypt_file(self, data):
        pass

    def decrypt(self, data):
        pass
