import time
import tkinter
import tkinter.messagebox
import tkinter.font
from tkinter import *
from tkinter import filedialog
import Painter
import webbrowser
import threading


class AJArt_Gui:
    def __init__(self):
        self.win = Tk()
        self.win.iconphoto(False, tkinter.PhotoImage(file="ajarticon.png"))
        self.win.title('Animal Jam Art Printer')
        self.file_path = None
        self.mode = StringVar(self.win, "CMYK")
        self.speed = BooleanVar(self.win, True)
        self.scaling_factor = IntVar(self.win, 10)
        self.cd = IntVar(self.win, 20)
        self.p = None
        topframe = Frame(self.win, relief=RAISED)
        topframe.pack(fill="both", expand=True)
        pad = 50
        topframe.grid_rowconfigure(1, weight=1, pad=pad)
        topframe.grid_columnconfigure(1, weight=1, pad=pad)
        topframe.grid_rowconfigure(0, weight=1, pad=pad)
        topframe.grid_columnconfigure(0, weight=1, pad=pad)

        ###SELECT IMAGE BUTTON###
        select_image_button = Button(topframe, text="Select Image", width=20, height=5, command=self.select_image)
        select_image_button.grid(row=0, column=0)

        ###MODE SELECT###
        modes_frame = Frame(topframe)
        select_mode_message = Message(modes_frame, text="------Select Mode------", width=300)
        select_mode_message.pack()
        mode_dict = {"CMYK": "CMYK", "L": "Grayscale"}
        for mode in mode_dict.keys():
            Radiobutton(modes_frame, text=mode_dict[mode], value=mode, var=self.mode).pack()
        modes_frame.grid(row=0, column=1)

        ###DOTSIZE SELECT###
        ds_frame = Frame(topframe)
        select_ds_message = Message(ds_frame, text="------Select Dot Size------", width=300)
        select_ds_message.pack()
        ds_dict = {5: "Tiny", 10: "Small", 20: "Medium", 30: "Large", 40: "Very Large", 60: "Gigantic"}
        for ds in ds_dict.keys():
            Radiobutton(ds_frame, text=ds_dict[ds], value=ds, var=self.scaling_factor).pack()
        ds_frame.grid(row=1, column=0)

        ###LOAD BUTTON###
        self.load_button = Button(self.win, text="Load", width=20, height=5, command=self.load)
        self.load_button.pack()

        ###SPEED SELECT###
        speed_frame = Frame(topframe)
        select_speed_message = Message(speed_frame, text="------Select Speed------", width=300)
        select_speed_message.pack()
        speed_dict = {True: "Fast", False: "Accurate (No Glitches)"}
        for speed in speed_dict.keys():
            Radiobutton(speed_frame, text=speed_dict[speed], value=speed, var=self.speed).pack()
        speed_frame.grid(row=1, column=1)

        ###COLOR DEPTH SELECT###
        cd_frame = Frame(topframe)
        select_cd_message = Message(cd_frame, text="------Select Color Depth------", width=300)
        select_cd_message.pack()
        cd_dict = {20: "Standard", 25: "Deep"}
        for cd in cd_dict.keys():
            Radiobutton(cd_frame, text=cd_dict[cd], value=cd, var=self.cd).pack()
        cd_frame.grid(row=2, column=1)

        ###BOTTOM MESSAGE###
        my_font = tkinter.font.Font(size=18)
        controls_message = Message(self.win, text="Once Loaded, Press '[' to start, and ']' to pause",
                                   width=550, font=my_font)
        controls_message.pack(fill="both", expand=True)

        self.win.mainloop()

    def select_image(self):
        self.file_path = filedialog.askopenfilename()

    def load(self):
        if not self.file_path is None:
            self.load_button.pack_forget()
            threading.Thread(target=self.loadthread, daemon=True).start()
        else:
            tkinter.messagebox.showerror("Error", "No Image Selected.")

    def loadthread(self):
        self.p = Painter.Painter(self.file_path, self.mode.get(), self.scaling_factor.get(), self.speed.get(),
                                 self.cd.get())
        threading.Thread(target=self.thanks, daemon=True).start()

    def thanks(self):
        while self.p.done is False:
            time.sleep(1)
        result = tkinter.messagebox.askquestion("Thank you",
                                                "Thanks for using AJART Printer! Was your print worth supporting me "
                                                "for 5$?")
        if result == "yes":
            webbrowser.open("https://paypal.me/AedanETaylor")
        exit(0)


if __name__ == "__main__":
    main = AJArt_Gui()
