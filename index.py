import cv2
import sys
from flask import Flask, render_template, request
from Sensors import Ultrasonic
from machine_check import Machine_Check

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle file upload and extract number from image
        image = request.files['file']
        return render_template('index.html', number=number)
    else:
        return render_template('index.html')
        

if __name__ == '__main__':
    if sys.argc == 2:
        dist_to_machine = int(sys.argv[1])
        machine_status = 'Available'
        mc_thread = Machine_Check(dist_to_machine, machine_status)
        app.run(debug=True)
        mc_thread.start()
    