from flask import Flask, request, send_from_directory
from pynput.keyboard import Controller, Key
import threading

app = Flask(__name__)
keyboard = Controller()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/farming')
def farming():
    return send_from_directory('.', 'farming.html')

@app.route('/press', methods=['POST'])
def press():
    key = request.json.get('key')
    if key == 'shift+d':
        with keyboard.pressed(Key.shift):
            keyboard.press('d')
            keyboard.release('d')
    else:
        keyboard.press(key)
        keyboard.release(key)
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    