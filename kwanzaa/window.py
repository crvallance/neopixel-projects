# import sys
from dateutil import tz
from datetime import datetime
import time

# Some static stuff
# Colors
red = (74.2890625, 0.0, 0.0)
green = (0, 0x10, 0)
off = (0, 0, 0)
pixnum = 364
r_window = range(0, 119 + 1)
c_window = range(120, 243 + 1)
l_window = range(244, 363 + 1)
# From inside the house: windows are Left, Center, Right
# Indicators are (L)eft, (T)op, (R)ight
# Windows ranges are w_i (window_indicator)
day_one = list(range(0, 50))  # r_r
day_two = list(range(70, 120))  # r_l
day_three = list(range(120, 170))  # c_r
day_four = list(range(194, 241))  # c_l
day_five = list(range(240, 294))  # l_r
day_six = list(range(313, 364))  # l_l

fo = open("/dev/rpmsg_pru30", "w")


def paintSingleColor(color):
    r, g, b = color
    for i in range(0, 364):
        fo.write("%d %d %d %d\n" % (i, r, g, b))
        fo.flush()
    fo.write("-1 0 0 0\n")


def strobe_error():
    blinks = 8
    sleepy = .25
    # bright_white = (255, 255, 255)
    paintSingleColor(off)
    for i in range(1, blinks):
        time.sleep(sleepy)
        paintSingleColor(red)
        time.sleep(sleepy)
        paintSingleColor(off)


def paintPositions(pixel_list, color_tup, push=False):
    r, g, b = color_tup
    for item in pixel_list:
        fo.write("%d %d %d %d\n" % (item, r, g, b))
        fo.flush()
    # if push == True:
    if push:
        fo.write("-1 0 0 0\n")
        fo.flush()


def lights_by_day():
    home_tz = tz.gettz("America/Chicago")
    now = datetime.now(tz=home_tz)
    paintSingleColor(off)
    if now.month == 12:
        if now.day == 27:
            paintPositions(day_one, red, push=True)
        if now.day == 28:
            paintPositions(day_one, red)
            paintPositions(day_two, red, push=True)
        if now.day == 29:
            paintPositions(day_one, red)
            paintPositions(day_two, red)
            paintPositions(day_three, red, push=True)
        if now.day == 30:
            paintPositions(day_one, red)
            paintPositions(day_two, red)
            paintPositions(day_three, red)
            paintPositions(day_four, green, push=True)
        if now.day == 31:
            paintPositions(day_one, red)
            paintPositions(day_two, red)
            paintPositions(day_three, red)
            paintPositions(day_four, green)
            paintPositions(day_five, green, push=True)
    elif now.month == 1: 
        if now.day == 1:
            paintPositions(day_one, red)
            paintPositions(day_two, red)
            paintPositions(day_three, red)
            paintPositions(day_four, green)
            paintPositions(day_five, green)
            paintPositions(day_six, green, push=True)
    else:
        strobe_error()


def main():
    lights_by_day()
    time.sleep()


if __name__ == "__main__":
    main()
