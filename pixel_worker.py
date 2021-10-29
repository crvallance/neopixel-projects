class Pattern(object, pru='/dev/rpmsg_pru30'):
    def __init__(self, name):
        self.__name = name
        self.__colors = []
        self.pixnum = 364
        self.right_window = range(0, 120)
        self.center_window = range(120, 244)
        self.left_window = range(244, 364)
        self.all_windows = range(0, 364)

    def name(self):
        return self.__name

    def with_color(self, color):
        self.__colors.append(color)
        return self

    def pru_init(self):
        pru_file_object = open(self.pru)
        return(pru_file_object)

    def paint_single_color(self, color):
        fo = self.pru_init()
        r, g, b = color
        for i in self.all_windows:
            fo.write("%d %d %d %d\n" % (i, r, g, b))
            fo.flush()
        fo.write("-1 0 0 0\n")


class LightRunner(object):
    def __init__(self):
        self.__patterns = []


class Color(object):
    def __init__(self):
        self.halloween_orange = (164.64062, 38.14844, 2.00781)
        self.purple = (36.14062, 4.01562, 51.19922)
        self.black = (6.02344, 6.02344, 6.02344)
        self.off = (0, 0, 0)
        self.pink = (200, 25, 31)
        self.orange = (245, 25, 0)
