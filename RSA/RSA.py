import ast
import base64

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import binascii
import datetime

def key_pair():
    # generate pair of keys
    key_pair = RSA.generate(2048)

    # substract public key and translate to bytes
    pubKey = key_pair.publickey()
    pubKeyPEM = pubKey.exportKey()
    # translate to ascii
    public_key = pubKeyPEM.decode('ascii')
    # current date
    now = datetime.datetime.now()
    date = now.strftime("%y_%m_%d_%H%M%S")
    # save it to /RSA diractory
    with open('../RSA/public_key' + date + '.pem', "w") as f1:
        f1.write(public_key)
        f1.close()

    privKeyPEM = key_pair.exportKey()
    private_key = privKeyPEM.decode('ascii')
    with open('../RSA/private_key' + date + '.pem', "w") as f2:
        f2.write(private_key)
        f2.close()
    print("Pair of keys saves to /RSA")
    return public_key, private_key


# encryption
def RSA_Encrypt(msg, key):
    rsa_key = RSA.importKey(key)
    encryptor = PKCS1_OAEP.new(rsa_key)
    encrypted = encryptor.encrypt(msg.encode())
    return base64.b64encode(encrypted)


def RSA_Decrypt(msg, key):
    decoded_data = base64.b64decode(msg)
    private_key = RSA.importKey(key)
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted = decryptor.decrypt(decoded_data)
    return decrypted.decode()

