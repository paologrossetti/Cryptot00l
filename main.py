from CryptoClass.AESClass import AESClass
from CryptoClass.RSAClass import RSAClass

if __name__ == '__main__':
    '''aes = AESClass("this are 16bytes", "OFB")
    res_enc = aes.encrypt_file("/tmp/test_AES")#res_enc = aes.encrypt_string("secret")
    if res_enc:
        aes.decrypt_file(res_enc)#aes.decrypt_string(res_enc)'''
    rsa_alice = RSAClass('alice')
    rsa_bob = RSAClass('bob')
    data = rsa_alice.send_message('bob', 'Eve does not exists!')
    rsa_bob.receive_message(data)

