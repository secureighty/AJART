import time

import pyautogui
import keyboard
from PIL import Image
from math import floor
from PIL.Image import Resampling


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


def select_color_CYMK(color):
    # 1=cyan, 2=magenta, 3=yellow, 4=key
    pyautogui.click(53, 31)
    color = color + 1
    time.sleep(1)
    if color == 1:
        pyautogui.click(457, 510)
    elif color == 2:
        pyautogui.click(457, 820)
    elif color == 3:
        pyautogui.click(457, 327)
    elif color == 4:
        pyautogui.click(1000, 930)
    time.sleep(1)
    pyautogui.click(1108, 60)


def select_color_RGB(color):
    # 1=r, 2=g, 3=b, 4=a
    pyautogui.click(53, 31)
    color = color + 1
    time.sleep(.5)
    if color == 1:
        pyautogui.click(457, 165)
    elif color == 2:
        pyautogui.click(457, 409)
    elif color == 3:
        pyautogui.click(457, 695)
    time.sleep(.5)
    pyautogui.click(1108, 60)

def select_color_B(color):
    # 1=r, 2=g, 3=b, 4=a
    pyautogui.click(53, 31)
    color = color + 1
    time.sleep(.5)
    if color == 1:
        pyautogui.click(1000, 930)
    time.sleep(.5)
    pyautogui.click(1108, 60)


filename = input("filename: ")
# filename = "C:/users/ataylor/pictures/AJAT.png"
scaledivisor = 10
img = Image.open(filename)
img = img.convert("L")
#img = gcr(img)
img = img.resize((1320 // scaledivisor, 1080 // scaledivisor))

pix = img.load()
x, y = img.size
img.show()
width = 1320
height = 1080


def click(xloc, yloc):
    pyautogui.click(xloc, yloc)


def drawpic(x=x, y=y, width=width, height=height, colorrange=16):
    stop = False
    for color in range(3):
        if stop:
            while not keyboard.is_pressed("="):
                pass
            stop = False
            print("unstopped")
        select_color_RGB(color)
        for xval in range(x):
            if stop:
                while not keyboard.is_pressed("="):
                    pass
                stop = False
                print("unstopped")
            for yval in range(y):
                if stop:
                    while not keyboard.is_pressed("="):
                        pass
                    stop = False
                    print("unstopped")
                xloc = 360 + xval * width / x
                yloc = yval * height / y
                if color == 1:
                    xloc += width / x / 2
                if color == 2:
                    yloc += height / y / 2
                px = pix[xval, yval]
                print(px)
                pixel = px[color]
                pixmult = floor(pixel * colorrange / 256)
                if not keyboard.is_pressed("]"):
                    for i in range(pixmult):
                        click(xloc, yloc)
                        if color == 1:
                            yloc += width / x / 2
                            click(xloc, yloc)
                else:
                    stop = True


def drawpicCYMK(x=x, y=y, width=width, height=height, colorrange=16):
    stop = False
    for color in range(4):
        if stop:
            while not keyboard.is_pressed("="):
                pass
            stop = False
            print("unstopped")
        select_color_CYMK(color)
        for xval in range(x):
            if stop:
                while not keyboard.is_pressed("="):
                    pass
                stop = False
                print("unstopped")
            for yval in range(y):
                if stop:
                    while not keyboard.is_pressed("="):
                        pass
                    stop = False
                    print("unstopped")
                xloc = 360 + xval * width / x
                yloc = yval * height / y
                if color == 1:
                    xloc += width / x / 2
                if color == 2:
                    yloc += height / y / 2
                if color == 3:
                    yloc += height / y / 2
                    xloc += width / x / 2
                px = pix[xval, yval]
                print(px)
                pixel = px[color]
                pixmult = floor(pixel * colorrange / 256)
                if not keyboard.is_pressed("]"):
                    for i in range(pixmult):
                        click(xloc, yloc)
                else:
                    stop = True



def drawpicBW(x=x, y=y, width=width, height=height, colorrange=10):
    color = 0
    stop = False
    if stop:
        while not keyboard.is_pressed("="):
            pass
        stop = False
        print("unstopped")
    select_color_B(color)
    for xval in range(x):
        if stop:
            while not keyboard.is_pressed("="):
                pass
            stop = False
            print("unstopped")
        for yval in range(y):
            if stop:
                while not keyboard.is_pressed("="):
                    pass
                stop = False
                print("unstopped")
            xloc = 360 + xval * width / x
            yloc = yval * height / y
            if color == 1:
                xloc += width / x / 2
            if color == 2:
                yloc += height / y / 2
            if color == 3:
                yloc += height / y / 2
                xloc += width / x / 2
            px = pix[xval, yval]
            print(px)
            pixel = 256 - px
            pixmult = floor(pixel * colorrange / 256)
            if not keyboard.is_pressed("]"):
                for i in range(pixmult):
                    click(xloc, yloc)
            else:
                stop = True


keyboard.add_hotkey("[", drawpicBW)
keyboard.wait()
