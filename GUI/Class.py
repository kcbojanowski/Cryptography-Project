class Client:
    shareKey = None
    shareInitVector = None
    shareOwnersAdresses = None
    ciphertext = None
    sharesRequired = None
    availableSockets = None

    def __init__(self, index: int):
        self.index = index

    def __str__(self):
        return f"Client nr {self.index}\n   Share: {self.shareKey}"