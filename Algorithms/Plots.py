from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from collections import Counter


def alphabet_plot(msg):
    alphabet = [chr(letter) for letter in range(65, 91)]
    msg = msg.upper()
    counter = Counter(msg)
    sorted_counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
    letters = list(sorted_counter.keys())
    numbers = list(sorted_counter.values())

    letterFrequency = {'E': 12.0,
                       'T': 9.10,
                       'A': 8.12,
                       'O': 7.68,
                       'I': 7.31,
                       'N': 6.95,
                       'S': 6.28,
                       'R': 6.02,
                       'H': 5.92,
                       'D': 4.32,
                       'L': 3.98,
                       'U': 2.88,
                       'C': 2.71,
                       'M': 2.61,
                       'F': 2.30,
                       'Y': 2.11,
                       'W': 2.09,
                       'G': 2.03,
                       'P': 1.82,
                       'B': 1.49,
                       'V': 1.11,
                       'K': 0.69,
                       'X': 0.17,
                       'Q': 0.11,
                       'J': 0.10,
                       'Z': 0.07}

    sort_frqs = dict(sorted(letterFrequency.items(), key=lambda item: item[1], reverse=True))
    letters2 = list(sort_frqs.keys())
    numbers2 = list(sort_frqs.values())

    fig, (ax1, ax2) = plt.subplots(2, figsize=(5, 6))
    fig.suptitle('Frequencies of letters')
    fig.tight_layout(pad=2.0)
    ax1.bar(range(len(sorted_counter)), numbers, tick_label=letters)
    ax1.set_title("Your text")

    ax2.bar(range(len(sort_frqs)), numbers2, tick_label=letters2)
    ax2.set_title("English alphabet")

    return fig


if __name__ == '__main__':
    msg = "creseczka fresh siedzi pach boombastic"
    fig = alphabet_plot(msg)
    plt.show()