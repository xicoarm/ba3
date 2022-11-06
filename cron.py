from pickle import TRUE
import requests
import time
import shutil
import os
from my_site.anpr import anpr
from django.contrib.auth.models import User
from authenticate.models import Vehicle
from authenticate.models import Charge

import RPi.GPIO as GPIO
import time
import pymodbus
from pymodbus.pdu import ModbusRequest

from pymodbus.client import ModbusSerialClient as ModbusClient 
#initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer
from datetime import datetime


def check_for_vehicle_plates():

    url= 'http://172.20.10.5'
    module_path = os.path.dirname(os.path.realpath(__file__))
    desired_location = str(module_path) + '/my_site'+ "/temp_snapshots"

    #while not charging or no car detected
    while True:

        time_stemp = int(round(time.time()* 1000))
        output_path = os.path.join(desired_location, 'temp_snapshot_' + str(time_stemp) + '.png')

        r = requests.get(f'{url}/capture?id={int(round(time.time()*1000))}', stream=True)
        with open(output_path, 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)

        #start the plate recognition process    
        #print(pic_name)
        print(os.path.join(desired_location + '/12345.png'))
        
        plate_nr = anpr(os.path.join(desired_location + '/12345.png')) 
        print(plate_nr)

        #anpr("1111.jpg")

        # check if the plate is authorized

        break
        #could check here if the status = charging and break the look


def check_consumption():

    #if still charging 

    #count= the number of registers to read
    #unit= the slave unit this request is targeting
    #address= the starting address to read from

    while True:
        client = ModbusClient(method = 'rtu', port='/dev/ttyUSB0', stopbits = 1, bytesize = 8, parity = 'E' , baudrate= 9600)

        #Connect to the serial modbus server
        connection = client.connect()
        print(connection)

        #Starting add, num of reg to read, slave unit.
        coil = client.read_holding_registers(0x0140,2,slave=1)# address, count, slave address

        for t in range(2):
            print(coil.getRegister(t))
            if t == 1:
                consumption = coil.getRegister(t)

        #Closes the underlying socket connection
        client.close()

        #if consumption > 0:

            #user_charging = Vehicle.objects.get(is_charging=True).user
            #if not user_charging:
            #    user_charging = False

        publisher = Charge(current_kw=consumption, snapshot_time=datetime.now())
        publisher.save()

        time.sleep(5)

        #else charging finished
    return

