# CircuitPlaygroundExpress_NeoPixel

import board
import neopixel
import time
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
white = (255, 255, 255)
blue = (0, 0, 255)
r_window = range(1, 120 + 1)
c_window = range(121, 244 + 1)
l_window = range(245, 364 + 1)


def blank():
    black = (0, 0, 0)
    for i in range(0, pixnum):
        pixels[i] = black
    pixels.show()
    time.sleep(.5)


def marquee(wait, color=''):
    if not color:
        color = (0, 0, 0x10)
    black = (0, 0, 0)  # noqa: F841
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
        pixels[item] = white
    pixels.show()
    time.sleep(wait)
    for item in evens:
        pixels[item] = white
    for item in odds:
        pixels[item] = color
    pixels.show()
    time.sleep(wait)


def marquee_static(wait, color=''):
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
        pixels[item] = dark_orage
    for item in odds:
        pixels[item] = black
    pixels.show()
    time.sleep(wait)
    for item in evens:
        pixels[item] = black
    for item in odds:
        pixels[item] = purp
    pixels.show()
    time.sleep(wait)


while True:
    marquee(2, blue)
