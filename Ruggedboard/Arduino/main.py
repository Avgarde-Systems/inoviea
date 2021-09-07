import serial

import time

ser = serial.Serial('/dev/ttymxc2',115200)

while True:
 ser.write(b'0')
 print('On')
 time.sleep(1)
 ser.write(b'9')
 print('Off')
 time.sleep(1)
