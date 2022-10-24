import requests
import time
import shutil
import os
from my_site.anpr import anpr



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