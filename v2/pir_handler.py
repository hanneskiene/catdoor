import RPi.GPIO as GPIO
import time

class PirHandler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        PIR_PIN = 23
        GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(24, GPIO.OUT)
        GPIO.output(24, 1)
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=self.MOTION)
        self.last_time = time.time()

    def MOTION(self, pin):
        this_time = time.time()
        elapsed = this_time - self.last_time
        self.last_time = this_time
        if elapsed > 115 and elapsed < 125:
            print(".")
        else:
            print("Motion")
            self.callback()

    def setCallback(self, cb):
        self.callback = cb

    def __del__(self):
        GPIO.cleanup() 
