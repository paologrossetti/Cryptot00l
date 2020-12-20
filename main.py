from CryptoClass.AESClass import AESClass

if __name__ == '__main__':
    aes = AESClass("this are 16bytes", "CBC")
    aes.encrypt_string("secret")
