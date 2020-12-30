# Docker instructions

## Build Image
```console
foo@bar:~$ cd project_folder
foo@bar:~$ docker build -t cryptot00l:latest .
```
## Run and execute container

### Example encryption/decryption message
```console
foo@bar:~$ docker run --rm cryptot00l stream chacha20 -m 'This a s3cr3t!'
{'ciphertext': 'vu4kDGz5eroqbAp2+64='}
String decrypted is: This a s3cr3t!
```
### Example encryption/decryption RSA message
```console
foo@bar:~$ docker run --rm cryptot00l rsa alice bob 'Eve cant read this'
Sent message to bob: b'8\x93\x11IV\xa9\x88\xecF\xf7.....X7\xdf\x84\x9a4\xfe\xf3\x1>l)@\xb1rMV\xd8\xc5\x9eS\x84)X^U2o@'
RSA secret is: Eve cant read this
```
### Example encryption/decryption file
```console
foo@bar:~$ docker run -v ABS_LOCAL_FILEPATH:ABS_CONTAINER_FILEPATH --rm cryptot00l aes -t cbc -f ABS_LOCAL_FILEPATH
AES:cbc MODE
{'file_enc': '/tmp/test_enc', 'iv': 'RHPnRG/ycv0zjUS9nhlFNQ=='}
File decrypted is: /tmp/test_dec
```