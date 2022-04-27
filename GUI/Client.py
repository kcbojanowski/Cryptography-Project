import socket
import pickle

HEADER = 32
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)

#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

#send("Hello World!")

#input()
'''
send("Hello Wolrd 2!")
input()
send("Hello World 3!")'''

#send(DISCONNECT_MESSAGE)

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    msg = client.recv(2048)
    client = pickle.loads(msg)
    print(f'Share: {client.shareKey}')