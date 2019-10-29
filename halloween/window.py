import time
import random
import sys

# Some static stuff
# Colors
jen_orange = (164.64062, 38.14844, 2.00781)
purple = (36.14062, 4.01562, 51.19922)
black = (6.02344, 6.02344, 6.02344)
off = (0, 0, 0)
pink = (200, 25, 31)
orange = (245, 25, 0)
# red = 0x100000  (0x10, 0, 0) also works
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
r_window = range(0, 119 + 1)
c_window = range(120, 243 + 1)
l_window = range(244, 363 + 1)

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


def marquee_static(wait, color=()):
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
    paintPositions(odds, black)
    fo.write("-1 0 0 0\n")
    fo.flush()
    time.sleep(wait)
    paintPositions(evens, black)
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


def window_chase(color=(), direction='l'):
    if direction == 'l':
        popindex = 0
    elif direction == 'r':    
        popindex = -1
    center_cheat = [63, 62, 61, 60]
    r_list = list(r_window)
    c_list = list(c_window)
    l_list = list(l_window)
    for i, val in enumerate(c_window):
        if i in center_cheat:
            try:
                pixel = [c_list.pop(popindex)]
                paintPositions(pixel, color, push=True)
            except IndexError as e:
                print('Error %s' % e)
                print('Cheat %d' % val)
        if i < 60:
            try:
                pixels = [r_list.pop(popindex), c_list.pop(popindex), l_list.pop(popindex)]
                paintPositions(pixels, color, push=True)
            except IndexError as e:
                print('Error %s' % e)
                print('Under 181 %d' % val)
        if i > 63:
            try:
                pixels = [r_list.pop(popindex), c_list.pop(popindex), l_list.pop(popindex)]
                paintPositions(pixels, color, push=True)
            except IndexError as e:
                print('Error %s' % e)
                print('Over 184 %d' % val)


def popcorn(color):
    paintSingleColor(off)
    percent = 20
    all_pixels = list(range(0, pixnum))
    dim_white = (36.140625, 36.140625, 36.140625)
    sleepz = [.25, .5, .75, .125, .0625, 1, 1.5]
    while len(all_pixels) > int(pixnum * percent/100):
        pixel = all_pixels.pop(random.randrange(len(all_pixels)))
        time.sleep(random.choice(sleepz))
        print(pixel)
        paintPositions([pixel], dim_white, push=True)

def strobe(color):
    bright_white = (255, 255, 255)
    paintSingleColor(off)
    paintSingleColor(bright_white)
    paintSingleColor(off)
    paintSingleColor(bright_white)
    paintSingleColor(off)
    paintSingleColor(bright_white)
    paintSingleColor(off)
    paintSingleColor(bright_white)


def marquee_loop(sleep=2, color=()):
    # print('random color is: {}'.format(color))
    loops = 10
    for i in range(1, loops):
        if i < loops:
            print('marquee loop: {} of {}'.format(i, loops))
            marquee(sleep, color)
            i += 1
    paintSingleColor(off)

def marquee_static_loop(sleep=2, color=()):
    # print('random color is: {}'.format(color))
    loops = 10
    for i in range(1, loops):
        if i < loops:
            print('marquee static loop: {} of {}'.format(i, loops))
            marquee_static(sleep, color)
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

def window_chase_loop(color=()):
    loops = 6
    dirs = ['l', 'r']
    loop_dir = random.choice(dirs)
    for i in range(1, loops):
        print(loop_dir)
        random.shuffle(colors)
        r_color=colors[0]
        print(r_color)
        if i < loops:
            print('window chase loop: {} of {}'.format(i, loops))
            window_chase(r_color, direction=loop_dir)
            i += 1
    paintSingleColor(off)

# tricks = [shifter_loop, backandforth_loop, fill_the_glass_loop, circle_loop]
# tricks = [chase_loop, marquee_loop, marquee_loop_static] # noqa
tricks = [marquee_static_loop] # noqa
# colors = [orange, purple]
colors = [orange, purple]
while True:
    try:
        random.choice(tricks)(color=random.choice(colors))
    except KeyboardInterrupt:
        paintSingleColor(off)
        sys.exit()