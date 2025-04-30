import threading
import time

import pyautogui
import keyboard
from PIL import Image
import os


def open_color_menu():
    pyautogui.click(50, 54)
    time.sleep(.5)


def enter_rgb():
    pyautogui.click(1024, 990)
    time.sleep(.5)


def close_color_menu():
    pyautogui.click(1416, 74)
    time.sleep(.5)


def select_color(color):
    open_color_menu()
    enter_rgb()
    if color == "cyan":
        keyboard.write("00ffff")
    elif color == "magenta":
        keyboard.write("ff00ff")
    elif color == "yellow":
        keyboard.write("ffff00")
    elif color == "key" or color == "black":
        keyboard.write("000000")
    elif color == "red":
        keyboard.write("ff0000")
    elif color == "blue":
        keyboard.write("0000ff")
    elif color == "green":
        keyboard.write("00ff00")
    else:
        raise ValueError(f"Value {color} not in colors")
    time.sleep(.5)
    # # Select opacity = 20
    # pyautogui.click(1133, 646)

    # Select opacity = 2
    pyautogui.click(1133, 732)
    time.sleep(.5)

    close_color_menu()


def open_tools_menu():
    pyautogui.click(52, 378)
    time.sleep(.5)


def select_brush():
    pyautogui.click(411, 234)
    time.sleep(.5)


def select_small():
    pyautogui.click(878, 999)
    time.sleep(.5)


def close_tools_menu():
    pyautogui.click(860, 84)
    time.sleep(.5)


def select_size(size):
    open_tools_menu()
    select_brush()
    select_small()
    close_tools_menu()


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


class Painter:
    def __init__(self, filename, mode="CYMK", scaledivisor=20, speed=False, cd=5):
        self.speed = speed
        self.cd = cd  # cd stands for color depth. The higher the number, the deeper the colors.
        self.done = False
        self.filename = filename
        self.mode = mode
        self.scaledivisor = scaledivisor
        self.img = Image.open(filename)
        self.img = self.img.convert(self.mode)
        if self.mode == "CMYK":
            self.img = gcr(self.img)

        # measured size of AJ art window
        self.width = 1320
        self.height = 1080

        self.img = self.img.resize((self.width // self.scaledivisor, self.height // self.scaledivisor))
        # self.pixel_matrix = self.img.load()
        self.pixel_matrix = {}
        loaded_img = self.img.load()
        self.x, self.y = self.img.size
        for x in range(self.x):
            for y in range(self.y):
                self.pixel_matrix[x, y] = list(loaded_img[x, y])
        print(self.x, self.y)
        self.drawpic()

    def drawpic(self):
        # select the size. TODO: reexpand this
        select_size(self.scaledivisor)

        # set up pause functionality
        global stop
        stop = False

        def stoppainter():
            global stop
            stop = True

        def startpainter():
            global stop
            stop = False

        keyboard.add_hotkey("]", stoppainter)
        keyboard.add_hotkey("[", startpainter)
        threading.Thread(target=keyboard.wait).start()

        '''
        alternate colors, subtracting 1 for each click until all pixel values are (0,0,0,0)
        '''

        # run until all color values are 0
        all_vals_are_0 = False
        while not all_vals_are_0:
            # hypothesize that this is the last run
            all_vals_are_0 = True
            # for each available color:
            for color, color_index_in_tuple in zip(getcolors(self.mode), range(len(getcolors(self.mode)))):
                select_color(color)

                # for every pixel
                for xval in range(self.x):
                    acted_this_y = False
                    drag_buffer_start_x = -1
                    drag_buffer_start_y = -1  # -1 if unused, positive otherwise
                    drag_buffer_size = 0
                    for yval in range(self.y):
                        pixel = self.pixel_matrix[xval, yval]
                        pixel_color_value = pixel[color_index_in_tuple]
                        if pixel_color_value > 0:
                            # get the pixel location
                            xloc = 360 + xval * self.width / self.x
                            yloc = yval * self.height / self.y

                            drag_buffer_size += self.height / self.y
                            if drag_buffer_start_y < 0:
                                drag_buffer_start_y = yloc
                                drag_buffer_start_x = xloc

                            self.pixel_matrix[xval, yval][color_index_in_tuple] -= max(int(256 / self.cd), 1)

                            # this never runs if everything is always 0
                            all_vals_are_0 = False
                            acted_this_y = True
                            while stop:
                                pass
                        elif drag_buffer_size > 0:
                            time.sleep(0.25)
                            pyautogui.moveTo(drag_buffer_start_x, drag_buffer_start_y)
                            pyautogui.mouseDown()
                            pyautogui.moveTo(drag_buffer_start_x, drag_buffer_start_y + drag_buffer_size)
                            pyautogui.mouseUp()
                            drag_buffer_start_y = -1
                            drag_buffer_size = 0
                            drag_buffer_start_x = -1
                            time.sleep(0.25)

                    # last drag check
                    if drag_buffer_size > 0:
                        time.sleep(0.25)
                        pyautogui.moveTo(drag_buffer_start_x, drag_buffer_start_y)
                        pyautogui.mouseDown()
                        pyautogui.moveTo(drag_buffer_start_x, drag_buffer_start_y + drag_buffer_size)
                        pyautogui.mouseUp()
                        time.sleep(0.25)

        os.system("start https://ko-fi.com/ajart_printer")
        exit(1)

