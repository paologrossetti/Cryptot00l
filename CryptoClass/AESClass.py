import logging
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


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
            # pad: the output length is guaranteed to be a multiple of block_size
            ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
            # Must be base64 encode beacuse, probably, there is some non-ascii character and it can't be encoded/decoded
            ct = b64encode(ct_bytes).decode('utf-8')
            if self.mode is AES.MODE_ECB:
                print({'ciphertext': ct})
            elif self.mode is AES.MODE_CTR:
                nonce = b64encode(cipher.nonce).decode('utf-8')
                print({'nonce': nonce, 'ciphertext': ct})
            else:
                iv = b64encode(cipher.iv).decode('utf-8')
                print({'iv': iv, 'ciphertext': ct})
        except Exception as err:
            logging.error(f"Error in string encryption: {err}")

    def decrypt_string(self):
        pass


