'''
| Offset | Definition               | Data                                                                 |
| ------ |:------------------------:| --------------------------------------------------------------------:|
| 0      | Start byte 1             | Fixed 0x42 (char "B")                                                |
| 1      | Start byte 2             | Fixed 0x4D (char "M")                                                |
| 2      | Frame length (16 bits)   | Length = 14 * 2                                                      |
| 4      | Data 1 (16 bits)         | The PM1.0 concentration (CF = 1, standard particle), unit μg/m³      |
| 6      | Data 2 (16 bits)         | The PM2.5 concentration (CF = 1, standard particle), unit μg/m³      |
| 8      | Data 3 (16 bits)         | The PM10 concentration (CF = 1, standard particle), unit μg/m³       |
| 10     | Data 4 (16 bits)         | The PM1.0 concentration (generic atmospheric conditions), unit μg/m³ |
| 12     | Data 5 (16 bits)         | The PM2.5 concentration (generic atmospheric conditions), unit μg/m³ |
| 14     | Data 6 (16 bits)         | The PM10 concentration (generic atmospheric conditions), unit μg/m³  |
| 16     | Data 7 (16 bits)         | The number of particles with diameter >= 0.3 μm in 0.1 liter of air  |
| 18     | Data 8 (16 bits)         | The number of particles with diameter >= 0.5 μm in 0.1 liter of air  |
| 20     | Data 9 (16 bits)         | The number of particles with diameter >= 1.0 μm in 0.1 liter of air  |
| 22     | Data 10 (16 bits)        | The number of particles with diameter >= 2.5 μm in 0.1 liter of air  |
| 24     | Data 11 (16 bits)        | Temperature. Note: Real temperature = value / 10                     |
| 26     | Data 12 (16 bits)        | Humidity. Note: Real humidity = value / 10                           |
| 28     | Data 13 (high 8 bits)    | Version No.                                                          |
| 29     | Data 13 (low 8 bits)     | Error No.                                                            |
| 30     | Data checksum (16 bits)  | Checksum = byte 0 + byte 1 + ... + byte 29                           |
'''

import serial
from collections import OrderedDict

class Sensor():
    def __init__(self, tty = '/dev/ttyS0'):
        self.tty = tty
    
    def open(self):
        self.serial = serial.Serial(self.tty, baudrate = 9600)

    def close(self):
        self.serial.close()

    def read_bytes(self, data, idx, size = 2):
        return int("".join(data[idx : idx + size]), 16)

    def read(self):
        data = self.serial.read(32)
        data = ["{:02X}".format(d) for d in data]
        
        if data[0] != '42' or data[1] != '4D':
            return None
        
        res = OrderedDict()
        res['pm1_cf'] = self.read_bytes(data, 4)
        res['pm25_cf'] = self.read_bytes(data, 6)
        res['pm10_cf'] = self.read_bytes(data, 8)
        res['pm1'] = self.read_bytes(data, 10)
        res['pm25'] = self.read_bytes(data, 12)
        res['pm10'] = self.read_bytes(data, 14)

        res['temperature'] = self.read_bytes(data, 24) / 10
        res['humidity'] = self.read_bytes(data, 26) / 10
        return res
        
if __name__ == '__main__':
    '''
    Test code
    '''
    sensor = Sensor()
    sensor.open()
    data = sensor.read()
    sensor.close()
    print(data)