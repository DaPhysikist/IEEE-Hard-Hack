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

    def check_status(machine_status):
        return machine_status.pop()

    def run(self):
        flag_1 = False
        flag_2 = False

        while True:
            ultrasonic_status = self.ultrasonic_queue.get()
            lcd_value = self.camera_queue.get()

            if ultrasonic_status is not None:
                if ultrasonic_status == "unloaded":
                    flag_1 = True
            else:
                if flag_1 == True:
                    flag_2 = True

            if flag_1 == True and flag_2 == True:
                if "125" in lcd_value or ("25" in lcd_value and len(lcd_value) > 2):
                    self.machine_status.put("Available")
                else:
                    if int(lcd_value) > 0 or int(lcd_value) <= 53:
                        self.machine_status.put(lcd_value)
                    elif int(lcd_value) == 0:
                        self.machine_status.put("Pending Collection")
                flag_1 = False
                flag_2 = False
            else:
                if int(lcd_value) > 0 or int(lcd_value) <= 53:
                    self.machine_status.put(lcd_value)
                elif int(lcd_value) == 0:
                    self.machine_status.put("Pending Collection")
            time.sleep(3)

