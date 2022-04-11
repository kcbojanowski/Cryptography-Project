from tkinter import *


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class AlgoPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = Label(self, text="Algorithms", font=("BebasNeue-Regular", 15))
        label.pack(side="top", fill="y", expand=False, pady=10)

        options = ["Ceasar", "Playfair", "Vigenere"]
        algorithms = StringVar()
        algorithms.set(options[0])
        combo = OptionMenu(self, algorithms, *options)
        combo.pack(side="top", fill="y", expand=False)


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
    root.wm_geometry("800x600")
    root.mainloop()
