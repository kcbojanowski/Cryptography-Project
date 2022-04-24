"""
Encryption and Decryption of Playfair Cipher
"""


def create_matrix(key):
    key = key.upper()
    matrix = [[0 for col in range(5)] for row in range(5)]
    alphabet = [chr(letter) for letter in range(65, 91)]
    alphabet.remove('J')
    used_letters = []
    col = 0
    row = 0

    for letter in key:
        if letter not in used_letters:
            used_letters.append(letter)

    for letter in alphabet:
        if letter not in used_letters:
            used_letters.append(letter)

    nr = 0
    for i in range(5):
        for j in range(5):
            matrix[i][j] = used_letters[nr]
            nr += 1
    return matrix


def index_matrix(matrix, letter):

    for i, j in enumerate(matrix):
        if letter in j:
            return i, j.index(letter)


def Encrypt_Playfair(message, key):
    encrypt_mess = []
    matrix = create_matrix(key)
    message = message.strip().replace(" ", "").upper()
    message = message.replace("J", "I")

# adding 'X' in case of odd number of letters in message
    if not len(message) % 2 == 0:
        message += 'X'
    # adding 'X' in case of two similar symbols next to each other
    for n in range(0, len(message)-1, 2):
        if message[n] == message[n+1]:
            message = message[:n + 1] + 'X' + message[n + 1:]

        if not len(message) % 2 == 0:
            message += 'X'

        l1 = list(index_matrix(matrix, message[n]))
        l2 = list(index_matrix(matrix, message[n+1]))

# Case no.1 - same column
        if l1[1] == l2[1]:
            if l1[0] + 1 == 5:
                encrypt_mess.append(matrix[0][l1[1]])
            else:
                encrypt_mess.append(matrix[l1[0] + 1][l1[1]])

            if l2[0] + 1 == 5:
                encrypt_mess.append(matrix[0][l1[1]])
            else:
                encrypt_mess.append(matrix[l2[0] + 1][l2[1]])

# Case no.2 - same row
        elif l1[0] == l2[0]:
            if l1[1] + 1 == 5:
                encrypt_mess.append(matrix[l1[0]][0])
            else:
                encrypt_mess.append(matrix[l1[0]][l1[1] + 1])

            if l2[1] + 1 == 5:
                encrypt_mess.append(matrix[l2[0]][0])
            else:
                encrypt_mess.append(matrix[l2[0]][l2[1] + 1])

# Case no.3 - Normal Playfair algorithm
        else:
            encrypt_mess.append(matrix[l1[0]][l2[1]])
            encrypt_mess.append(matrix[l2[0]][l1[1]])

    return "".join(encrypt_mess).lower()


def Decrypt_Playfair(message, key):
    decrypt_mess = []
    matrix = create_matrix(key)
    mess = message.replace(" ", "").strip().upper()
    mess = mess.replace("J", "I")
    for n in range(0, len(mess)-1, 2):

        l1 = list(index_matrix(matrix, mess[n]))
        l2 = list(index_matrix(matrix, mess[n + 1]))

        # Case no.1 - same column
        if l1[1] == l2[1]:
            if l1[0] == 0:
                decrypt_mess.append(matrix[4][l1[1]])
            else:
                decrypt_mess.append(matrix[l1[0] - 1][l1[1]])

            if l2[0] == 0:
                decrypt_mess.append(matrix[4][l1[1]])
            else:
                decrypt_mess.append(matrix[l2[0] - 1][l2[1]])

        # Case no.2 - same row
        elif l1[0] == l2[0]:
            if l1[1] == 0:
                decrypt_mess.append(matrix[l1[0]][4])
            else:
                decrypt_mess.append(matrix[l1[0]][l1[1] - 1])

            if l2[1] == 0:
                decrypt_mess.append(matrix[l2[0]][4])
            else:
                decrypt_mess.append(matrix[l2[0]][l2[1] - 1])

        # Case no.3 - Normal Playfair algorithm
        else:
            decrypt_mess.append(matrix[l1[0]][l2[1]])
            decrypt_mess.append(matrix[l2[0]][l1[1]])

    return "".join(decrypt_mess).lower()


