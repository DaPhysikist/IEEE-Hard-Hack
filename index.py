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
        
import time

@app.route('/status')
def get_status():
    global machine_status
    return jsonify({'status': machine_status})

def update_status():
    global machine_status
    while True:
        result = camera.get_lcd_value() # Get the machine status from the blah.py module
        machine_status = 'available' if not result else result  # Update the machine status
        time.sleep(3)

if __name__ == '__main__':
    if sys.argc == 2:
        try:
            dist_to_machine = int(sys.argv[1])
            mc_thread = Machine_Check(dist_to_machine, machine_status)
            update_thread = threading.Thread(target=update_status)
            update_thread.start()
            app.run(debug=True)
        except KeyboardInterrupt:
            update_thread.ultrasonic_1.destroy()
            update_thread.join()
    