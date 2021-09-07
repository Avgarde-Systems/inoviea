import paho.mqtt.client as mqtt
import time
import serial
import pycrc

 # ser.write(str.encode(x))


def on_connect(client, userdata, flags, rc):
    print(rc)
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the IoT/topic topic
    client.subscribe("IoT/topic")
    



# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload)
    mode = input("Enter 1 for Modbus, 2 for Remote Relay")
    if mode == '2':
        ser = serial.Serial(
        port='/dev/ttymxc1',baudrate = 115200,parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=1)
        ser.write(msg.payload)
    elif mode == '1':
        s = serial.Serial("/dev/ttymxc5",9600)
        #s = serial.Serial("COM18",115200)
        cmd = [0, 0, 0, 0, 0, 0, 0, 0]
        
        cmd[0] = 0x01  #Device address
        cmd[1] = 0x05  #command
        
        while True:
            for i in range(8):
                cmd[2] = 0
                cmd[3] = i
                cmd[4] = 0x5A
                cmd[5] = 0
                crc = pycrc.ModbusCRC(cmd[0:6])
                cmd[6] = crc & 0xFF
                cmd[7] = crc >> 8
                print(cmd)
                s.write(cmd)
                time.sleep(0.2)
                
            for i in range(8):
                cmd[2] = 0
                cmd[3] = i
                cmd[4] = 0
                cmd[5] = 0
                crc = pycrc.ModbusCRC(cmd[0:6])
                cmd[6] = crc & 0xFF
                cmd[7] = crc >> 8
                print(cmd)
                s.write(cmd)
                time.sleep(0.2)
        
       
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the SBC is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('IoT/status', b'{"status": "Off"}')

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("broker.emqx.io", 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()




