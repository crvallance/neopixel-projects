import time
import random
from dataclasses import dataclass
from typing import Type


class LightController():
    def __init__(self, pru: str = '/dev/rpmsg_pru30', pixel_count: int = 365):
        self._pru = pru
        self.fo = open(self._pru, 'w')
        self.pixel_count = pixel_count
        self.right_window = range(0, 119 + 1)
        self.center_window = range(120, 243 + 1)
        self.left_window = range(244, 363 + 1)
    
    def write(self, pixel_location: int, color: tuple, autocommit: bool = False):
        r, g, b = color
        self.fo.write(f'{pixel_location} {r} {g} {b}\n')
        self.fo.flush()
        if autocommit:
            self.commit()
    
    def commit(self):
        self.fo.write('-1 0 0 0\n')
        self.fo.flush()

    def paint_all_windows(self, color):
        for pixel in range(0, self.pixel_count):
            self.write(pixel_location=pixel, color=color)
        self.commit()

    def paint_pixel_list(self, color, pixels: list, push: bool = False):
        for pixel in pixels:
            self.write(pixel_location=pixel, color=color, autocommit=False)
        if push:
            self.commit()


class Display():
    pass

class Pattern():
    pass

class RepeaterPattern(Pattern):
    def __init__(self, patterns, count):
        self._patterns = patterns
        self._count = count

    def run(self, controller: Type[LightController]):
        for _ in range(self._count):
            for pattern in self._patterns:
                pattern.run(controller)

class SequentialDisplay(Display):
    def __init__(self):
        self._patterns = [
            SimpleChase(color=Colors.halloween_orange)
        ]

    def run(self, controller: Type[LightController]):
        for pattern in self._patterns:
            pattern.run(controller)

class RandomDisplay(Display):
    def __init__(self):
        self._patterns = [
            SimpleChase(color=Colors.halloween_orange),
        ]

    def run(self, controller: Type[LightController]):
        random.shuffle(self._patterns)
        for pattern in self._patterns:
            pattern.run(controller)

class Halloween(RandomDisplay):
    def __init__(self):
        super().__init__()
        chase1 = [
            WindowChase(color=Colors.halloween_orange, direction='r'),
            WindowChase(color=Colors.purple2, direction='l'),
            WindowChase(color=Colors.green, direction='r'),
            WindowChase(color=Colors.off)
            ]
        chase2 = [
            WindowChase(color=Colors.halloween_orange),
            WindowChase(color=Colors.off)
            ]
        chase3 = [
            WindowChase(color=Colors.purple2),
            WindowChase(color=Colors.off)
            ]
        chase4 = [
            WindowChase(color=Colors.green),
            WindowChase(color=Colors.off)
            ]
        chase1_repeater = RepeaterPattern(chase1, 5)
        chase2_repeater = RepeaterPattern(chase2, 5)
        chase3_repeater = RepeaterPattern(chase3, 5)
        chase4_repeater = RepeaterPattern(chase4, 5)
        self._patterns = [
            # Strobe(color=Colors.halloween_orange, loop_count=30),
            # Strobe(color=Colors.purple2, loop_count=30),
            # Marquee(color1=Colors.halloween_orange, loop_count=15),
            # Marquee(color1=Colors.halloween_orange, color2=Colors.purple2, loop_count=15),
            Marquee(color1=Colors.halloween_orange, color2=Colors.purple2, loop_count=15, dense = True),
            # Marquee(color1=Colors.purple2, loop_count=15),
            # chase1_repeater,
            # chase2_repeater,
            # chase3_repeater,
            # chase4_repeater,
        ]


class EmptyPattern():
    pass


class ClearPixels(EmptyPattern):
    def run(self, controller: Type[LightController]):
        controller.paint_all_windows(Colors.off)


class SimpleChase(EmptyPattern):
    def __init__(self, loop_count: int = 5, color: tuple = (255, 255, 255)):
        self._color = color
        self._count = loop_count
        self._wait = 0
        super().__init__()

    def run(self, controller: Type[LightController], color: tuple = (255, 255, 255), wait: int = .0005):
        for loop in range(0, self._count):
            for i in range(0, controller.pixel_count):
                controller.write(color=self._color, pixel_location=i, autocommit=True)
                time.sleep(self._wait)
            for i in range(0, controller.pixel_count):
                controller.write(pixel_location=i, color=Colors.off, autocommit=True)


class Strobe(EmptyPattern):
    def __init__(self, loop_count: int = 20, color: tuple = (255, 255, 255)):
        self._color = color
        self._count = loop_count
        self._wait = 0
        super().__init__()

    def run(self, controller: Type[LightController]):
        for loop in range(0, self._count):
            controller.paint_all_windows(Colors.off)
            controller.paint_all_windows(self._color)
            controller.paint_all_windows(Colors.off)
            controller.paint_all_windows(self._color)
            time.sleep(self._wait)
        controller.paint_all_windows(Colors.off)


