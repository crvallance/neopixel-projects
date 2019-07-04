#!/usr/env/python
import board
import neopixel_write
import digitalio


def colors(color):
    if "off" in color:
        rgbout = [0, 0, 0]
    if "orange" in color:
        rgbout = [255, 140, 0]
    if "blue" in color:
        rgbout = [0, 0, 255]
    if "green" in color:
        rgbout = [255, 0, 0]
    if "yellow" in color:
        rgbout = [255, 255, 0]
    if "red" in color:
        rgbout = [0, 255, 0]
    if "purple" in color:
        rgbout = [128, 0, 128]
    if "white" in color:
        rgbout = [255, 255, 255]
    return rgbout


def light_all(color, pix_cnt=12):
    allcolor = colors(color)
    light = allcolor * 12
    return light


pin = digitalio.DigitalInOut(board.A0)
pin.direction = digitalio.Direction.OUTPUT

""" Example with color cycling
color_cycle = ['white', 'green', 'red', 'blue', 'yellow']

for item in color_cycle:
  neopixel_write.neopixel_write(pin, colors(item))
  time.sleep(5)
"""

neopixel_write.neopixel_write(pin, bytearray(light_all("white")))
