import time
import VL53L0X

class PirHandler:
    def __init__(self):
        self.tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
        self.tof.open()
        self.tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

    def get_distance(self):
        dist = 0
        for i in range(10):
            dist = dist + self.tof.get_distance()
        dist = dist / 10
        return dist


    def __del__(self):
        self.tof.stop_ranging()
        self.tof.close()
