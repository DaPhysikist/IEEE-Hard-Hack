import threading

from Sensors import Ultrasonic

class Machine_Check(threading.Thread):
    def __init__(self, dist_to_machine, machine_status):
        threading.Thread.__init__(self)

        self.ultrasonic_1 = Ultrasonic(12, 16)
        self.dist_to_machine = dist_to_machine
        self.machine_status = machine_status

    def run(self):
        dist1 = self.ultrasonic_1.distance()
        if (dist1 > (self.dist_to_machine + 5)):
            self.out.put({'Open':True})
        else:
            self.out.put({'Open':False})
