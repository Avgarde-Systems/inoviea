import paho.mqtt.client as mqtt
import time
import serial

 # ser.write(str.encode(x))


def on_connect(client, userdata, flags, rc):
    print(rc)
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe("IoT/topic")

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload)
    ser = serial.Serial(
        port='/dev/ttymxc1',baudrate = 115200,parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=1)
 
    ser.write(msg.payload)
    return msg.payload

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('IoT/status', b'{"status": "Off"}')

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("broker.emqx.io", 1883, 60)
print(client.on_connect)
# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
