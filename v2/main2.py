from telegram_handler import TelHandler
from servo_handler import ServoHandler
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
        self.camera = PiCamera()
        self.camera.framerate = 1
        time.sleep(2)
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g

        self.th_lock = Lock()
        self.cam_lock = Lock()

        self.th.setCallbackShow(self.onShow)
        self.th.setCallbackOpen(self.onOpen)
        self.th.setCallbackClose(self.onClose)
        self.th.startListening()
        self.th.text("Started")
        self.sendPhoto()
        print("Ready")

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
            try:
                self._run()
            except KeyboardInterrupt:
                break

    def _run(self):
        score_out = 0.0
        self.cam_lock.acquire()
        try:
            self.output2 = self.output
            with picamera.array.PiRGBArray(self.camera) as self.output:
                self.camera.capture(self.output, 'rgb')
                gray = cv2.cvtColor(output.array, cv2.COLOR_RGB2GRAY)
                gray2 = cv2.cvtColor(output2.array, cv2.COLOR_RGB2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
                # dif = gray2 - gray
                # dif_abs = np.sum(dif)
                # print("Difference:" + str(dif_abs))
                # if(dif_abs > 58000000):
                (score, diff) = compare_ssim(gray, gray2, full=True)
                # print("SSIM: {}".format(score))
                score_out = score
        finally:
            self.cam_lock.release()
            time.sleep(2)

        if(score_out < 0.93):
            self.th.text("Movement")
            self.sendPhoto()
            


while(True):
    try:
        app = MainController()
        app.run()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        time.sleep(10)
    finally:
        GPIO.cleanup()

