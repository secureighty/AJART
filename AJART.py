import tkinter
import tkinter.messagebox
import tkinter.font
from tkinter import *
from tkinter import filedialog

import win32con

import Painter
import threading

import win32gui
import re


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)


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
        self.topframe = Frame(self.win, relief=RAISED)
        self.topframe.pack(fill="both", expand=True)
        pad = 50
        self.topframe.grid_rowconfigure(1, weight=1, pad=pad)
        self.topframe.grid_columnconfigure(1, weight=1, pad=pad)
        self.topframe.grid_rowconfigure(0, weight=1, pad=pad)
        self.topframe.grid_columnconfigure(0, weight=1, pad=pad)

        ###SELECT IMAGE BUTTON###
        select_image_button = Button(self.topframe, text="Select Image", width=20, height=5, command=self.select_image)
        select_image_button.grid(row=0, column=0)

        ###LOAD BUTTON###
        self.load_button = Button(self.topframe, text="Start", width=20, height=5, command=self.load)
        self.load_button.grid(row=0, column=1)

        ###BOTTOM MESSAGE###
        my_font = tkinter.font.Font(size=18)
        controls_message = Message(self.win, text="While running,\npress '[' to start,\nand ']' to pause",
                                   width=550, font=my_font)
        controls_message.pack(fill="both", expand=True)

        self.win.mainloop()

    def select_image(self):
        self.file_path = filedialog.askopenfilename()

    def load(self):
        if self.file_path is not None:
            self.topframe.pack_forget()
            self.load_button.pack_forget()
            w = WindowMgr()
            w.find_window_wildcard("Animal Jam")
            w.set_foreground()
            threading.Thread(target=self.loadthread, daemon=True).start()
        else:
            tkinter.messagebox.showerror("Error", "No Image Selected.")

    def loadthread(self):
        thiswindow = win32gui.FindWindow(None, "Animal Jam Art Printer")
        win32gui.SetWindowPos(thiswindow, win32con.HWND_TOPMOST, 1680, 0, 240, 240, 0)
        self.p = Painter.Painter(self.file_path, self.mode.get(), self.scaling_factor.get())


if __name__ == "__main__":
    main = AJArt_Gui()
