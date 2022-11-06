import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')
import django
django.setup()
import authenticate.utils as utils
import threading

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
import requests
from pprint import pprint
from authenticate.utils import get_plot, get_plot_data_task



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




def check_for_vehicle_plates_recognizer():

    url= 'http://172.20.10.5'
    module_path = os.path.dirname(os.path.realpath(__file__))
    desired_location = str(module_path) + "/temp_snapshots"
    counter2 = 0
    print('startttttttttttttttttttttttttttttt')
    #while not charging or no car detected
    while True:

        charging_now = Vehicle.objects.all().filter(is_charging=True)

        if not charging_now and counter2 < 8:

            time_stemp = int(round(time.time()* 1000))
            output_path = os.path.join(desired_location, 'temp_snapshot_' + str(time_stemp) + '.png')
            img_name = ('/temp_snapshot_' + str(time_stemp) + '.png')
            print('11111111111111111111111111')
            print(output_path)

            r = requests.get(f'{url}/capture?id={int(round(time.time()*1000))}', stream=True)

            with open(output_path, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)

            #start the plate recognition process    
            #print(pic_name)
            
            #plate_nr = utils.platerecognizer(img_name) 
            plate_nr= 'zh672653'

            print(plate_nr)

            charging_vehicle = Vehicle.objects.all().filter(vehicle_id=plate_nr)
            user = User.objects.filter(vehicle = charging_vehicle.first())

            if charging_vehicle:
                print('44444444444444444444')
                charging_vehicle.update(is_charging = True)

                charging_vehicle.update(start_session = datetime.now())

                #start script to turn on the Switch
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(21, GPIO.OUT)
                GPIO.output(21, GPIO.HIGH)
                print("pin is on")



        else:
        
            charging_now = Vehicle.objects.all().filter(is_charging=True)

            print('555555555555555')    

            time_stemp = int(round(time.time()* 1000))
            output_path = os.path.join(desired_location, 'temp_snapshot_' + str(time_stemp) + '.png')
            img_name = ('/temp_snapshot_' + str(time_stemp) + '.png')

            r = requests.get(f'{url}/capture?id={int(round(time.time()*1000))}', stream=True)
            
            with open(output_path, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)


            #captured_plate_nr = utils.platerecognizer(img_name) 
            
            captured_plate_nr= 'zh672653'

            if counter2 > 8:
                captured_plate_nr= 'zh67263'
                
            counter2 = counter2 + 1    

            print(counter2)
            authenticated_charging_vehicle_id = charging_now.first().vehicle_id
            print(captured_plate_nr)

            if captured_plate_nr != authenticated_charging_vehicle_id:

                charging_now = Vehicle.objects.all().filter(is_charging=True).first()
                
                print('00000000000000000')      

                id = Vehicle.objects.all().filter(is_charging=True).first().id

                print('00000000000000000')

                b = Vehicle.objects.all().filter(id=id)

                b.update(is_charging = False)
                b.update(stop_session = datetime.now())
                

                now = datetime.strptime(b.first().stop_session, '%Y-%m-%d %H:%M:%S.%f')
                then = datetime.strptime(b.first().start_session, '%Y-%m-%d %H:%M:%S.%f')

                tdelta =  now - then
                seconds = tdelta.total_seconds()
                
            

                b.update(total_time_last_session = seconds)
                

                # kw count...
                # get all charges that are newer than start time and older than stop time

                list = Charge.objects.all().filter(snapshot_time__range=[then, now])
                kw_count = 0
                count = 0

                for item in list:
                    print('123123123123')
                    kw_count = kw_count + item.current_kw
                    count = count + 1
                
            
                if not count == 0:
                    average_kw_during_session = kw_count / count
                else:
                    average_kw_during_session = 0
                #average_kw_during_session = kw_count / 1

                b.update(total_time_last_session = seconds)
                b.update(average_count_kw_last_session = average_kw_during_session)
                print('average')
                print(average_kw_during_session)

                average_kwh_during_session = ((seconds / 3600) * average_kw_during_session) / 1000
                
                b.update(average_count_kwh_last_session = average_kwh_during_session)

                result = get_plot_data_task(b.first())
                x = result[0]
                y = result[1]

                chart = get_plot(x, y)

                b.update(plot = chart)

                print('8888888888888888888')
                print(chart)

                #start script to turn on the Switch
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(21, GPIO.OUT)
                GPIO.output(21, GPIO.LOW)
                        
                print('pin is off')
            
                break


        time.sleep(15)








def check_consumption():

    while True:

        client = ModbusClient(method = 'rtu', port='/dev/ttyUSB0', stopbits = 1, bytesize = 8, parity = 'E' , baudrate= 9600)

        #Connect to the serial modbus server
        connection = client.connect()

        #Starting add, num of reg to read, slave unit.
        coil = client.read_holding_registers(0x0140,2,slave=1)# address, count, slave address

        for t in range(2):
            if t == 1:
                consumption = coil.getRegister(t)

        #Closes the underlying socket connection
        client.close()


        publisher = Charge(current_kw=consumption, snapshot_time=datetime.now())
        publisher.save()
        
        print('checking consumption11111111111111111111111')
        print(datetime.now())

        time.sleep(30)

        #else charging finished


thread = threading.Thread(target= check_consumption)
#thread.start()

thread2 = threading.Thread(target= check_for_vehicle_plates_recognizer)
#thread2.start()