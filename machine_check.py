from queue import Queue
import threading

from Sensors import Ultrasonic
from Sensors import Camera

class Machine_Check(threading.Thread):
    def __init__(self, dist_to_machine, machine_status):
        threading.Thread.__init__(self)

        self.ultrasonic_queue = Queue()
        self.camera_queue = Queue()

        self.ultrasonic_1 = Ultrasonic(12, 16)
        self.camera = Camera(self.camera_queue)
        self.dist_to_machine = dist_to_machine
        self.machine_status = machine_status

        self.camera.start()

    def run(self):
        while True:
            ultrasonic_status = self.ultrasonic_queue.get()
            lcd_value = self.camera_queue.get()

