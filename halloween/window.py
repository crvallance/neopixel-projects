# CircuitPlaygroundExpress_NeoPixel

import board
import neopixel
import time
import random
import adafruit_fancyled.adafruit_fancyled as fancy

pixpin = board.D5
pixnum = 364
pixels = neopixel.NeoPixel(pixpin, pixnum, brightness=1, auto_write=False)
pixels.fill((0, 0, 0))
# pixels.show()
base_orange = fancy.CRGB(255, 140, 0.0)  # Orange
orange_adj_1 = fancy.gamma_adjust(base_orange, gamma_value=4.5)
dark_orage = orange_adj_1.pack()
base_purple = fancy.CRGB(0x10, 0, 0x10)
purple_adj_1 = fancy.gamma_adjust(base_purple, gamma_value=.75)
purp = purple_adj_1.pack()
r_window = range(1, 120 + 1)
c_window = range(121, 244 + 1)
l_window = range(245, 364 + 1)


def blank():
    black = (0, 0, 0)
    for i in range(0, pixnum):
        pixels[i] = black
    pixels.show()
    time.sleep(.5)


def green_fader():
    green_rgb = fancy.CRGB(34, 139, 34)
    inc = .5
    j = 10
    while True:
        if j > 2:
            print(j)
            j = j - inc
            print(j)
            color = fancy.gamma_adjust(green_rgb, gamma_value=j)
            green = color.pack()
            for i in range(len(pixels)):
                pixels[i] = green
            pixels.show()
        if j <= 2.1:
            print(j)
            color = fancy.gamma_adjust(green_rgb, gamma_value=j)
            green = color.pack()
            for i in range(len(pixels)):
                pixels[i] = green
            pixels.show()
            j += inc

'''
    for j in [10 - (x * .5) for x in range(0, 15, 3)]:
        print(j)
        color = fancy.gamma_adjust(green_rgb, gamma_value=j)
        green = color.pack()
        for i in range(len(pixels)):
            pixels[i] = green
        pixels.show()
    for k in [1 + (x * .5) for x in range(0, 15, 3)]:
        print(k)
        color = fancy.gamma_adjust(green_rgb, gamma_value=k)
        green = color.pack()
        for i in range(len(pixels)):
            pixels[i] = green
        pixels.show()
   '''


def marquee(wait, color=''):
    if not color:
        color = (0, 0, 0x10)
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
        pixels[item] = color
    for item in odds:
        pixels[item] = black
    pixels.show()
    time.sleep(wait)
    for item in evens:
        pixels[item] = black
    for item in odds:
        pixels[item] = color
    pixels.show()
    time.sleep(wait)


def simplechase(wait, color=''):
    if not color:
        color = (0, 0, 0x10)
    # red = 0x100000  # (0x10, 0, 0) also works
    # yellow = (0x10, 0x10, 0)
    # green = (0, 0x10, 0)
    # aqua = (0, 0x10, 0x10)
    # blue = (0, 0, 0x10)
    # color = fancy.CRGB(1.0, 0.3, 0.0)  # Orange
    # color1 = fancy.CRGB(255, 140, 0.0)  # Orange
    # color = fancy.gamma_adjust(color1, gamma_value=4.5)
    # purple = color.pack()
    # purple = (0x10, 0, 0x10)
    black = (0, 0, 0)
    # white = (0x10, 0x10, 0x10)
    for i in range(len(pixels)):
        pixels[i] = color
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


def marquee_loop(sleep=2, color=''):
    print('random color is: {}'.format(color))
    loops = 10
    for i in range(1, loops):
        if i < loops:
            print('marquee loop: {} of {}'.format(i, loops))
            marquee(sleep, color)
            i += 1
    blank()


def chase_loop(color=''):
    print('random color is: {}'.format(color))
    loops = 4
    for i in range(1, loops):
        if i < loops:
            print('chase loop: {} of {}'.format(i, loops))
            simplechase(.0005, color)
            i += 1
    blank()

# tricks = [shifter_loop, backandforth_loop, fill_the_glass_loop, circle_loop]
tricks = [chase_loop, marquee_loop] # noqa
colors = [dark_orage, purp]
while True:
    random.choice(tricks)(color=random.choice(colors))
