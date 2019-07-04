import time
import board
import neopixel
import random

pixpin = board.D5
pixnum = 364
pixels = neopixel.NeoPixel(pixpin, pixnum, brightness=1, auto_write=False)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)

r_window = range(0, 120)
c_window = range(120, 244)
l_window = range(244, 364)


def color_chase(color, wait):
    for i in range(pixnum):
        pixels[i] = color
        # time.sleep(wait)
        pixels.show()
    # time.sleep(0.5)


def solid_fill(sleepy=2):
    print('solid fill')
    pixels.fill(RED)
    pixels.show()
    # Increase or decrease to change the speed of the solid color change.
    time.sleep(sleepy)
    pixels.fill(WHITE)
    pixels.show()
    time.sleep(sleepy)
    pixels.fill(BLUE)
    pixels.show()
    time.sleep(sleepy)


def patriot_chase(sleepy=0.1):
    print('partiot chase')
    color_chase(RED, sleepy)
    color_chase(WHITE, sleepy)
    color_chase(BLUE, sleepy)


def set_window(winrange, color=BLACK):
    sloppy_calc = []
    for i in winrange:
        pixels[i] = color
        sloppy_calc.append(i)
    # print(max(sloppy_calc))
    if max(sloppy_calc) == 119:
        print('left window')
    elif max(sloppy_calc) == 243:
        print('center window')
    elif max(sloppy_calc) == 363:
        print('right window')


def three_pane_solid(sleepy=5):
    print('three pane solid')
    set_window(r_window, color=RED)
    set_window(c_window, color=WHITE)
    set_window(l_window, color=BLUE)
    pixels.show()
    time.sleep(sleepy)


def three_pane_shift(sleepy=5, shift=12):
    print('three pane shift, total {}'.format(shift))
    colors = [RED, WHITE, BLUE]
    set_window(r_window, color=colors[0])
    set_window(c_window, color=colors[1])
    set_window(l_window, color=colors[2])
    pixels.show()
    time.sleep(sleepy)
    for n in range(1, shift):
        print('shift {}'.format(n))
        shifted = (colors[len(colors) - n:len(colors)] + colors[0:len(colors) - n]) # noqa
        set_window(r_window, color=shifted[0])
        set_window(c_window, color=shifted[1])
        set_window(l_window, color=shifted[2])
        pixels.show()
        time.sleep(sleepy)


tricks = [solid_fill(), patriot_chase(), three_pane_solid(), three_pane_shift()] # noqa
while True:
    # solid_fill(sleepy=2)
    # patriot_chase(sleepy=0.01)
    # three_pane_solid()
    # three_pane_shift()
    random.choice(tricks)
