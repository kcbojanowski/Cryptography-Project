# Caesar cipher

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ALPHABET_SIZE = 26


def caesar_encrypt(plaintext, key):
    ciphertext = ""
    #print("Plaintext: ", plaintext)
    for text in plaintext.lower().split():
        for char in text:
            ciphertext = ciphertext + ALPHABET[(ALPHABET.index(char) + key) % ALPHABET_SIZE]
   #print("Ciphertext: ",  ciphertext)
    return ciphertext
    return ciphertext


def caesar_decrypt(ciphertext, key):
    decrypted_text = ""
    for text in ciphertext:
        for char in text:
            decrypted_text = decrypted_text + ALPHABET[(ALPHABET.index(char) - key) % ALPHABET_SIZE]
    #print("Decrypted message: ", decrypted_text)
    return decrypted_text
    return decrypted_text


if __name__ == '__main__':
    plaintext = "apple"
    ciphertext = ""
    key = 5