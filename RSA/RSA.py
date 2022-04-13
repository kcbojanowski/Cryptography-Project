from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import binascii
import datetime

def key_pair():
    key_pair = RSA.generate(2048)

    pubKey = key_pair.publickey()
    #print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
    pubKeyPEM = pubKey.exportKey()
    public_key = pubKeyPEM.decode('ascii')
    now = datetime.datetime.now()
    date = now.strftime("%y_%m_%d_%H%M%S")
    with open('../RSA/public_key' + date + '.txt', "w") as f1:
        f1.write(public_key)

    #print(f"Private key: (n={hex(pubKey.n)}, d={hex(key_pair.d)})")
    privKeyPEM = key_pair.exportKey()
    private_key = privKeyPEM.decode('ascii')
    with open('../RSA/private_key' + date + '.txt', "w") as f1:
        f1.write(private_key)
    print("Pair of keys saves to /RSA")
    return public_key, private_key


# encryption
def RSA_Encrypt(msg, key):
    rsa_key = RSA.importKey(key)
    encryptor = PKCS1_OAEP.new(rsa_key)
    encrypted = encryptor.encrypt(msg.encode())
    return binascii.hexlify(encrypted)


if __name__ == '__main__':
    RSA_Encrypt("A message for encryption", )