fo = open("/dev/rpmsg_pru30", "w")
pixnum = 364


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(pixnum):
            rc_index = (i * 256 // pixnum) + j
            # pixels[i] = wheel(rc_index & 255)
            color_tup = wheel(rc_index & 255)
            setpix = str(i) + ' '
            for cnt, item in enumerate(color_tup):
                if cnt == 2:
                    setpix += str(item) + '\n'
                else:
                    setpix += (str(item) + ' ')
            fo.write(setpix)
            fo.flush()
        fo.write("-1 0 0 0\n")


rainbow_cycle(1)
