import time
import random
from dataclasses import dataclass


class Pattern(object):
    def __init__(self, pru: str = '/dev/rpmsg_pru30', pixel_count: int = 365, push: bool = False):
        self.__pru = pru
        self.fo = open(self.__pru, 'w')
        self.push = push
        self.pixel_count = pixel_count

    def commit(self):
        self.fo.write('-1 0 0 0\n')
        self.fo.flush()

    def write(self, pixel_location: int, color: tuple):
        r, g, b = color
        self.fo.write(f'{pixel_location} {r} {g} {b}\n')
        self.fo.flush()
        if self.push:
            self.commit()

    def paint_all_windows(self, color):
        for pixel in range(0, self.pixel_count):
            self.write(pixel_location=pixel, color=color)
        self.commit()

    def paint_pixel_list(self, color, pixels: list, push: bool = False):
        for pixel in pixels:
            self.write(pixel_location=pixel, color=color)
        if push:
            self.commit()


class Strobe(Pattern):
    def __init__(self, color: tuple = (255, 255, 255)):
        self.__color = color
        super().__init__()

    def run(self, color):
        self.paint_all_windows(Colors.off)
        self.paint_all_windows(self.__color)
        self.paint_all_windows(Colors.off)
        self.paint_all_windows(self.__color)
        self.paint_all_windows(Colors.off)

    def loop(self, color: tuple = (255, 255, 255), loop_count: int = 20, wait: int = 0):
        for loop in range(0, loop_count):
            self.run(color)
            time.sleep(wait)


class Marquee(Pattern):
    def __init__(self, color: tuple = (255, 255, 255)):
        self.__color = color
        super().__init__()

    def run(self, color, wait: int = 1):
        evens = []
        odds = []
        for num in range(self.pixel_count):
            if num % 2 == 0:
                evens.append(num)
            else:
                odds.append(num)
        self.paint_pixel_list(color=color, pixels=evens)
        self.paint_pixel_list(color=Colors.off, pixels=odds)
        self.commit()
        time.sleep(wait)
        self.paint_pixel_list(color=color, pixels=odds)
        self.paint_pixel_list(color=Colors.off, pixels=evens)
        self.commit()
        time.sleep(wait)

    def loop(self, color: tuple = (255, 255, 255), loop_count: int = 20, wait: int = 1):
        for loop in range(0, loop_count):
            self.run(color, wait)


class SimpleChase(Pattern):
    def __init__(self, color: tuple = (255, 255, 255)):
        self.__color = color
        super().__init__()

    def run(self, color, wait: int = 1):
        self.paint_all_windows(Colors.off)
        self.push = True
        for i in range(0, self.pixel_count):
            self.write(color, pixel_location=i)
            # self.paint_positions([i], color, push=True)
            time.sleep(wait)
        for i in range(0, self.pixel_count):
            self.write(pixel_location=i, color=Color.off)
            #self.paint_positions([i], self.__off, push=True)
            time.sleep(wait)


@dataclass
class Colors:
    off: tuple = (0, 0, 0)
    aqua: tuple = (0, 0x10, 0x10)
    black: tuple = (6.02344, 6.02344, 6.02344)
    blue1: tuple = (0, 0, 0x10)
    blue2: tuple = (0, 0, 255)
    green: tuple = (0, 0x10, 0)
    halloween_orange: tuple = (164.64062, 38.14844, 2.00781)
    jen_orange: tuple = (164.64062, 38.14844, 2.00781)
    jen_red: tuple = (74.2890625, 0.0, 0.0)
    orange: tuple = (245, 25, 0)
    pink: tuple = (200, 25, 31)
    purple1: tuple = (0x10, 0, 0x10)
    purple2: tuple = (36.14062, 4.01562, 51.19922)
    red1: tuple = (0x10, 0, 0)
    red2: tuple = (0x10, 0, 0)
    red3: tuple = (74.2890625, 0.0, 0.0)
    yellow: tuple = (0x10, 0x10, 0)


def main():
    meh = Strobe()
    meh.loop(color=Colors.blue2)
    # for loop in range(0, meh.loops):
        # meh.run()
    # hi = SimpleChase()
    # hi = Marquee(Colors.blue2)
    # hi = Strobe()
    # for loop in range(0, hi.loops):
    #     hi.run(color=Colors.halloween_orange)
    # hi.loop(color=Colors.blue1)


'''
class ALLPattern(object):
    def __init__(self, name: str, wait: int = 0, pru: str = '/dev/rpmsg_pru30'):
        self.__name: str = name
        self.__wait: int = wait
        self.__colors: list = []
        self.__off = (0, 0, 0)
        self.pixel_count: int = 364
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


    def simple_chase(self, color: tuple):
        self.paint_single_color(self.__off)
        if not color:
            color = (0, 0, 0x10)
        for i in range(self.pixel_count):
            self.paint_positions([i], color, push=True)
            time.sleep(self.wait)
        for i in range(self.pixel_count):
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
        all_pixels = list(range(0, self.pixel_count))
        dim_white = (36.140625, 36.140625, 36.140625)
        sleepz = [.25, .5, .75, .125, .0625, 1, 1.5]
        while len(all_pixels) > int(self.pixel_count * percent / 100):
            pixel = all_pixels.pop(random.randrange(len(all_pixels)))
            time.sleep(random.choice(sleepz))
            print(pixel)
            self.paint_positions([pixel], dim_white, push=True)




class LightRunner(object):
    def __init__(self):
        self.__patterns = []

'''

if __name__ == '__main__':
    main()
