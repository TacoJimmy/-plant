import sys
import time
import serial

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import paho.mqtt.client as mqtt
import random
import json
import datetime
import codecs

import schedule
import time


def on_AC_publish(AC_infor):
    try:
        client = mqtt.Client()
        client.username_pw_set("CaMBi9SXcyjgPFJ9N6GU","xxxx")
        client.connect('thingsboard.cloud', 1883, 60)
        payload = {'soil_Temp' : AC_infor[0], 'soil_WC' : AC_infor[1], 'soil_EC' : AC_infor[2], 'Air_Temp' : AC_infor[3],'Air_Humi' : AC_infor[4]}
        #payload = {'Temperature' : AC_infor[0] , 'humidity' : AC_infor[1],'CO2':AC_infor[2], 'settemp':AC_infor[3], 'compressor':AC_infor[4]}
        client.publish("v1/devices/me/telemetry", json.dumps(payload))
        time.sleep(1)
    except:
        print('error')


def AC_infor(PORT):
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        soil_read = master.execute(1, cst.READ_HOLDING_REGISTERS, 1, 4)
        time.sleep(1)
        air_read = master.execute(2, cst.READ_HOLDING_REGISTERS, 1090, 4)
        time.sleep(1)
        contain_infor = soil_read[0]/100,soil_read[1]/100,soil_read[2],air_read[0]/100,air_read[3]/100
        return (contain_infor)

    except:
        contain_infor = [0,0,0,0,0]

        return (contain_infor)
    else:
        contain_infor = [0,0,0,0,0]

        return (contain_infor)

if __name__ == '__main__':
    while True:
        # read soil sensor data
        AC_contain = AC_infor('/dev/ttyS1')
        if AC_contain != 0:
            on_AC_publish(AC_contain)
        #print (AC_contain)
        time.sleep(120)


