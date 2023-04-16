import threading

from Sensors import Ultrasonic

class Machine_Check(threading.Thread):
    def __init__(self, dist_to_machine, dist_to_obstruction, out):
        threading.Thread.__init__(self)

        self.ultrasonic_1 = Ultrasonic(12, 16)
        self.ultrasonic_2 = Ultrasonic(18, 22)
        self.dist_to_machine = dist_to_machine
        self.dist_to_obstruction = dist_to_obstruction
        self.out = out

    def run(self):
        dist1 = self.ultrasonic_1.distance()
        dist2 = self.ultrasonic_2.distance()
        if (dist1 > (self.dist_to_machine - 15) and dist1 < (self.dist_to_machine - self.dist_to_obstruction)) or (dist2 > (self.dist_to_machine - 15) and dist2 < (self.dist_to_machine - self.dist_to_obstruction)):
            self.out.put({'Blocked':True})
        else:
            self.out.put({'Blocked':False})