from tkinter import *
import Algorithms.Vigenere as vigenere
import Algorithms.Playfair as playfair
import Algorithms.Caesar as caesar


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
        label.pack(side="top", fill="y", anchor=E, expand=False, pady=10)

        options = ["Ceasar", "Playfair", "Vigenere"]
        algorithms = StringVar()
        algorithms.set(options[0])
        combo = OptionMenu(algoframe, algorithms, *options)
        combo.pack(side="top", fill="y", anchor=E, expand=False)

        if algorithms.get() == "Ceasar":
            crack_btn = Button(algoframe, text="Break", font=("BebasNeue-Regular", 11), width=12, height=15,
                               command=lambda: break_ceasar())
            crack_btn.pack(side="right", anchor=W, expand=False, pady=5, padx=10)

        input_txt = Text(algoframe, height=12, width=30, bg="#CEF3EF")
        input_txt.pack(side="top", fill="both", expand=True, pady=10)

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

        output = Text(algoframe, height=12, width=30, bg="#F3CED8")
        output.pack(side="top", fill="both", expand=True, pady=10)

        def encrypt():
            current_algo = algorithms.get()
            message_input = input_txt.get("1.0", END)
            key_input = key_txt.get()

            if current_algo == "Playfair":
                out = playfair.Encrypt_Playfair(message_input, key_input)
                output.insert("1.0", out)

            if current_algo == "Vigenere":
                out = vigenere.Encrypt_Vigenere(message_input, key_input)
                output.insert(END, out)

            if current_algo == "Ceasar":
                out = caesar.caesar_encrypt(message_input, int(key_input))
                output.insert(END, out)

        def decrypt():
            current_algo = algorithms.get()
            message_input = input_txt.get("1.0", END).strip()

            key_input = key_txt.get().strip()

            if current_algo == "Playfair":
                out = playfair.Decrypt_Playfair(message_input, key_input)
                output.insert(END, out)

            if current_algo == "Vigenere":
                out = vigenere.Decrypt_Vigenere(message_input, key_input)
                output.insert(END, out)

            if current_algo == "Ceasar":
                out = caesar.caesar_decrypt(message_input, int(key_input))
                output.insert(END, out)

        def break_ceasar():
            print("hi")
class SSSPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="SSS", font=("BebasNeue-Regular", 12))
        label.pack(side="top", fill="both", expand=True)


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = AlgoPage(self)
        p2 = SSSPage(self)

        container = Frame(self)
        mainframe = Frame(self)
        mainframe.pack(side="left", fill="x", anchor=N, expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        title = Label(mainframe, text="Cryptography Tool \n by Kacper Bojanowski & Filip Opilka",
                      font=("BebasNeue-Regular", 15))
        title.pack(side="top", fill="y",  anchor=NW, pady=13, padx=10)

        # Instruction
        instruction = Label(mainframe, text="Choose an action:", font=("BebasNeue-Regular", 12))
        instruction.pack(side="top",fill="y", anchor=NW, pady=15, padx=10)

        algo_txt = StringVar()
        algo_txt.set("Algorithms")
        sss_txt = StringVar()
        sss_txt.set("sss")
        algo_btn = Button(mainframe, textvariable=algo_txt, font=("BebasNeue-Regular", 15),
                          height=5, width=16, command=p1.show)
        sss_btn = Button(mainframe, textvariable=sss_txt, font=("BebasNeue-Regular", 15),
                         height=5, width=16, command=p2.show)

        algo_btn.pack(side="top",anchor=NW, pady=10, padx=10)
        sss_btn.pack(side="top", anchor=NW, pady=10, padx=10)

        p1.show()


if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x800")
    root.mainloop()
