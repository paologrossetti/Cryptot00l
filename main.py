from CryptoClass.AESClass import AESClass

if __name__ == '__main__':
    aes = AESClass("this are 16bytes", "OFB")
    res_enc = aes.encrypt_string("secret")
    if res_enc:
        aes.decrypt_string(res_enc)
