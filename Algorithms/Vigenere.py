"""
Encryption and Decryption of Vigenere Cipher
"""


def generateKey(string, key):
    key = list(key)
    string = string.replace(" ", "")

    if len(string) == len(key):
        return key
    else:
        for i in range(len(string) - len(key)):
            key.append(key[i % len(key)])

    key = "".join(key).upper()
    return key


def Encrypt_Vigenere(message, keyword):
    encrypt_mess = ""
    message = message.replace(" ", "").upper()
    key = generateKey(message, keyword)

    for i in range(len(message)-1):
        en = (ord(message[i]) + ord(key[i])) % 26
        encrypt_mess = encrypt_mess + chr(en + 65)
    return encrypt_mess.lower()


def Decrypt_Vigenere(message, keyword):
    decrypt_mess = ""
    message = message.replace(" ", "").upper()
    key = generateKey(message, keyword)

    for i in range(len(message)):
        dec = (ord(message[i]) - ord(key[i]) + 26) % 26
        decrypt_mess = decrypt_mess + chr(dec + 65)
    return decrypt_mess.lower()


if __name__ == '__main__':
    mess = 'QWERTYUIOP'
    key = 'crypti'
    print(Encrypt_Vigenere(mess, key))
    print(Decrypt_Vigenere(mess, key))