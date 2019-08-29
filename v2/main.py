from telegram_handler import TelHandler
from servo_handler import ServoHandler
from pir_handler import PirHandler
from threading import Lock
import RPi.GPIO as gpio
import cv2
import time
import sys

from picamera import PiCamera

def mainApp():
    th = TelHandler()
    servo = ServoHandler()
    pir = PirHandler()

    lock = Lock()

    def picam():
        camera=PiCamera()
        time.sleep(2)
        camera.capture("img.jpg")
        camera.close()

    def usbcam():
        cam = cv2.VideoCapture(0)
        s, im = cam.read()
        cv2.imwrite('img.jpg', im)
        cam.release()

    def onShow(th):
        lock.acquire()
        try:
            print("main show")
            picam()
            th.sendPhoto('img.jpg')
            th.sendCmdList()
        finally:
            lock.release()

    def onOpen(th):
        print("main open")
        servo.open()
        th.notifyOpen()

    def onPir():
        th.text('Movement detected')
        onShow(th)

    th.setCallbackShow(onShow)
    th.setCallbackOpen(onOpen)
    th.startListening() #call if all callbacks are initialized

    pir.setCallback(onPir)
    print("Loading Complete")
    while(True):
        pir.tick()
        time.sleep(2)
#
# entry
#   main loop supervisor
#
while(True):
    try:
        mainApp()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        time.sleep(2)
    finally:
        gpio.cleanup()


