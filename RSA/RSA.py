import ast
import base64

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import binascii
import datetime

def key_pair():
    key_pair = RSA.generate(2048)

    pubKey = key_pair.publickey()
    #print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")klucz
    pubKeyPEM = pubKey.exportKey()
    public_key = pubKeyPEM.decode('ascii')
    now = datetime.datetime.now()
    date = now.strftime("%y_%m_%d_%H%M%S")
    with open('../RSA/public_key' + date + '.pem', "w") as f1:
        f1.write(public_key)
        f1.close()
    #print(f"Private key: (n={hex(pubKey.n)}, d={hex(key_pair.d)})")
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

if __name__ == '__main__':
    msg = "90de302dcf4c4a69327a141d8a9ee8b08264e0d8664fc005204fbb54d0c9131cf37bffe98284c583223293ea05996af9e034139e9bc4a1644b2482924fcf04b9edf8a75c586bf8e9eb105867ed28f0219e9451ce8b6dcd1d1d6a2c80008f873681e827f6e2e851aeb5bd7836484ffe49ad31e96dea7eabcb0a4eddadc223a95b6bfebd715d9f01b0169f5773d86a3e10eab6ebbf36f6d5eb93b8a65d85de9eee7c33279b3965219dbcfcfa0af82a03834f705c2b020edcea726e64bccb51751c5747f2865322a7d1c2cae9ab0fd349749dfe79ae54ced9628009cc2989670b8eee4b699447881684a107ef95bf980da97c5b3d9d68b75e001669fc354f0d9551"
    with open('private_key22_04_15_160913.pem', "r") as key:
        priv = key.read()
        key.close()
    RSA_Decrypt(msg, priv)