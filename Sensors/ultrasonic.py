#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

class Ultrasonic():
    def __init__(TRIG, ECHO, self):
        self.TRIG = TRIG
        self.ECHO = ECHO

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)

    def distance(self):
        GPIO.output(self.TRIG, 0)
        time.sleep(0.000002)
        GPIO.output(self.TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, 0)

        while GPIO.input(self.ECHO) == 0:
            a = 0
            time1 = time.time()

        while GPIO.input(self.ECHO) == 1:
            a = 1
            time2 = time.time()

        during = time2 - time1
        return during * 340 / 2 * 100

    def destroy(self):
        GPIO.cleanup()