#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

TRIG = 12
ECHO = 16

class Ultrasonic():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)

        try:
            self.loop()
        except:
            self.destroy()

    def distance(self):
        GPIO.output(TRIG, 0)
        time.sleep(0.000002)
        GPIO.output(TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG, 0)

        while GPIO.input(ECHO) == 0:
            a = 0
            time1 = time.time()

        while GPIO.input(ECHO) == 1:
            a = 1
            time2 = time.time()

        during = time2 - time1
        return during * 340 / 2 * 100

    def loop(self):
        while True:
            dis = self.distance()
            print (dis, 'cm')
            time.sleep(0.3)

    def destroy(self):
        GPIO.cleanup()