from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Algorithms.Vigenere as Vigenere
import Algorithms.Playfair as Playfair
import Algorithms.Caesar as Caesar
import Algorithms.Caesar_hack as Caesar_hack
import Algorithms.Plots as Plots
import RSA.RSA as rsa
#import SSS.Server as server
import SSS.SSS as sss
from Class import Client
from copy import copy
import ctypes
import threading
import socket
import pickle
import os

colors = ["#8ecae6", "#219ebc", "#f8f7ff", "#34a0a4", "#76c893"]
# colors = [background, labels, textfields, page buttons, other buttons]

HEADER = 32
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class AlgoPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        algoframe = Frame(self, bg=colors[0])
        algoframe.pack(side="top", fill="both", expand=True)

        label = Label(algoframe, text="Algorithms", font=("BebasNeue-Regular", 15), bg=colors[1])
        label.pack(side="top", fill="y", anchor=NE, expand=False, pady=30, padx=30)

        instr = Label(algoframe, text="Choose an algorithm:", font=("BebasNeue-Regular", 13), bg=colors[1])
        instr.pack(side="top", fill="y", anchor=NE, expand=False, padx=30)

        options = ["Ceasar", "Playfair", "Vigenere"]
        algorithms = StringVar()
        algorithms.set(options[0])

        def callback(*args):
            if algorithms.get() != "Ceasar":
                crack_btn.pack_forget()
            else:
                crack_btn.pack(side="bottom", expand=False, pady=5, padx=10)

        algorithms.trace("w", callback)
        combo = OptionMenu(algoframe, algorithms, *options)

        combo.pack(side="top", fill="y", anchor=NE, expand=False, padx=30)

        crack_btn = Button(algoframe, text="Break", font=("BebasNeue-Regular", 11), width=12, height=15,
                           bg=colors[4], command=lambda: break_ceasar())
        crack_btn.pack(side="left", anchor=W, expand=False, pady=5, padx=10)

        freq_btn = Button(algoframe, text="Letter plots", font=("BebasNeue-Regular", 11), width=12, height=15,
                           bg=colors[4], command=lambda: plots())
        freq_btn.pack(side="right", anchor=W, expand=False, pady=5, padx=10)

        input_txt = Text(algoframe, height=12, width=30, bg=colors[2])

        input_txt.pack(side="top", fill="both", expand=True, pady=10)

        key_label = Label(algoframe, text="enter key:", font=("BebasNeue-Regular", 12), bg=colors[1])
        key_label.pack(side="top", expand=False)

        key_txt = Entry(algoframe)
        key_txt.pack(side="top", fill="y", expand=False, pady=10)

        encrypt_btn = Button(algoframe, text="encrypt", font=("BebasNeue-Regular", 11), width=12,
                             bg=colors[4], command=lambda: encrypt())
        encrypt_btn.pack(side="top", expand=False, pady=5)

        decrypt_btn = Button(algoframe, text="decrypt", font=("BebasNeue-Regular", 11), width=12,
                             bg=colors[4],command=lambda: decrypt())
        decrypt_btn.pack(side="top", expand=False, pady=5)

        output = Text(algoframe, height=12, width=30, bg=colors[2])
        output.pack(side="top", fill="both", expand=True, pady=10)

        def encrypt():
            output.delete('1.0', END)
            current_algo = algorithms.get()
            message_input = input_txt.get("1.0", END)
            key_input = key_txt.get().strip()
            if key_input == "" or message_input == "":
                message("Warning", "Enter message and key first!")
            else:
                if current_algo == "Playfair":
                    out = Playfair.Encrypt_Playfair(message_input, key_input)
                    output.insert("1.0", out)

                if current_algo == "Vigenere":
                    out = Vigenere.Encrypt_Vigenere(message_input, key_input)
                    output.insert(END, out)

                if current_algo == "Ceasar":
                    if key_input.isnumeric():
                        out = Caesar.caesar_encrypt(message_input, int(key_input))
                        output.insert(END, out)
                    else:
                        message("Warning", "Key must be a number")

        def decrypt():
            output.delete('1.0', END)
            current_algo = algorithms.get()
            message_input = input_txt.get("1.0", END).strip()
            key_input = key_txt.get().strip()
            if key_input == "" or message_input == "":
                message("Warning", "Enter message and key first!")
            else:
                if current_algo == "Playfair":
                    stripped_msg = message_input.replace(" ", "").strip()
                    if len(stripped_msg) % 2 == 0:
                        out = Playfair.Decrypt_Playfair(message_input, key_input)
                        output.insert(END, out)
                    else:
                        message("Warning", "It is not a Playfair ciphertext")

                if current_algo == "Vigenere":
                    out = Vigenere.Decrypt_Vigenere(message_input, key_input)
                    output.insert(END, out)

                if current_algo == "Ceasar":
                    if key_input.isnumeric():
                        out = Caesar.caesar_decrypt(message_input, int(key_input))
                        output.insert(END, out)
                    else:
                        message("Warning", "Key must be a number")

        def break_ceasar():
            output.delete('1.0', END)
            message_input = input_txt.get("1.0", END).strip()
            if message_input != "":
                out = Caesar_hack.caesar_hack(message_input)
                output.insert(END, out)
            else:
                message("Warning", "Enter the message first!")

        def plots():
            msg = input_txt.get("1.0", END).strip().replace(" ", "")
            cipher = output.get("1.0", END).strip().replace(" ", "")
            fig = Plots.alphabet_plot(msg, cipher)
            newwindow = Toplevel(self)
            canvas = FigureCanvasTkAgg(fig, master=newwindow)
            canvas.draw()
            canvas.get_tk_widget().pack()


class SSSPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        clients = []
        clientSockets = []
        clientAdresses = []

        self.shares = []

        sssframe = Frame(self, bg=colors[0])
        sssframe.pack(side="top", fill="both", expand=True)

        label = Label(sssframe, text="Shamir's Secret Sharing", font=("BebasNeue-Regular", 15), bg=colors[1])
        label.pack(side="top", fill="y", anchor=W, expand=False, pady=10, padx=20)

        key_label = Label(sssframe, text="enter pin:", font=("BebasNeue-Regular", 12), bg=colors[1])
        key_label.pack(side="top", expand=False, pady=5)

        self.input_txt = Entry(sssframe, width=30, bg=colors[2])
        self.input_txt.pack(side="top", pady=1, padx=1)

        shares_label = Label(sssframe, text="Shares:", font=("BebasNeue-Regular", 12), bg=colors[1])
        shares_label.pack(side="top", expand=False, pady=5)

        self.shares_txt = Text(sssframe, height=5, width=30, bg=colors[2])
        self.shares_txt.pack(side="top", fill="both", expand=False, pady=5, padx=10)

        key_label = Label(sssframe, text="Server console:", font=("BebasNeue-Regular", 12), bg=colors[1])
        key_label.pack(side="top", expand=False, pady=5)

        self.server_txt = Text(sssframe, height=12, width=30, bg=colors[2])
        self.server_txt.pack(side="top", fill="both", expand=True, pady=5, padx=10)

        recon_btn = Button(sssframe, text="Reconstruction", font=("BebasNeue-Regular", 11), width=14,
                          bg=colors[4], command=lambda: self.reconstruction())
        recon_btn.pack(side="right", expand=False, padx=5, pady=5)

        send_btn = Button(sssframe, text="Send shares", font=("BebasNeue-Regular", 11), width=14,
                                 bg=colors[4], command=lambda: send_shares())
        send_btn.pack(side="right", expand=False, padx=5, pady=5)

        connections_btn = Button(sssframe, text="Active connections", font=("BebasNeue-Regular", 11), width=16,
                            bg=colors[4], command=lambda: active_connections())
        connections_btn.pack(side="right", expand=False, padx=5, pady=5)

        server_btn = Button(sssframe, text="Start server", font=("BebasNeue-Regular", 11), width=14,
                         bg=colors[4], command=lambda: server_start())
        server_btn.pack(side="right", expand=False, padx=5, pady=5)

        sss_btn = Button(sssframe, text="Generate secrets", font=("BebasNeue-Regular", 11), width=14,
                          bg=colors[4], command=lambda: self.sharing())
        sss_btn.pack(side="right", expand=False, padx=5, pady=5)

        def handle_client(conn, addr):
            #print(f"[NEW CONNECTION] {addr} connected.")
            self.server_txt.insert(END, f"\n\n[NEW CONNECTION] {addr} connected.")

            connected = True
            while connected:
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    if msg == DISCONNECT_MESSAGE:
                        connected = False

                    #print(f"[{addr}] {msg}")
                    self.server_txt.insert(END, f"\n[{addr}] {msg}")
                    conn.send("Msg received".encode(FORMAT))
            conn.close()

        '''
        def get_server():
            return SERVER
            '''

        def server_start():
            thread = threading.Thread(target=start)
            thread.start()
            message("Info", "Server is listening")
            #s = get_server()
            #self.server_txt.insert(END, "[STARTING] server is starting...\n")
            #self.server_txt.insert(END, "[LISTENING] Server is listening on " + s + "\n")

        def start():
            self.server_txt.insert(END, "[STARTING] server is starting...\n")
            server.listen()
            self.server_txt.insert(END, "[LISTENING] Server is listening on " + SERVER + "\n")

            for i in range(0, 5):
                conn, addr = server.accept()
                client = Client(i)
                clientSockets.append(conn)
                clientAdresses.append(addr)
                clients.append(client)
                self.server_txt.insert(END, f"\n\n[NEW CONNECTION] {addr} connected.")
            '''
            while True:
                conn, addr = server.accept()
                clients.append((conn, addr))
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
                text = "\n[ACTIVE CONNECTIONS] " + str(threading.activeCount() - 2)
                self.server_txt.insert(END, str(text))'''

        def send_shares():
            self.server_txt.insert(END, "\nSending data ... \n")
            for i in range(0, 5):
                client = clients[i]
                c = clientSockets[i]

                client.shareKey = self.shares[i]
                client.shareOwnersAdresses = copy(clientAdresses)

                dataString = pickle.dumps(client)
                c.send(dataString)
                c.close()
            self.server_txt.insert(END, "Done\n")

        def active_connections():
            if threading.activeCount() >= 2:
                self.server_txt.insert(END, "\n[ACTIVE CONNECTIONS] " + str(threading.activeCount() - 2) + "\n")
                #for i in clients:
                    #txt = "Client no." + str(i + 1) + " : IP: " + repr(clients[i[0]]) + " | Port: " + repr(clients[i[1]])
                    #self.server_txt.insert(END, f"\n[{int(clients[i][0])}] \n")
            else:
                self.server_txt.insert(END, "\n[ACTIVE CONNECTIONS] 0\n")
            #print(clients)




    def sharing(self):
        share_input = self.input_txt.get().strip()
        if share_input == "":
            message("Warning", "Enter PIN first!")
        else:
            message_input = int(self.input_txt.get())
            self.shares = sss.generate_shares(5, 3, message_input)
            tmp = self.shares
            shares_str = "\n".join("\t\t\t" + str(share) for share in tmp)
            self.shares_txt.insert(END, shares_str)


    def reconstruction(self):
        new = Toplevel(self, bg=colors[0])
        new.title("Reconstruction")
        Label(new, text="Reconstruction", font=("BebasNeue-Regular", 15), bg=colors[1]).grid(row=0, columnspan=3, pady=10)
        Label(new, text="1: ", font=("BebasNeue-Regular", 12), bg=colors[1]).grid(row=1, column=0)
        Label(new, text="2: ", font=("BebasNeue-Regular", 12), bg=colors[1]).grid(row=2, column=0)
        Label(new, text="3: ", font=("BebasNeue-Regular", 12), bg=colors[1]).grid(row=3, column=0)
        Button(new, text="Reconstruct: ", font=("BebasNeue-Regular", 12), bg=colors[3], command=lambda: reconstruct()).grid(row=4, columnspan=3)
        Label(new, text="Reconstructed PIN", font=("BebasNeue-Regular", 12), bg=colors[1]).grid(row=5, columnspan=3, pady=10)
        e1 = Entry(new, width=30)
        e1.grid(row=1, column=1, pady=10, padx=5)
        e1_2 = Entry(new, width=30)
        e1_2.grid(row=1, column=2, pady=10, padx=5)
        e2 = Entry(new, width=30)
        e2.grid(row=2, column=1, pady=10, padx=5)
        e2_2 = Entry(new, width=30)
        e2_2.grid(row=2, column=2, pady=10, padx=5)
        e3 = Entry(new, width=30)
        e3.grid(row=3, column=1, pady=10, padx=5)
        e3_2 = Entry(new, width=30)
        e3_2.grid(row=3, column=2, pady=10, padx=5)
        recon_text = Text(new, height=16, width=50)
        recon_text.grid(row=6, columnspan=3, pady=15, padx=15)

        def reconstruct():
            shares = [(int(e1.get()), int(e1_2.get())), (int(e2.get()), int(e2_2.get())), (int(e3.get()), int(e3_2.get()))]
            out = sss.reconstruct_secret(shares)
            recon_text.delete("1.0", END)
            recon_text.insert(END, out)



