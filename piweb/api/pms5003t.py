'''
https://github.com/Thomas-Tsai/pms3003-g3
'''

import serial
import time
import sys
from struct import *

class Sensor():
    def __init__(self, tty = '/dev/ttyS0', debug = True):
        self.debug = debug
        self.edian = sys.byteorder
        self.tty = tty
    
    def conn(self, device):
        self.serial = serial.Serial(device, baudrate = 9600)
    
    def check_keyword(self):
        while True:
            token = self.serial.read()
            token_hex = token.encode('hex')
            if token_hex == '42':
                token = self.serial.read()
                token_hex = token.encode('hex')
                return token_hex == '4d'
            else:
                return False

    def read_word(self, data, idx):
        idx *= 4
        return int(data[idx : idx + 4], 16)

    def read_data(self):
        data = self.serial.read(32)
        data = data.encode('hex')
        if self.debug:
            print(data)
        
        res = {}
        res['pm1_cf'] = self.read_word(data, 1)
        res['pm25_cf'] = self.read_word(data, 2)
        res['pm10_cf'] = self.read_word(data, 3)
        res['pm1'] = self.read_word(data, 4)
        res['pm25'] = self.read_word(data, 5)
        res['pm10'] = self.read_word(data, 6)

        res['temperature'] = self.read_word(data, 11) / 10
        res['humidity'] = self.read_word(data, 12) / 10
        return res

    def read(self):
        self.conn(self.tty)
        if self.check_keyword():
            return self.read_data()
        return None

    def close(self):
        self.serial.close()

if __name__ == '__main__':
    '''
    Test code
    '''
    sensor = Sensor()
    data = sensor.read()
    print(data)
    sensor.close()