from telegram_handler import TelHandler
from servo_handler import ServoHandler
from pir_handler import PirHandler
from threading import Lock
import RPi.GPIO as GPIO
import cv2
import time
import sys
from threading import Lock
from picamera import PiCamera
import picamera.array
import numpy as np
from skimage.measure import compare_ssim

class MainController:
    def __init__(self):
        self.th = TelHandler()
        self.servo = ServoHandler()
        self.tof = PirHandler()
        self.camera = PiCamera()
        self.camera.framerate = 5
        
        self.output_raw = picamera.array.PiRGBArray(self.camera)

        self.calibrate()

        self.counter = 0

        self.th_lock = Lock()
        self.cam_lock = Lock()

        self.th.setCallbackShow(self.onShow)
        self.th.setCallbackOpen(self.onOpen)
        self.th.setCallbackClose(self.onClose)
        self.th.startListening()
        self.th.text("Started")
        self.sendPhoto()
        print("Ready")
    
    def calibrate(self):
        #self.camera.close()
        #time.sleep(1)
        #self.camera = PiCamera()
        #self.camera.framerate = 10
        #self.output_raw = picamera.array.PiRGBArray(self.camera)

        self.camera.exposure_mode = 'auto'
        self.camera.awb_mode = 'auto'
        #self.camera.iso = 0
        #self.camera.shutter_speed = 0
        time.sleep(2)
        #s = self.camera.exposure_speed
        #self.camera.exposure_mode = 'off'
        #self.camera.shutter_speed = s
        #g = self.camera.awb_gains
        #self.camera.awb_mode = 'off'
        #self.camera.awb_gains = g

        #self.camera.capture(self.output_raw, 'rgb')
        #self.old_image = self.output_raw.array
        #self.output_raw.truncate(0)

    def capture(self):
        self.cam_lock.acquire()
        try:
            self.camera.capture('img.jpg')
        finally:
            self.cam_lock.release()

    def sendPhoto(self):
        self.th_lock.acquire()
        try:
            print("Sending Photo")
            self.capture()
            self.th.sendPhoto('img.jpg')
            self.th.sendCmdList()
        finally:
            self.th_lock.release()

    def onShow(self, t):
        self.sendPhoto()

    def onOpen(self, t):
        self.servo.open()
#        self.th.notifyOpen()

    def onClose(self, t):
        self.servo.close()

    def run(self):
        while(True):
            if(self.tof.get_distance() < 260):
                self.sendPhoto()
            time.sleep(3)
            
try:
    app = MainController()
    app.run()
except KeyboardInterrupt:
    sys.exit()
except Exception as e:
    print(e)
finally:
    GPIO.cleanup()