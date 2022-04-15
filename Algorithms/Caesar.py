# Caesar cipher

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ALPHABET_SIZE = 26


def caesar_encrypt(plaintext, key):
    plaintext = plaintext.strip()
    ciphertext = ""
    if " " not in plaintext:
        for text in plaintext.lower():
            for char in text:
                ciphertext = ciphertext + ALPHABET[(ALPHABET.index(char) + key) % ALPHABET_SIZE]
    else:
        plaintext = plaintext.lower().split()
        for text in plaintext:
            for char in text:
                ciphertext = ciphertext + ALPHABET[(ALPHABET.index(char) + key) % ALPHABET_SIZE]
            ciphertext = ciphertext + " "
    return ciphertext


def caesar_decrypt(ciphertext, key):
    decrypted_text = ""
    if " " not in ciphertext:
        for text in ciphertext.lower():
            for char in text:
                decrypted_text = decrypted_text + ALPHABET[(ALPHABET.index(char) - key) % ALPHABET_SIZE]
    else:
        ciphertext = ciphertext.lower().split()
        for text in ciphertext:
            for char in text:
                decrypted_text = decrypted_text + ALPHABET[(ALPHABET.index(char) - key) % ALPHABET_SIZE]
            decrypted_text = decrypted_text + " "
    return decrypted_text


if __name__ == '__main__':
    plaintext = "aaa bbb cccc ddd"
    ciphertext = "bbb ccc ddd eee "
    key = 1
    print(caesar_decrypt(ciphertext, key))
