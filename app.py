from flask import Flask, render_template, request, jsonify
from gpiozero import OutputDevice
import json
from datetime import datetime
import threading
import time

app = Flask(__name__)

IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

pin1 = OutputDevice(IN1)
pin2 = OutputDevice(IN2)
pin3 = OutputDevice(IN3)
pin4 = OutputDevice(IN4)

curtain_state = "unknown"
motor_stop = False

step_sequence = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

def load_schedule():
    with open('schedule.json', 'r') as f:
        return json.load(f)

def save_schedule(schedule):
    with open('schedule.json', 'w') as f:
        json.dump(schedule, f, indent=2)

def load_state():
    try:
        with open('state.json', 'r') as f:
            return json.load(f)['state']
    except:
        return "unknown"

def save_state(state):
    with open('state.json', 'w') as f:
        json.dump({'state': state}, f)

curtain_state = load_state()

def motor_forward(steps):
    global motor_stop
    motor_stop = False
    for _ in range(steps):
        if motor_stop:
            break
        for step in step_sequence:
            if motor_stop:
                break
            pin1.value = step[0]
            pin2.value = step[1]
            pin3.value = step[2]
            pin4.value = step[3]
            time.sleep(0.0012)

def motor_backward(steps):
    global motor_stop
    motor_stop = False
    for _ in range(steps):
        if motor_stop:
            break
        for step in reversed(step_sequence):
            if motor_stop:
                break
            pin1.value = step[0]
            pin2.value = step[1]
            pin3.value = step[2]
            pin4.value = step[3]
            time.sleep(0.0012)

def open_curtain():
    global curtain_state
    if curtain_state != "open":
        print("Opening curtain...")
        t = threading.Thread(target=motor_forward, args=(3800,))
        t.start()
        curtain_state = "open"
        save_state("open")
    else:
        print("Curtain already open, doing nothing")

def close_curtain():
    global curtain_state
    if curtain_state != "closed":
        print("Closing curtain...")
        t = threading.Thread(target=motor_backward, args=(3800,))
        t.start()
        curtain_state = "closed"
        save_state("closed")
    else:
        print("Curtain already closed, doing nothing")

def scheduler():
    while True:
        now = datetime.now()
        day = now.strftime("%A").lower()
        current_time = now.strftime("%H:%M")
        schedule = load_schedule()
        if day in schedule and schedule[day]["enabled"]:
            if current_time == schedule[day]["open"]:
                open_curtain()
            elif current_time == schedule[day]["close"]:
                close_curtain()
        time.sleep(60)

scheduler_thread = threading.Thread(target=scheduler, daemon=True)
scheduler_thread.start()

@app.route('/')
def index():
    schedule = load_schedule()
    return render_template('index.html', schedule=schedule, state=curtain_state)

@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    schedule = load_schedule()
    data = request.json
    day = data['day']
    schedule[day]['open'] = data['open']
    schedule[day]['close'] = data['close']
    schedule[day]['enabled'] = data['enabled']
    save_schedule(schedule)
    return jsonify({"status": "saved"})

@app.route('/manual', methods=['POST'])
def manual():
    action = request.json['action']
    if action == 'open':
        open_curtain()
    elif action == 'close':
        close_curtain()
    return jsonify({"status": "done", "state": curtain_state})

@app.route('/stop', methods=['POST'])
def stop():
    global motor_stop
    motor_stop = True
    pin1.value = 0
    pin2.value = 0
    pin3.value = 0
    pin4.value = 0
    return jsonify({"status": "stopped"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
