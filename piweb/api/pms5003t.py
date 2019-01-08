'''
https://github.com/Thomas-Tsai/pms3003-g3
'''

import serial
from collections import OrderedDict

class Sensor():
    def __init__(self, tty = '/dev/ttyS0'):
        self.tty = tty
    
    def conn(self, device):
        self.serial = serial.Serial(device, baudrate = 9600)

    def read_word(self, data, idx):
        return int(data[idx] + data[idx + 1], 16)

    def read_data(self):
        data = self.serial.read(32)
        data = ["{:02X}".format(d) for d in data]
        
        if data[0] != '42' or data[1] != '4D':
            return None
        
        res = OrderedDict()
        res['pm1_cf'] = self.read_word(data, 4)
        res['pm25_cf'] = self.read_word(data, 6)
        res['pm10_cf'] = self.read_word(data, 8)
        res['pm1'] = self.read_word(data, 10)
        res['pm25'] = self.read_word(data, 12)
        res['pm10'] = self.read_word(data, 14)

        res['temperature'] = self.read_word(data, 24) / 10
        res['humidity'] = self.read_word(data, 26) / 10
        return res

    def read(self):
        self.conn(self.tty)
        data = self.read_data()
        self.serial.close()
        return data

if __name__ == '__main__':
    '''
    Test code
    '''
    sensor = Sensor()
    data = sensor.read()
    print(data)