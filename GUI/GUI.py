from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Algorithms.Vigenere as Vigenere
import Algorithms.Playfair as Playfair
import Algorithms.Caesar as Caesar
import Algorithms.Plots as Plots
import RSA.RSA as rsa



class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class AlgoPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        algoframe = Frame(self)
        algoframe.pack(side="top", fill="both", expand=True)

        label = Label(algoframe, text="Algorithms", font=("BebasNeue-Regular", 15))
        label.pack(side="top", fill="y", anchor=NE, expand=False, pady=30, padx=30)

        instr = Label(algoframe, text="Choose an algorithm:", font=("BebasNeue-Regular", 13))
        instr.pack(side="top", fill="y", anchor=NE, expand=False, padx=30)

        options = ["Ceasar", "Playfair", "Vigenere"]
        algorithms = StringVar()
        algorithms.set(options[0])

        def callback(*args):
            if algorithms.get() != "Ceasar":
                crack_btn.pack_forget()
            else:
                crack_btn.pack(side="left", anchor=W, expand=False, pady=5, padx=10)

        algorithms.trace("w", callback)
        combo = OptionMenu(algoframe, algorithms, *options)

        combo.pack(side="top", fill="y", anchor=NE, expand=False, padx=30)

        crack_btn = Button(algoframe, text="Break", font=("BebasNeue-Regular", 11), width=12, height=15,
                           command=lambda: break_ceasar())
        crack_btn.pack(side="left", anchor=W, expand=False, pady=5, padx=10)

        freq_btn = Button(algoframe, text="Letter plots", font=("BebasNeue-Regular", 11), width=12, height=15,
                           command=lambda: plots())
        freq_btn.pack(side="right", anchor=W, expand=False, pady=5, padx=10)

        input_txt = Text(algoframe, height=12, width=30, bg="white")
        input_txt.pack(side="top", fill="y", expand=True, pady=10)

        key_label = Label(algoframe, text="enter key:", font=("BebasNeue-Regular", 12))
        key_label.pack(side="top", expand=False)

        key_txt = Entry(algoframe)
        key_txt.pack(side="top", fill="y", expand=False, pady=10)

        encrypt_btn = Button(algoframe, text="encrypt", font=("BebasNeue-Regular", 11), width=12,
                             command=lambda: encrypt())
        encrypt_btn.pack(side="top", expand=False, pady=5)

        decrypt_btn = Button(algoframe, text="decrypt", font=("BebasNeue-Regular", 11), width=12,
                             command=lambda: decrypt())
        decrypt_btn.pack(side="top", expand=False, pady=5)

        output = Text(algoframe, height=12, width=30, bg="white")
        output.pack(side="top", fill="y", expand=True, pady=10)



        def encrypt():
            current_algo = algorithms.get()
            message_input = input_txt.get("1.0", END)
            key_input = key_txt.get()

            if current_algo == "Playfair":
                out = Playfair.Encrypt_Playfair(message_input, key_input)
                output.insert("1.0", out)

            if current_algo == "Vigenere":
                out = Vigenere.Encrypt_Vigenere(message_input, key_input)
                output.insert(END, out)

            if current_algo == "Ceasar":
                out = Caesar.caesar_encrypt(message_input, int(key_input))
                output.insert(END, out)

        def decrypt():
            current_algo = algorithms.get()
            message_input = input_txt.get("1.0", END).strip()

            key_input = key_txt.get().strip()

            if current_algo == "Playfair":
                out = Playfair.Decrypt_Playfair(message_input, key_input)
                output.insert(END, out)

            if current_algo == "Vigenere":
                out = Vigenere.Decrypt_Vigenere(message_input, key_input)
                output.insert(END, out)

            if current_algo == "Ceasar":
                out = Caesar.caesar_decrypt(message_input, int(key_input))
                output.insert(END, out)

        def break_ceasar():
            print("hi")

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
        label = Label(self, text="SSS", font=("BebasNeue-Regular", 12))
        label.pack(side="top", fill="both", expand=True)


class RSAPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        rsaframe = Frame(self)
        rsaframe.pack(side="top", fill="both", expand=True)

        label = Label(rsaframe, text="RSA", font=("BebasNeue-Regular", 15))
        label.pack(side="top", fill="y", anchor=W, expand=False, pady=10, padx=20)

        input_txt = Text(rsaframe, height=12, width=30, bg="white")
        input_txt.pack(side="top", fill="both", expand=True, pady=10, padx=10)

        encrypt_btn = Button(rsaframe, text="Generate keys", font=("BebasNeue-Regular", 11), width=12,
                             command=lambda: generate_keys())
        encrypt_btn.pack(side="top", expand=False, pady=5)

        decrypt_btn = Button(rsaframe, text="Encrypt", font=("BebasNeue-Regular", 11), width=12,
                             command=lambda: encrypt_rsa())
        decrypt_btn.pack(side="top", expand=False, pady=5)

        output_rsa = Text(rsaframe, height=12, width=30, bg="white")
        output_rsa.pack(side="top", fill="both", expand=True, pady=10, padx=10)

        def generate_keys():
            rsa.key_pair()

        def encrypt_rsa():
            key = ""
            msg = input_txt.get("1.0", END).strip()
            filename = filedialog.askopenfilename(initialdir="../RSA", title="Select a Key",
                                                  filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
            with open(filename, "r") as f:
                key = f.read()
            encrypted = rsa.RSA_Encrypt(msg, key)

            if output_rsa.get("1.0", END).strip():
                output_rsa.forget()
            else:
                output_rsa.insert(END, encrypted)


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = AlgoPage(self)
        p2 = SSSPage(self)
        p3 = RSAPage(self)

        container = Frame(self)
        mainframe = Frame(self)
        mainframe.pack(side="left", fill="x", anchor=N, expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        title = Label(mainframe, text="Cryptography Tool \n by Kacper Bojanowski & Filip Opilka",
                      font=("BebasNeue-Regular", 15))
        title.pack(side="top", fill="y", anchor=NW, pady=13, padx=10)

        # Instruction
        instruction = Label(mainframe, text="Choose an action:", font=("BebasNeue-Regular", 12))
        instruction.pack(side="top", fill="y", anchor=NW, pady=15, padx=10)

        algo_txt = StringVar()
        algo_txt.set("Algorithms")
        sss_txt = StringVar()
        sss_txt.set("sss")
        algo_btn = Button(mainframe, textvariable=algo_txt, font=("BebasNeue-Regular", 15),
                          height=4, width=16, command=p1.show)
        sss_btn = Button(mainframe, textvariable=sss_txt, font=("BebasNeue-Regular", 15),
                         height=4, width=16, command=p2.show)

        rsa_txt = StringVar()
        rsa_txt.set("RSA")
        rsa_btn = Button(mainframe, textvariable=rsa_txt, font=("BebasNeue-Regular", 15),
                         height=4, width=16, command=p3.show)

        algo_btn.pack(side="top", anchor=NW, pady=10, padx=10)
        rsa_btn.pack(side="top", anchor=NW, pady=10, padx=10)
        sss_btn.pack(side="top", anchor=NW, pady=10, padx=10)

        p1.show()


if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x800")
    root.mainloop()
