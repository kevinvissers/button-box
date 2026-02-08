from flask import Flask, request, send_from_directory, render_template
from pynput.keyboard import Controller, Key
import threading

app = Flask(__name__)
keyboard = Controller()

@app.route('/')
def index():
    navigation = [{
        "active": "false",
        "href": "/eurotruck",
        "caption": "Eurotruck"
    }]
    return render_template('index.html', navigation=navigation)

@app.route('/farming')
def farming():
    return send_from_directory('.', 'pages/farming.html')

@app.route('/eurotruck')
def eurotruck():
    navigation = [{
        "active": "true",
        "href": "/eurotruck",
        "caption": "Eurotruck"
    }]

    buttons={}
    buttons["start_stop"] = "e"

    vehicle = [
        {
            "caption": "Handbrake",
            "key": "SPACE",
            "type": "btn-warning"
        },
        {
            "caption": "Engine break",
            "key": "B",
            "type": "btn-outline-warning"
        },
        {
            "caption": "Retarder +",
            "key": ";",
            "type": "btn-outline-info"
        },
        {
            "caption": "Retarder -",
            "key": "'",
            "type": "btn-outline-info"
        },
        {
            "caption": "Lift/Let down axle",
            "key": "U",
            "type": "btn-outline-primary"
        },
    ]

    lights = [
        {
            "caption": "Toggle",
            "key": "L",
            "type": "btn-primary"
        },
        {
            "caption": "Hazard",
            "key": "F",
            "type": "btn-danger"
        },
        {
            "caption": "High beam",
            "key": "K",
            "type": "btn-outline-info"
        },
        {
            "caption": "Warning",
            "key": "O",
            "type": "btn-outline-warning"
        },
    ]

    signals = [
        {
            "caption": "Horn",
            "key": "H",
            "type": "btn-primary"
        },
        {
            "caption": "Pneumatic",
            "key": "N",
            "type": "btn-danger"
        },
        {
            "caption": "Light",
            "key": "J",
            "type": "btn-outline-info"
        },
    ]

    audio = [
        {
            "caption": "skip-backward-fill",
            "key": "page-up",
            "type": "btn-outline-success"
        },
        {
            "caption": "play-fill",
            "key": "R",
            "type": "btn-success"
        },
        {
            "caption": "skip-forward-fill",
            "key": "page-down",
            "type": "btn-outline-success"
        },
        
    ]

    return render_template('eurotruck.html', navigation=navigation, buttons=buttons, vehicle=vehicle, lights=lights, signals=signals, audio=audio)

@app.route('/press', methods=['POST'])
def press():
    key = request.json.get('key')
    if key == 'page-up':
        keyboard.press(Key.page_up)
        keyboard.release(Key.page_up)

    elif key == 'page-down':
        keyboard.press(Key.page_down)
        keyboard.release(Key.page_down)

    elif key == 'shift+d':
        with keyboard.pressed(Key.shift):
            keyboard.press('d')
            keyboard.release('d')
    else:
        keyboard.press(key)
        keyboard.release(key)
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, load_dotenv=True, debug=True)
    