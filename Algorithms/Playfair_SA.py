import Playfair
from math import log10, exp, floor
from time import time
import random
import string

"""
Approach for breaking a ciphertext made using Playfair using
Simulated annealing (SA) algorithm. It uses randomization and
comparision between keys to find a global maxima solution.
"""
class Playfair_SA(object):

    ngrams = {}
    total_sum = 0
    total_runs = 0

    def __init__(self, mess):
        self.mess = mess

    def GenerateQuadgrams(self, message):
        textgrams = []
        for i in range(len(message)):
            textgrams.append(message[i:i+4])

        return textgrams

    def Read_ngram(self):
        file = open("english_4grams.txt")

        for line in file:
            key, count = line.split(" ")
            self.ngrams[key] = int(count)
            self.total_sum += int(count)

    def Fitness(self, message):
        textgrams = self.GenerateQuadgrams(message)
        score = 0

        for gram in textgrams:
            if gram in self.ngrams:
                probability = self.ngrams[gram] / self.total_sum
                score += log10(probability)

        return score

    def Shuffle(self, parent_key):
        self.total_runs += 1
        shuffled_key = ""
        random.seed(time())
        prob = random.random()
        shuffle_matrix = Playfair.create_matrix(parent_key)
        r1 = random.randint(0, 5)
        r2 = random.randint(0, 5)

        while r1 == r2:
            r2 = random.randint(0, 5)

        if prob <= 0.2:
            shuffled_key = parent_key[::-1]
        elif prob <= 0.04:
            for i in range(len(shuffle_matrix)):
                shuffle_matrix[i] = shuffle_matrix[i][::-1]
        elif prob <= 0.06:
            for i in range(5):
                s = 0
                e = 4
                while s < e:
                    temp = shuffle_matrix[s][i]
                    shuffle_matrix[s][i] = shuffle_matrix[e][i]
                    shuffle_matrix[e][i] = temp
                    s += 1
                    e -= 1
        elif prob <= 0.08:
            temp = shuffle_matrix[r1]
            shuffle_matrix[r1] = shuffle_matrix[r2]
            shuffle_matrix[r2] = temp
        elif prob <= 0.1:
            for i in range(5) :
                temp = shuffle_matrix[i][r1]
                shuffle_matrix[i][r1] = shuffle_matrix[i][r2]
                shuffle_matrix[i][r2] = temp
        else:
            r1 = random.randint(0, 25)
            r2 = random.randint(0, 25)

            temp = shuffle_matrix[floor(r1 / 5)][r1 % 5]
            shuffle_matrix[r1 // 5][r1 % 5] = shuffle_matrix[r1 // 5][r2 % 5]
            shuffle_matrix[r1 // 5][r2 % 5] = temp

        if not shuffled_key:
            for i in shuffle_matrix:
                shuffled_key += str(i)

        return shuffled_key

    def Break_Playfair(self):
        temp = 0.0
        parent_key = ""
        child_key = ""
        parent_fitness = 0
        child_fitness = 0

        try:
            if not self.ngrams:
                self.Read_ngram()

            if len(self.mess) <= 120:
                temp = 10.0 + (0.087 * (len(self.mess) - 84))
            elif len(self.mess) <= 130:
                temp = 12.0
            else:
                temp = 10.0
            parent_key = ''.join(random.choices(string.ascii_uppercase, k=25))
            decrypted_mess = Playfair.Decrypt_Playfair(self.mess, parent_key)
            parent_fitness = self.Fitness(decrypted_mess)

        except FileNotFoundError:
            print('File with 4grams missing')

        while temp > 0:
            for i in range(50000, 0, -1):
                child_key = self.Shuffle(parent_key)
                decrypted_mess = Playfair.Decrypt_Playfair(self.mess, child_key)
                child_fitness = self.Fitness(decrypted_mess)
                delta = child_fitness - parent_fitness

                if delta > 0:
                    parent_key = child_key
                    parent_fitness = child_fitness
                elif delta < 0 and 1.0/exp((-1 * delta) / temp) > random.random():
                    parent_key = child_key
                    parent_fitness = child_fitness
            temp -= 1

        decrypted_mess = Playfair.Decrypt_Playfair(self.mess, parent_key)
        print(decrypted_mess)


if __name__ == '__main__':
    file = open("test_playfair", "r")
    message = file.read()
    message = "".join(message).upper()
    print(len(message))
    pf = Playfair_SA(message)
    pf.Break_Playfair()