class Marquee(EmptyPattern):
    def __init__(self, loop_count: int = 20, color1: tuple = (255, 255, 255), color2: tuple = (0, 0, 0), dense: bool = False):
        self._color1 = color1
        self._color2 = color2
        self._dense = dense
        self._count = loop_count
        self._wait = 1
        super().__init__()

    def run(self, controller: Type[LightController]):
        for loop in range(0, self._count):
            evens = []
            odds = []
            for num in range(controller.pixel_count):
                if num % 2 == 0:
                    evens.append(num)
                else:
                    odds.append(num)
            controller.paint_pixel_list(color=self._color1, pixels=evens)
            if self._dense:
                controller.paint_pixel_list(color=self._color2, pixels=odds)
            else:
                controller.paint_pixel_list(color=Colors.off, pixels=odds)
            controller.commit()
            time.sleep(self._wait)
            if self._dense:
                controller.paint_pixel_list(color=self._color1, pixels=odds)
                controller.paint_pixel_list(color=self._color2, pixels=evens)
            else:
                controller.paint_pixel_list(color=self._color2, pixels=odds)
                controller.paint_pixel_list(color=Colors.off, pixels=evens)
            controller.commit()
            time.sleep(self._wait)
        controller.paint_all_windows(Colors.off)


class WindowChase(EmptyPattern):
    def __init__(self, loop_count: int = 1, color: tuple = (255, 255, 255), direction='l'):
        self._direction = direction
        self._color = color
        self._count = loop_count
        self._wait = 1
        super().__init__()
    
    def run(self, controller: Type[LightController]):
        for loop in range(0, self._count):
            if self._direction == 'l':
                popindex = 0
            elif self._direction == 'r':
                popindex = -1
            center_cheat = [63, 62, 61, 60]
            r_list = list(controller.right_window)
            c_list = list(controller.center_window)
            l_list = list(controller.left_window)
            for i, val in enumerate(controller.center_window):
                if i in center_cheat:
                    try:
                        pixels = [c_list.pop(popindex)]
                        controller.paint_pixel_list(pixels=pixels, color=self._color, push=True)
                    except IndexError as e:
                        print('Error %s' % e)
                        print('Cheat %d' % val)
                if i < 60:
                    try:
                        pixels = [r_list.pop(popindex), c_list.pop(popindex), l_list.pop(popindex)]
                        controller.paint_pixel_list(pixels=pixels, color=self._color, push=True)
                    except IndexError as e:
                        print('Error %s' % e)
                        print('Under 181 %d' % val)
                if i > 63:
                    try:
                        pixels = [r_list.pop(popindex), c_list.pop(popindex), l_list.pop(popindex)]
                        controller.paint_pixel_list(pixels=pixels, color=self._color, push=True)
                    except IndexError as e:
                        print('Error %s' % e)
                        print('Over 184 %d' % val)


class Popcorn(object):
    def __init__(self, loop_count: int = 1, color: tuple = (36.140625, 36.140625, 36.140625), percent: int = 20):
        self._color = color
        self._count = loop_count
        self._wait = 1
        self._percent = percent
        self._sleepz = [.25, .5, .75, .125, .0625, 1, 1.5]
        super().__init__()

    def run(self, controller: Type[LightController]):
        for loop in range(0, self._count):
            controller.paint_all_windows(Colors.off)
            all_pixels = list(range(0, controller.pixel_count))
            while len(all_pixels) > int(controller.pixel_count * self._percent / 100):
                pixel = all_pixels.pop(random.randrange(len(all_pixels)))
                time.sleep(random.choice(self._sleepz))
                controller.paint_pixel_list(pixels=[pixel], color=self._color, push=True)
        controller.paint_all_windows(Colors.off)

@dataclass
class Colors:
    off: tuple = (0, 0, 0)
    aqua: tuple = (0, 0x10, 0x10)
    black: tuple = (6.02344, 6.02344, 6.02344)
    blue1: tuple = (0, 0, 0x10)
    blue2: tuple = (0, 0, 255)
    green: tuple = (0, 0x10, 0)
    halloween_orange: tuple = (164.64062, 38.14844, 2.00781)
    jen_red: tuple = (74.2890625, 0.0, 0.0)
    orange: tuple = (245, 25, 0)
    pink: tuple = (200, 25, 31)
    purple1: tuple = (0x10, 0, 0x10)
    purple2: tuple = (36.14062, 4.01562, 51.19922)
    red1: tuple = (0x10, 0, 0)
    red3: tuple = (74.2890625, 0.0, 0.0)
    yellow: tuple = (0x10, 0x10, 0)
    white: tuple = (255, 255, 255)

