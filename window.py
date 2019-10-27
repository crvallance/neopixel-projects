import time
import random
import sys

# Some static stuff
# Colors
orange = (164.64062, 38.14844, 2.00781)
purple = (36.14062, 4.01562, 51.19922)
black = (6.02344, 6.02344, 6.02344)
off = (0, 0, 0)
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
# white = (0x10, 0x10, 0x10)
# Pixel info
pixnum = 364
r_window = range(1, 120 + 1)
c_window = range(121, 244 + 1)
l_window = range(245, 364 + 1)

fo = open("/dev/rpmsg_pru30", "w")

def paintSingleColor(color):
    r, g, b = color
    for i in range(0, 364):
        fo.write("%d %d %d %d\n" % (i, r, g, b))
        fo.flush()
    fo.write("-1 0 0 0\n")

def paintPositions(pixel_list, color_tup, push=False):
    r, g, b = color_tup
    for item in pixel_list:
        fo.write("%d %d %d %d\n" % (item, r, g, b))
        fo.flush()
    if push == True:
        fo.write("-1 0 0 0\n")
        fo.flush()

def marquee(wait, color=()):
    if not color:
        color = (0, 0, 0x10)
    evens = []
    odds = []
    for num in range(pixnum):
        # Test if the number is even
        if num % 2 == 0:
            evens.append(num)
        else:
            odds.append(num)
    paintPositions(evens, color)
    paintPositions(odds, off)
    fo.write("-1 0 0 0\n")
    fo.flush()
    time.sleep(wait)
    paintPositions(evens, off)
    paintPositions(odds, color)
    fo.write("-1 0 0 0\n")
    fo.flush()
    time.sleep(wait)


def simplechase(wait=0, color=()):
    paintSingleColor(off)
    if not color:
        color = (0, 0, 0x10)
    for i in range(pixnum):
        paintPositions([i], color, push=True)
        time.sleep(wait)
    for i in range(pixnum):
        paintPositions([i], off, push=True)
        time.sleep(wait)


def marquee_loop(sleep=2, color=()):
    # print('random color is: {}'.format(color))
    loops = 10
    for i in range(1, loops):
        if i < loops:
            print('marquee loop: {} of {}'.format(i, loops))
            marquee(sleep, color)
            i += 1
    paintSingleColor(off)

def chase_loop(color=()):
    # print('random color is: {}'.format(color))
    loops = 4
    for i in range(1, loops):
        if i < loops:
            print('chase loop: {} of {}'.format(i, loops))
            simplechase(.0005, color)
            i += 1
    paintSingleColor(off)

# tricks = [shifter_loop, backandforth_loop, fill_the_glass_loop, circle_loop]
# tricks = [chase_loop, marquee_loop, marquee_loop_static] # noqa
tricks = [chase_loop] # noqa
# colors = [orange, purple]
colors = [orange, purple]
while True:
    try:
        random.choice(tricks)(color=random.choice(colors))
    except KeyboardInterrupt:
        paintSingleColor(off)
        sys.exit()