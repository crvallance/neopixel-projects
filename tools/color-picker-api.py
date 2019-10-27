from flask import Flask, request

# Open a file
fo = open("/dev/rpmsg_pru30", "w")

app = Flask(__name__)


def set_colors(r, g, b):
    for i in range(0, 364):
        # print(i)
        fo.write("%d %d %d %d\n" % (i, r, g, b))
        fo.flush()
        # sleep(.5)
    fo.write("-1 0 0 0\n")
    fo.flush()


@app.route('/api/color/', methods=['GET'])
def color():
    # rquest should look like: :8080/api/color?r=0&g=0&b=0
    r = float(request.args.get('r', None))
    g = float(request.args.get('g', None))
    b = float(request.args.get('b', None))
    try:
        set_colors(r, g, b)
        return('R:%0.5f G:%0.5f B:%0.5f') % (r, g, b)
    except Exception as e:
        return 'Error: ' + str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
