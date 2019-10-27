from tkinter import colorchooser
import requests

def main():
    color=colorchooser.askcolor()
    r = str(color[0][0])
    g = str(color[0][1])
    b = str(color[0][2])
    request = f'http://192.168.1.6:8080/api/color/?r={r}&g={g}&b={b}'
    print(request)
    try:
        requests.get(request)
    except Exception as e:
        raise Exception('Request Error: ' +str(e))

if __name__ == "__main__":
    while True:
        main()