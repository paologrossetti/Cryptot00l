import argparse
from CryptoClass.AESClass import AESClass
from CryptoClass.RSAClass import RSAClass
from CryptoClass.Salsa20Class import Salsa20Class
from CryptoClass.ChaCha20Class import ChaCha20Class


def main(args):
    switch = {
        'aes': start_aes,
        'rsa': start_rsa,
        'salsa20': start_salsa20,
        'chacha20': start_chacha20
    }
    cipher = switch.get(args.cipher, None)
    if cipher:
        cipher(args)
    else:
        print("Please, run the command with the -h or –help for usage information")


def start_aes(args):
    mode = args.type
    message = args.message
    file = args.file
    aes = AESClass(mode=mode)
    if message:
        res_enc = aes.encrypt_string(message)
        if res_enc:
            aes.decrypt_string(res_enc)
    else:
        res_enc = aes.encrypt_file(file)
        if res_enc:
            aes.decrypt_file(res_enc)


def start_rsa(args):
    sender = args.sender
    receiver = args.receiver
    message = args.message
    rsa_sender = RSAClass(sender)
    rsa_receiver = RSAClass(receiver)
    res_enc = rsa_sender.send_message(receiver=rsa_receiver.user, message=message)
    if res_enc:
        rsa_receiver.receive_message(res_enc)


def start_salsa20(args):
    message = args.message
    file = args.file
    salsa20 = Salsa20Class()
    if message:
        res_enc = salsa20.encrypt_string(message)
        if res_enc:
            salsa20.decrypt_string(res_enc)
    else:
        res_enc = salsa20.encrypt_file(file)
        if res_enc:
            salsa20.decrypt_file(res_enc)


def start_chacha20(args):
    message = args.message
    file = args.file
    chacha20 = ChaCha20Class()
    if message:
        res_enc = chacha20.encrypt_string(message)
        if res_enc:
            chacha20.decrypt_string(res_enc)
    else:
        res_enc = chacha20.encrypt_file(file)
        if res_enc:
            chacha20.decrypt_file(res_enc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt/decrypt message and file.')
    subparsers = parser.add_subparsers(help='Sub-command help')

    parser_aes = subparsers.add_parser('aes', help='AES cipher help')
    parser_aes.add_argument('cipher', default='aes', choices=['aes'], nargs='?')
    parser_aes.add_argument("-t", "--type", choices=['ecb', 'cbc', 'ctr', 'cfb', 'ofb'], help="AES type")
    group_aes = parser_aes.add_mutually_exclusive_group(required=True)
    group_aes.add_argument("-m", "--message", help="Message to encrypt")
    group_aes.add_argument("-f", "--file", help="Filepath to encrypt")

    parser_rsa = subparsers.add_parser('rsa', help='RSA cipher help')
    parser_rsa.add_argument('cipher', default='rsa', choices=['rsa'], nargs='?')
    parser_rsa.add_argument("sender", help="Sender of the message")
    parser_rsa.add_argument("receiver", help="Receiver of the message")
    parser_rsa.add_argument("message", help="Message to send")

    parser_stream = subparsers.add_parser('stream', help='Stream cipher help')
    parser_stream.add_argument('cipher', choices=['salsa20', 'chacha20'])
    group_stream = parser_stream.add_mutually_exclusive_group(required=True)
    group_stream.add_argument("-m", "--message", help="Message to encrypt")
    group_stream.add_argument("-f", "--file", help="Filepath to encrypt")

    args = parser.parse_args()
    if hasattr(args, 'cipher'):
        main(args)
    else:
        parser.print_help()
