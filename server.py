from flask import Flask, request, send_from_directory, render_template
from pynput.keyboard import Controller, Key
import threading
import time

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

    control = [
        {
            "caption": "power",
            "key": "e",
            "type": "btn-danger"
        }
    ]

    vehicle = [
        {
            "caption": "Handbrake",
            "key": "SPACE",
            "type": "btn-outline-danger"
        },
        {
            "caption": "E-break",
            "key": "b",
            "type": "btn-outline-warning",
            "separator": True
        },
        {
            "caption": "Retarder+",
            "key": ";",
            "type": "btn-outline-info"
        },
        {
            "caption": "Retarder-",
            "key": "\\'",
            "type": "btn-outline-info"
        },
        {
            "caption": "Axle",
            "key": "u",
            "type": "btn-outline-primary",
            "separator": True
        },
        {
            "caption": "Trailer",
            "key": "t",
            "type": "btn-outline-primary"
        },
    ]

    lights = [
        {
            "caption": "Toggle",
            "key": "l",
            "type": "btn-outline-primary"
        },
        {
            "caption": "Hazard",
            "key": "f",
            "type": "btn-outline-danger"
        },
        {
            "caption": "H-Beam",
            "key": "k",
            "type": "btn-outline-info"
        },
        {
            "caption": "Warning",
            "key": "o",
            "type": "btn-outline-warning"
        },
    ]

    signals = [
        {
            "caption": "Horn",
            "key": "h",
            "type": "btn-outline-primary",
            "duration": 1
        },
        {
            "caption": "Pneumatic",
            "key": "n",
            "type": "btn-outline-light",
            "duration": 1
        },
        {
            "caption": "Light",
            "key": "j",
            "type": "btn-outline-info",
            "duration": 1
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
            "key": "r",
            "type": "btn-outline-success"
        },
        {
            "caption": "skip-forward-fill",
            "key": "page-down",
            "type": "btn-outline-success"
        },
        
    ]

    camera = [
        {
            "caption": "Interior",
            "key": "&",
            "type": "btn-outline-light"
        },
        {
            "caption": "Following",
            "key": "é",
            "type": "btn-outline-light"
        },
        {
            "caption": "Vertical",
            "key": "\"",
            "type": "btn-outline-light"
        },
        {
            "caption": "Next",
            "key": "ç",
            "type": "btn-outline-light"
        },
    ]

    manager = [
        {
            # World map
            "caption": "globe",
            "key": "m",
            "type": "btn-outline-primary"
        },
        {
            # Garage manager
            "caption": "house-fill",
            "key": "g",
            "type": "btn-outline-primary",
            "separator": True
        },
        {
            # F5 - Mouse Control In Route Advisor
            "caption": "mouse2",
            "key": "F5",
            "type": "btn-outline-info"
        },
        {
            # F6 - Route Advisor: Navigation Page
            "caption": "sign-turn-right-fill",
            "key": "F6",
            "type": "btn-outline-info"
        },
        {
            # F7 - Route Advisor: Information About Orders
            "caption": "list-task",
            "key": "F7",
            "type": "btn-outline-light"
        },
        {
            # F8 - Route Advisor: Truck Diagnostics
            "caption": "bug",
            "key": "F8",
            "type": "btn-outline-warning"
        },
        {
            # F9 - Route Advisor Information Page
            "caption": "info-circle",
            "key": "F9",
            "type": "btn-outline-info"
        },
    ]

    return render_template('eurotruck.html', navigation=navigation, control=control, vehicle=vehicle, lights=lights, signals=signals, audio=audio, camera=camera, manager=manager)

@app.route('/press', methods=['POST'])
def press():
    key: str = request.json.get('key')
    duration: int = int(request.json.get('duration'))

    print("key: " + key)
    print("duration: " + str(duration))

    if key == 'page-up':
        keyboard.press(Key.page_up)
        keyboard.release(Key.page_up)

    elif key == 'page-down':
        keyboard.press(Key.page_down)
        keyboard.release(Key.page_down)
    
    elif key == 'SPACE':
        keyboard.press(Key.space)
        keyboard.release(Key.space)

    elif key == 'shift+d':
        with keyboard.pressed(Key.shift):
            keyboard.press('d')
            keyboard.release('d')
    else:
        keyboard.press(key.lower())

        if duration != 0:
            time.sleep(duration)

        keyboard.release(key.lower())
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, load_dotenv=True, debug=True)
    