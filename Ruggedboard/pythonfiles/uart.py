import serial
from time import sleep

ser = serial.Serial ("/dev/ttymxc1", 115200,timeout=3)    #Open port with baud rate

ser.write(str.encode('+++'))

Flag = True
while Flag:
    i = input("Enter the address of the relay")
    # i = 1,2,3,4 respectively for relay
    # press space bar to exit
    if i == ' ':
        Flag = False
    else:
        ser.write(str.encode(i))
        Flag = True
ser.close()

