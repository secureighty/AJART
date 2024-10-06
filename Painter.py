import time

import pyautogui
import keyboard
from PIL import Image
from math import floor


def select_color(color):
    pyautogui.click(53, 31)
    time.sleep(1)
    if color == "cyan":
        pyautogui.click(198, 193)
    elif color == "magenta":
        pyautogui.click(198, 286)
    elif color == "yellow":
        pyautogui.click(198, 101)
    elif color == "key" or color == "black":
        pyautogui.click(131, 354)
    elif color == "red":
        pyautogui.click(457, 165)
    elif color == "blue":
        pyautogui.click(457, 409)
    elif color == "green":
        pyautogui.click(457, 695)
    else:
        raise ValueError(f"Value {color} not in colors")
    time.sleep(1)
    pyautogui.click(1108, 60)
    time.sleep(1)


def select_size(size):
    pyautogui.click(53, 516)
    time.sleep(1)
    if size <= 3:
        pyautogui.click(172, 866)
    elif size <= 7:
        pyautogui.click(265, 866)
    elif size <= 13:
        pyautogui.click(172, 917)
    elif size <= 20:
        pyautogui.click(265, 917)
    elif size <= 40:
        pyautogui.click(172, 980)
    else:
        pyautogui.click(265, 980)
    time.sleep(1)


def gcr(im):
    """
    Basic "Gray Component Replacement" function. Returns a CMYK image with
    percentage gray component removed from the CMY channels and put in the
    K channel, ie. for percentage=100, (41, 100, 255, 0) >> (0, 59, 214, 41)
    """
    cmyk_im = im.split()
    cmyk = []
    for i in range(4):
        cmyk.append(cmyk_im[i].load())
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            gray = int(
                min(cmyk[0][x, y], cmyk[1][x, y], cmyk[2][x, y])
            )
            for i in range(3):
                cmyk[i][x, y] = cmyk[i][x, y] - gray
            cmyk[3][x, y] = gray
    return Image.merge("CMYK", cmyk_im)


def getcolors(mode):
    if mode == "CMYK":
        return ["cyan", "magenta", "yellow", "key"]
    elif mode == "L":
        return ["black"]
    elif mode == "RGB":
        return ["red", "green", "blue"]


def click(xloc, yloc, speed):
    if speed:
        pyautogui.click(xloc, yloc)
    else:
        pyautogui.moveTo(xloc, yloc)
        pyautogui.mouseDown()
        pyautogui.mouseUp()


class Painter:
    def __init__(self, filename, mode, scaledivisor, speed, cd):
        self.speed = speed
        self.cd = cd
        self.done = False
        self.filename = filename
        self.mode = mode
        self.scaledivisor = scaledivisor
        self.img = Image.open(filename)
        self.img = self.img.convert(self.mode)
        if self.mode == "CMYK":
            self.img = gcr(self.img)
        self.width = 1380
        self.height = 850
        self.img = self.img.resize((self.width // self.scaledivisor, self.height // self.scaledivisor))
        self.pix = self.img.load()
        self.x, self.y = self.img.size
        print(self.x, self.y)
        self.img.show()
        keyboard.add_hotkey("[", self.drawpic)

    def drawpic(self):
        pyautogui.click(176, 699)
        time.sleep(1)
        select_size(self.scaledivisor)

        keyboard.unhook_all_hotkeys()
        stop = False
        counter = 0
        for color in getcolors(self.mode):
            if stop:
                while not keyboard.is_pressed("["):
                    pass
                stop = False
                print("unstopped")
            select_color(color)
            for xval in range(self.x):
                if stop:
                    while not keyboard.is_pressed("["):
                        pass
                    stop = False
                    print("unstopped")
                for yval in range(self.y):
                    if stop:
                        while not keyboard.is_pressed("["):
                            pass
                        stop = False
                        print("unstopped")
                    xloc = 350 + xval * self.width / self.x
                    yloc = 110 + yval * self.height / self.y
                    px = self.pix[xval, yval]
                    print(px)
                    if type(px) != int:
                        pixel = px[counter]
                    else:
                        pixel = 256 - px
                    pixmult = floor(pixel * self.cd / 256)

                    for i in range(pixmult):
                        click(xloc, yloc, self.speed)
                    if keyboard.is_pressed("]"):
                        stop = True
            counter += 1
        self.done = True