def console_sending(message):
    output = SSSPage.get_server_txt()
    output.insert(END, message)


class RSAPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        rsaframe = Frame(self, bg=colors[0])
        rsaframe.pack(side="top", fill="both", expand=True)

        label = Label(rsaframe, text="RSA", font=("BebasNeue-Regular", 15), bg=colors[1])
        label.pack(side="top", fill="y", anchor=W, expand=False, pady=10, padx=20)

        input_txt = Text(rsaframe, height=12, width=30, bg=colors[2])
        input_txt.pack(side="top", fill="both", expand=True, pady=10, padx=10)

        key_btn = Button(rsaframe, text="Generate keys", font=("BebasNeue-Regular", 11), width=12,
                             bg=colors[4], command=lambda: generate_keys())
        key_btn.pack(side="top", expand=False, pady=5)

        encrypt_btn = Button(rsaframe, text="Encrypt", font=("BebasNeue-Regular", 11), width=12,
                             bg=colors[4], command=lambda: encrypt_rsa())
        encrypt_btn.pack(side="top", expand=False, pady=5)

        decrypt_btn = Button(rsaframe, text="Decrypt", font=("BebasNeue-Regular", 11), width=12,
                             bg=colors[4], command=lambda: decrypt_rsa())
        decrypt_btn.pack(side="top", expand=False, pady=5)

        output_rsa = Text(rsaframe, height=12, width=30, bg=colors[2])
        output_rsa.pack(side="top", fill="both", expand=True, pady=10, padx=10)

        def generate_keys():
            rsa.key_pair()
            message("Info", "Pair of keys saved to /RSA folder")

        def encrypt_rsa():
            key = ""
            msg = input_txt.get("1.0", END).strip()
            if msg != "":
                filename = filedialog.askopenfilename(initialdir="../RSA", title="Select a Key",
                                                      filetypes=(("pem files", "*.pem"), ("all files", "*.*")))
                with open(filename, "r") as f:
                    key = f.read()
                encrypted = rsa.RSA_Encrypt(msg, key)

                if output_rsa.get("1.0", END).strip():
                    output_rsa.forget()
                else:
                    output_rsa.insert(END, encrypted)
            else:
                message("Warning", "Enter the message first!")

        def decrypt_rsa():
            key = ""
            msg = input_txt.get("1.0", END).strip()
            if msg != "":
                filename = filedialog.askopenfilename(initialdir="../RSA", title="Select a Key",
                                                      filetypes=(("pem files", "*.pem"), ("all files", "*.*")))
                with open(filename, "r") as f:
                    key = f.read()
                decrypted = rsa.RSA_Decrypt(msg, key)

                if output_rsa.get("1.0", END).strip():
                    output_rsa.delete("1.0", END)
                else:
                    output_rsa.insert(END, decrypted)
            else:
                message("Warning", "Enter the message first!")


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = AlgoPage(self)
        p2 = SSSPage(self)
        p3 = RSAPage(self)

        container = Frame(self)
        mainframe = Frame(self, bg=colors[0])
        mainframe.pack(side="left", fill="both", anchor=N, expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        title = Label(mainframe, text="Cryptography Tool \n by Kacper Bojanowski & Filip Opilka",
                      font=("BebasNeue-Regular", 15), bg=colors[1])
        title.pack(side="top", fill="y", anchor=NW, pady=13, padx=10)

        # Instruction
        instruction = Label(mainframe, text="Choose an action:", font=("BebasNeue-Regular", 12), bg=colors[1])
        instruction.pack(side="top", fill="y", anchor=NW, pady=15, padx=10)

        algo_txt = StringVar()
        algo_txt.set("Algorithms")
        sss_txt = StringVar()
        sss_txt.set("sss")
        algo_btn = Button(mainframe, textvariable=algo_txt, font=("BebasNeue-Regular", 15),
                          bg=colors[3], height=4, width=16, command=p1.show)
        sss_btn = Button(mainframe, textvariable=sss_txt, font=("BebasNeue-Regular", 15),
                         bg=colors[3], height=4, width=16, command=p2.show)

        rsa_txt = StringVar()
        rsa_txt.set("RSA")
        rsa_btn = Button(mainframe, textvariable=rsa_txt, font=("BebasNeue-Regular", 15),
                         bg=colors[3], height=4, width=16, command=p3.show)

        algo_btn.pack(side="top", anchor=NW, pady=10, padx=10)
        rsa_btn.pack(side="top", anchor=NW, pady=10, padx=10)
        sss_btn.pack(side="top", anchor=NW, pady=10, padx=10)
        p1.show()


def message(title, text):
    return ctypes.windll.user32.MessageBoxW(0, text, title, 0)


if __name__ == "__main__":
    root = Tk()
    root.iconbitmap("Cryptoicon.ico")
    root.title("Simple Cryptography")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x800")
    root.mainloop()