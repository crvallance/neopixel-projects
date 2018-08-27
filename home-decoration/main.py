import adafruit_fancyled.adafruit_fancyled as fancy
import board
import neopixel
strip = neopixel.NeoPixel(board.D1, 12, auto_write=False, brightness=.3)
levels = (0.07, 0.06, 0.09)
'''palette = [fancy.CRGB(255, 255, 255),  # White
           fancy.CRGB(255, 255, 0),    # Yellow
           fancy.CRGB(255, 0, 0),      # Red
           fancy.CRGB(244, 66, 176),
           #fancy.CRGB(0,0,0)]          # Black
           ]
''' 
palette=[fancy.CRGB(148, 0, 211), 
        fancy.CRGB(75, 0, 130), 
        fancy.CRGB(0, 0, 255),
        fancy.CRGB(0, 255, 0),
        fancy.CRGB(255, 255, 0),
        fancy.CRGB(255, 127, 0),
        fancy.CRGB(255, 0 , 0),
        #fancy.CRGB(255, 255 , 255)
        ]


offset = 0  # Position offset into palette to make it "spin"
while True:
    for i in range(12):
        color = fancy.palette_lookup(palette, offset + i / 12)
        #color = fancy.gamma_adjust(color, brightness=levels)
        strip[i] = color.pack()
    strip.show()
 
    offset += .05  # Bigger number = faster spin
