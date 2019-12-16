from flask import Flask
import os
import signal
from subprocess import Popen, PIPE
import tempfile

app = Flask(__name__)
script_root = '/home/debian/neopixel-projects/'
python = '/usr/bin/python3'
temp = tempfile.TemporaryFile(mode='w+')

@app.route('/api/xmas/', methods=['GET'])
def xmas():
    try:
        p = Popen([python, script_root+'christmas/window.py'], stdout=PIPE)
        temp.seek(0)
        temp.write(str(p.pid))
        temp.truncate()
        return('Starting XMAS')
    except Exception as e:
        return 'Error: ' + str(e)


@app.route('/api/kill/', methods=['GET'])
def kill():
    try:
        temp.seek(0)
        pid = int(temp.read())
        # pid = int(pid_b.decode())
        os.kill(pid, signal.SIGKILL) #or signal.SIGKILL
        # os.killpg(os.getpgid(pid), signal.SIGTERM)  
        clear()
        return('Killing last known proccess: {}'.format(str(pid)))
    except Exception as e:
        return 'Error: ' + str(e)


@app.route('/api/clear/', methods=['GET'])
def clear():
    try:
        p = Popen([python, script_root+'tools/window_clear.py'], stdout=PIPE)
        return('Clearing LEDS')
    except Exception as e:
        return 'Error: ' + str(e)

@app.route('/api/halloween/', methods=['GET'])
def halloween():
    try:
        p = Popen([python, script_root+'halloween/window.py'], stdout=PIPE)
        temp.seek(0)
        temp.write(str(p.pid))
        temp.truncate()
        return('Starting Halloween')
    except Exception as e:
        return 'Error: ' + str(e)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
