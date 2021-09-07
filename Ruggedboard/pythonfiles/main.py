import time
import serial

ser = serial.Serial(
 port='/dev/ttymxc1',
 baudrate = 115200,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)
counter=0

while 1:
 x=input("enter the value ")
 print(x)
# ser.write(b'x')
 ser.write(str(x).encode('utf-8'))
# ser.write(x.encode())

