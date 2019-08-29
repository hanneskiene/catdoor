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
        self.p.start(2.5)
        self.idle()

    def idle(self):
        time.sleep(0.1) # wait till servo in position
        self.p.ChangeDutyCycle(0)

    def open(self, t = 10):
        print("Servo open")
        for i in range(70):
            self.p.ChangeDutyCycle(2.5+(i/10)) #2.5 to 12.5
            time.sleep(0.05)
        self.idle()
        #Thread(target=self.closeIn, args=[t]).start()

    def close(self):
        print("Servo close")
        for i in range(70):
            self.p.ChangeDutyCycle(8.5-(i/10)) #2.5 to 12.5
            time.sleep(0.05)
        self.idle()

    def __del__(self):
        gpio.cleanup()


