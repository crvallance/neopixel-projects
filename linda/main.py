# CircuitPlaygroundExpress_NeoPixel

import board
import neopixel
import time
import random

pixpin = board.D1
pixnum = 20
pixels = neopixel.NeoPixel(pixpin, pixnum, brightness=.5, auto_write=False)
pixels.fill((0, 0, 0))
# pixels.show()


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 85:
        return (int(pos * 3), int(255 - (pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - (pos * 3)), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))


def back_and_forth(wait):
    purple = (0x10, 0, 0x10)
    black = (0, 0, 0)
    for i in range(len(pixels)):
        pixels[i] = purple
        pixels.show()
        time.sleep(wait)
        pixels[i] = black
        pixels.show()
        time.sleep(wait)
    time.sleep(1)

    for i in range(len(pixels)):
        pixels[pixnum - 1 - i] = purple
        pixels.show()
        time.sleep(wait)
        pixels[pixnum - 1 - i] = black
        pixels.show()
        time.sleep(wait)
    time.sleep(1)


def blank():
    black = (0, 0, 0)
    for i in range(0, pixnum):
        pixels[i] = black
    pixels.show()
    time.sleep(.5)


def shifter(wait):
    purple = (0x10, 0, 0x10)
    black = (0, 0, 0)
    evens = []
    odds = []
    for num in range(pixnum):
        # Test if the number is even
        if num % 2 == 0:
            evens.append(num)
        else:
            odds.append(num)
    for item in evens:
        pixels[item] = purple
    for item in odds:
        pixels[item] = black
    pixels.show()
    time.sleep(wait)
    for item in evens:
        pixels[item] = black
    for item in odds:
        pixels[item] = purple
    pixels.show()
    time.sleep(wait)


def fill_the_glass(wait):
    purple = (0x10, 0, 0x10)
    black = (0, 0, 0)
    lit_array = []
    for i in range(pixnum):
        # print('lit array is: {}'.format(lit_array))
        if lit_array:
            for led in lit_array:
                # print('made it in here with {} as type {}'.format(led, type(led))) # noqa
                pixels[led - 1] = purple
        pixels.show()
        # print('i is {}'.format(i))
        for j in range(pixnum):
            # print('j is {}'.format(j))
            if j < pixnum - i - 1:
                pixels[j] = purple
                pixels.show()
                time.sleep(wait)
                pixels[j] = black
                pixels.show()
                time.sleep(wait)
                # print(pixnum - i)
        lit_array.append(pixnum - i)
        time.sleep(wait)


def simplecircle(wait):
    # red = 0x100000  # (0x10, 0, 0) also works
    # yellow = (0x10, 0x10, 0)
    # green = (0, 0x10, 0)
    # aqua = (0, 0x10, 0x10)
    # blue = (0, 0, 0x10)
    purple = (0x10, 0, 0x10)
    black = (0, 0, 0)
    # white = (0x10, 0x10, 0x10)
    for i in range(len(pixels)):
        pixels[i] = purple
        pixels.show()
        time.sleep(wait)
    time.sleep(1)
    '''
    for i in range(len(pixels)):
        pixels[i] = white
        time.sleep(wait)
    time.sleep(1)
    '''
    for i in range(len(pixels)):
        pixels[i] = black
        pixels.show()
        time.sleep(wait)
    time.sleep(1)


def shifter_loop():
    loops = 2
    for i in range(1, loops):
        if i < loops:
            print(i)
            print(loops)
            shifter(2)
            i += 1
    blank()


def backandforth_loop():
    loops = 2
    for i in range(1, loops):
        if i < loops:
            print(i)
            print(loops)
            back_and_forth(.125)
            i += 1
    blank()


def fill_the_glass_loop():
    sleep_val = float(.125)
    for trial in range(1, 7):
        fill_the_glass(sleep_val)
        # print('sleep val is {}'.format(sleep_val))
        sleep_val = sleep_val / 2.5
    blank()


def circle_loop():
    loops = 2
    for i in range(1, loops):
        if i < loops:
            print(i)
            print(loops)
            simplecircle(.05)
            i += 1

tricks = [shifter_loop, backandforth_loop, fill_the_glass_loop, circle_loop]

while True:
    random.choice(tricks)()
