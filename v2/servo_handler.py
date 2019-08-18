import RPi.GPIO as gpio
import time

import threading
from threading import Thread

class ServoHandler:
    pin = 18

    def __init__(self):
        print("Servo Init")
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin, gpio.OUT)
        self.p = gpio.PWM(self.pin, 50)
        self.p.start(10)
        self.idle()

    def idle(self):
        time.sleep(1) # wait till servo in position
        self.p.ChangeDutyCycle(0)

    def open(self, t = 10):
        print("Servo open")
        self.p.ChangeDutyCycle(4) #2.5 to 12.5
        self.idle()
        Thread(target=self.closeIn, args=[t]).start()

    def closeIn(self, t):
        time.sleep(t)
        print("Servo close")
        self.p.ChangeDutyCycle(10)
        self.idle()

    def __del__(self):
        gpio.cleanup()


