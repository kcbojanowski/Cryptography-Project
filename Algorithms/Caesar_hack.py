import nltk
nltk.download('words')
from nltk.corpus import words

alphabets = "abcdefghijklmnopqrstuvwxyz"

english_frequency_prob = [0.080, 0.015, 0.030, 0.040, 0.130, 0.020, 0.015, 0.060, 0.065, 0.005,
                          0.005, 0.035, 0.030, 0.070, 0.080, 0.020, 0.002, 0.065, 0.060, 0.090,
                          0.030, 0.010, 0.015, 0.005, 0.020, 0.002]

def caesar_hack(ciphertext):

    unique = []
    frequency = []
    psi = []
    key = 0
    value = 0.0
    exit = True

    for char in ciphertext:
        if (char not in unique) and (char.isalpha()):
            unique.append(char)

    only_alphabets = [char for char in ciphertext if char.isalpha()]

    for unique_char in unique:
        frequency.append(ciphertext.count(unique_char) / (float)(len(only_alphabets)))

    for i in range(0, 26):
        for unique_char in unique:
            value = value + frequency[unique.index(unique_char)] * english_frequency_prob[
                alphabets.index(unique_char) - i]
        psi.append(value)
        value = 0.0

    sorted_psi = psi[:]
    sorted_psi.sort(reverse=True)

    decoded_string = ""
    for i in range(0, 26):
        key = psi.index(sorted_psi[i])
        decoded_string = ""
        for char in ciphertext:
            if (char != ' '):
                decoded_string = decoded_string + alphabets[alphabets.index(char) - key]
            else:
                decoded_string = decoded_string + " "

        print("Testing key: ", key, " ....", decoded_string)

        for word in decoded_string.split():
            if word not in words.words():
                exit = False
            else:
                exit = True
        if exit:
            break

    print("\n", "Decoded : ", decoded_string, "\n")
    return decoded_string