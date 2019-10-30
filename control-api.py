from flask import Flask, request
import os
from halloween import window

# Open a file
# fo = open("/dev/rpmsg_pru30", "w")

app = Flask(__name__)


@app.route('/api/shutdown/', methods=['GET'])
def shutdown():
    try:
        #os.system('tmux send-keys -t lights:0.0 C-c')
        window.paintSingleColor((0, 0, 0))
        #os.system('sudo /sbin/poweroff')
        return('Shutting Down! (Please unplug power supply')
    except Exception as e:
        return 'Error: ' + str(e)

@app.route('/api/halloween/', methods=['GET'])
def halloween():
    try:
        window.main()
        return('Running Halloween Script')
    except Exception as e:
        return 'Error: ' + str(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
