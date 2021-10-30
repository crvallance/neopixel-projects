import time
import random
from dataclasses import dataclass


class Pattern(object):
    def __init__(self, pru: str = '/dev/rpmsg_pru30', pixel_count: int = 365, push: bool = False):
        self.__pru = pru
        self.fo = open(self.__pru, 'w')
        self.push = push
        self.pixel_count = pixel_count

    def write(self, pixel_location: int, color: tuple):
        r, g, b = color
        self.fo.write(f'{pixel_location} {r} {g} {b}\n')
        self.fo.flush()
        if self.push:
            self.fo.write('-1 0 0 0\n')
            self.fo.flush()

    def paint_all_windows(self, color):
        for pixel in range(0, self.pixel_count):
            self.write(pixel_location=pixel, color=color)
        self.fo.write('-1 0 0 0\n')
        self.fo.flush()


class Strobe(Pattern):
    def __init__(self, color: tuple = (255, 255, 255)):
        self.__color = color
        super().__init__()

    def run(self):
        self.paint_all_windows(Colors.off)
        self.paint_all_windows(self.__color)
        self.paint_all_windows(Colors.off)
        self.paint_all_windows(self.__color)
        self.paint_all_windows(Colors.off)


@dataclass
class Colors:
    off: tuple = (0, 0, 0)
    halloween_orange: tuple = (164.64062, 38.14844, 2.00781)
    purple: tuple = (36.14062, 4.01562, 51.19922)
    black: tuple = (6.02344, 6.02344, 6.02344)
    pink: tuple = (200, 25, 31)
    orange: tuple = (245, 25, 0)


'''
class ALLPattern(object):
    def __init__(self, name: str, wait: int = 0, pru: str = '/dev/rpmsg_pru30'):
        self.__name: str = name
        self.__wait: int = wait
        self.__colors: list = []
        self.__off = (0, 0, 0)
        self.pixnum: int = 364
        self.right_window = range(0, 120)
        self.center_window = range(120, 244)
        self.left_window = range(244, 364)
        self.all_windows = range(0, 364)
        self.fo = open(self.pru, 'w')

    def name(self):
        return self.__name

    def wait(self):
        return self.__wait

    def with_color(self, color: tuple):
        self.__colors.append(color)
        return self

    def paint_single_color(self, color: tuple):
        r, g, b = color
        for i in self.all_windows:
            self.fo.write("%d %d %d %d\n" % (i, r, g, b))
            self.fo.flush()
        self.fo.write("-1 0 0 0\n")

    def paint_positions(self, window, color: tuple, push=False):
        r, g, b = color
        for item in window:
            self.fo.write("%d %d %d %d\n" % (item, r, g, b))
            self.fo.flush()
        if push:
            self.fo.write("-1 0 0 0\n")
            self.fo.flush()

    def marquee(self, color: tuple):
        if not color:
            color = (0, 0, 0x10)
        evens = []
        odds = []
        for num in range(self.pixnum):
            if num % 2 == 0:
                evens.append(num)
            else:
                odds.append(num)
        self.paintPositions(evens, color)
        self.paintPositions(odds, self.__off)
        self.fo.write("-1 0 0 0\n")
        self.fo.flush()
        time.sleep(self.wait)
        self.paintPositions(evens, self.__off)
        self.paintPositions(odds, color)
        self.fo.write("-1 0 0 0\n")
        self.fo.flush()
        time.sleep(self.wait)

    def simple_chase(self, color: tuple):
        self.paint_single_color(self.__off)
        if not color:
            color = (0, 0, 0x10)
        for i in range(self.pixnum):
            self.paint_positions([i], color, push=True)
            time.sleep(self.wait)
        for i in range(self.pixnum):
            self.paint_positions([i], self.__off, push=True)
            time.sleep(self.wait)

    def window_chase(self, color: tuple, direction='l'):
        if direction == 'l':
            popindex = 0
        elif direction == 'r':
            popindex = -1
        center_cheat = [63, 62, 61, 60]
        r_list = list(self.right_window)
        c_list = list(self.center_window)
        l_list = list(self.left_window)
        for i, val in enumerate(self.center_window):
            if i in center_cheat:
                try:
                    pixel = [c_list.pop(popindex)]
                    self.paint_positions(pixel, color, push=True)
                except IndexError as e:
                    print('Error %s' % e)
                    print('Cheat %d' % val)
            if i < 60:
                try:
                    pixels = [r_list.pop(popindex), c_list.pop(popindex), l_list.pop(popindex)]
                    self.paint_positions(pixels, color, push=True)
                except IndexError as e:
                    print('Error %s' % e)
                    print('Under 181 %d' % val)
            if i > 63:
                try:
                    pixels = [r_list.pop(popindex), c_list.pop(popindex), l_list.pop(popindex)]
                    self.paint_positions(pixels, color, push=True)
                except IndexError as e:
                    print('Error %s' % e)
                    print('Over 184 %d' % val)

    def popcorn(self, color: tuple):
        self.paint_single_color(self.__off)
        percent = 20
        all_pixels = list(range(0, self.pixnum))
        dim_white = (36.140625, 36.140625, 36.140625)
        sleepz = [.25, .5, .75, .125, .0625, 1, 1.5]
        while len(all_pixels) > int(self.pixnum * percent / 100):
            pixel = all_pixels.pop(random.randrange(len(all_pixels)))
            time.sleep(random.choice(sleepz))
            print(pixel)
            self.paint_positions([pixel], dim_white, push=True)




class LightRunner(object):
    def __init__(self):
        self.__patterns = []

'''


def main():
    meh = Strobe(Colors.purple)
    meh.run()


if __name__ == '__main__':
    main()
