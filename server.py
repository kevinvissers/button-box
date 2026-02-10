from flask import Flask, request, send_from_directory, render_template
from pynput.keyboard import Controller, Key
import time

app = Flask(__name__)
keyboard = Controller()

dry_run = True

@app.route('/')
def index():
    """
    Display main page
    """

    navigation = [{
        "active": "false",
        "href": "/eurotruck",
        "caption": "Eurotruck"
    }]
    return render_template('index.html', navigation=navigation)

@app.route('/eurotruck')
def eurotruck():
    """
    Display Eurotruck simulator button box
    """
    
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

    return render_template('eurotruck.html',dry_run=dry_run, navigation=navigation, control=control, vehicle=vehicle, lights=lights, signals=signals, audio=audio, camera=camera, manager=manager)

@app.route('/dryrun', methods=['POST'])
def dryrun():
    """
    Disable or enable dry run mode
    """

    global dry_run
    dry_run = request.json.get('value') == True
    return '', 204

@app.route('/press', methods=['POST'])
def press():
    """
    Handle key-press event
    """

    key: str = request.json.get('key')
    duration: int = int(request.json.get('duration'))

    print("key: " + key)
    print("duration: " + str(duration))

    if key == 'page-up':
        _keyPress(Key.page_up)

    elif key == 'page-down':
        _keyPress(Key.page_down)
    
    elif key == 'SPACE':
        _keyPress(Key.space)

    elif key == 'shift+d':
        _keyPressWithHolder('d', Key.shift)

    else:
        _keyPressWithDuration(key, duration)

    return '', 204


def _keyPress(key):
    """
    Press and release a key
    
    :param key: Key to press
    """

    if not dry_run:
        keyboard.press(key)
        keyboard.release(key)
    else:
        print('DRYRUN - Pressing key ' + str(key))


def _keyPressWithDuration(key, durationInSeconds):
    """
    Press and hold key before releasing
    When duration is 0, the key is just pressed
    
    :param key: Key to press
    :param duration: Duration in seconds to hold
    """

    if not dry_run:
        keyboard.press(key.lower())
        if durationInSeconds != 0:
            time.sleep(durationInSeconds)
        keyboard.release(key.lower())
    else:
        print('DRYRUN - Pressing key ' + str(key) + ' with duration ' + str(durationInSeconds))


def _keyPressWithHolder(key, holder):
    """
    Press a key while holding another button
    e.g SHIFT+A
    
    :param key: Key to press (e.g. A)
    :param holder: Key which is holded while pressing the other key (e.g. SHIFT)
    """
    
    if not dry_run:
        with keyboard.pressed(holder):
            keyboard.press(key)
            keyboard.release(key)
    else:
        print('DRYRUN - Pressing key ' + str(key) + ' while holding ' + str(holder))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, load_dotenv=True, debug=True)
    