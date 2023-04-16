import threading

from Sensors import Ultrasonic
from Sensors import Camera

class Machine_Check(threading.Thread):
    def __init__(self, dist_to_machine, machine_status):
        threading.Thread.__init__(self)

        self.ultrasonic_1 = Ultrasonic(12, 16)
        self.camera = Camera()
        self.dist_to_machine = dist_to_machine
        self.machine_status = machine_status

        self.camera.start()

    def run(self):
        while True:
            dist1 = self.ultrasonic_1.distance()
            lcd_value = self.camera.get_lcd_value()

            if (dist1 > (self.dist_to_machine + 5)):
                self.out.put({'Open':True})
            else:
                self.out.put({'Open':False})
