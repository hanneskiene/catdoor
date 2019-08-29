import time
import VL53L0X

class PirHandler:
    def __init__(self):
        self.tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
        self.tof.open()
        self.tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

    def tick(self):
        dist = self.tof.get_distance()
        print(dist)
        if( dist < 300 and dist > 100 ):
            self.callback()

    def setCallback(self, cb):
        self.callback = cb

    def __del__(self):
        self.tof.stop_ranging()
        self.tof.close()
