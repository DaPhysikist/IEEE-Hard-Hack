import cv2
import sys
from flask import Flask, render_template, request
from Sensors import Ultrasonic
from machine_check import Machine_Check
from queue import Queue

app = Flask(__name__)
machine_status = []

@app.route('/status')
def check_status(machine_status):
    return Machine_Check.check_status()


@app.route('/')
def home(): 
    return render_template('index.html')

if __name__ == '__main__':
    try:
        dist_to_machine = int(sys.argv[1])
        mc_thread = Machine_Check(dist_to_machine, machine_status)
        app.run(debug=True)
        mc_thread.start()
    except KeyboardInterrupt:
        mc_thread.ultrasonic_1.destroy()
        mc_thread.join()
    