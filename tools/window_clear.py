fo = open("/dev/rpmsg_pru30", "w")


def clear_all():
    for i in range(0, 364):
        # print(i)
        fo.write("%d %d %d %d\n" % (i, 0, 0, 0))
        fo.flush()
        # sleep(.5)
    fo.write("-1 0 0 0\n")
    fo.flush()


if __name__ == "__main__":
    clear_all()
    fo.close()
