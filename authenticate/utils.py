import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime
from .models import Charge
import requests
from pprint import pprint
import os

def get_graph():
     buffer = BytesIO()
     plt.savefig(buffer, format='png')
     buffer.seek(0)
     image_png = buffer.getvalue()
     graph = base64.b64encode(image_png)
     graph = graph.decode('utf-8')
     buffer.close()
     return graph

def get_plot(x,y):
     plt.switch_backend('AGG')
     plt.figure(figsize=(8,5))
     plt.title('Charging Stats')
     plt.plot(x,y)
     plt.xticks(rotation=45)
     plt.xlabel('time')
     plt.ylabel('kW')
     #plt.tight_layout()

     graph = get_graph()

     return graph

def get_plot_data(request):

     total_charge_time = request.user.vehicle.total_time_last_session

     now = request.user.vehicle.stop_session
     then = request.user.vehicle.start_session



    # Total time in seconds
     x=[]
     y=[]
     counter = 0
     avr_kw = 0
     list = Charge.objects.filter(snapshot_time__range=[then, now])

     # till 10min we take all 30 sec.
     if len(list) <= 20: 

          for item in list: 

               avr_kw = avr_kw + item.current_kw

               if counter == 1: 
                    y.append(avr_kw / counter) 
                    x.append(item.snapshot_time[11:19])
                    counter = 0
                    avr_kw = 0
                    continue

               counter = counter + 1  

     # from 10min to 30min. We show all 1 min
     
     elif 20 < len(list) <= 60:

          for item in list: 

               avr_kw = avr_kw + item.current_kw

               if counter == 2: 
                    y.append(avr_kw / counter) 
                    x.append(item.snapshot_time[11:19])
                    counter = 0
                    avr_kw = 0
                    continue

               counter = counter + 1          
               

     # from 30min to 2h. We show all 5 min
     elif 60 < len(list) <= 240:

          for item in list: 

               avr_kw = avr_kw + item.current_kw

               if counter == 10: 
                    y.append(avr_kw / counter) 
                    x.append(item.snapshot_time[11:19])
                    counter = 0
                    avr_kw = 0
                    continue

               counter = counter + 1    


     # from 2h to XXh. We show all 10 min
     else:
          for item in list: 

               avr_kw = avr_kw + item.current_kw

               if counter == 20: 
                    y.append(avr_kw / counter) 
                    x.append(item.snapshot_time[11:19])
                    counter = 0
                    avr_kw = 0
                    continue

               counter = counter + 1  

               #y.append(counter)
    
    # Total time in minutes 


    # Total time in hours

     #x = [1,2,3,4,5, 6, 7, 8, 9]
     
     #y = [1,2,3,4,5,6,7]


     return [x,y]





def get_plot_data_task(vehicle):

     now = vehicle.stop_session
     then = vehicle.start_session


    # Total time in seconds
     x=[]
     y=[]
     counter = 0
     avr_kw = 0
     list = Charge.objects.all().filter(snapshot_time__range=[then, now])
     

     
     # till 10min we take all 30 sec.
     if 0 < len(list) <= 20: 
          print('9999999999999999')
          for item in list: 

               avr_kw = avr_kw + item.current_kw

               if counter == 1: 
                    y.append(avr_kw / counter) 
                    x.append(item.snapshot_time[11:19])
                    counter = 0
                    avr_kw = 0
                    continue

               counter = counter + 1  

     # from 10min to 30min. We show all 1 min
     
     elif 20 < len(list) <= 60:

          for item in list: 

               avr_kw = avr_kw + item.current_kw

               if counter == 2: 
                    y.append(avr_kw / counter) 
                    x.append(item.snapshot_time[11:19])
                    counter = 0
                    avr_kw = 0
                    continue

               counter = counter + 1          
               

     # from 30min to 2h. We show all 5 min
     elif 60 < len(list) <= 240:

          for item in list: 

               avr_kw = avr_kw + item.current_kw

               if counter == 10: 
                    y.append(avr_kw / counter) 
                    x.append(item.snapshot_time[11:19])
                    counter = 0
                    avr_kw = 0
                    continue

               counter = counter + 1    


     # from 2h to XXh. We show all 10 min
     else:
          for item in list: 

               avr_kw = avr_kw + item.current_kw

               if counter == 20: 
                    y.append(avr_kw / counter) 
                    x.append(item.snapshot_time[11:19])
                    counter = 0
                    avr_kw = 0
                    continue

               counter = counter + 1  

               #y.append(counter)
    
    # Total time in minutes 


    # Total time in hours

     #x = [1,2,3,4,5, 6, 7, 8, 9]
     
     #y = [1,2,3,4,5,6,7]


     return [x,y]






















def platerecognizer(img_name):

     module_path = os.path.dirname(os.path.realpath(__file__))
     module_path = os.path.dirname(module_path)
     image_location = str(module_path) + '/my_site'+ "/temp_snapshots" + img_name

     regions = ['mx', 'ch'] # Change to your country
     print('inside recognizer 111111111111111111')
     with open(image_location, 'rb') as fp:
          response = requests.post(
               'https://api.platerecognizer.com/v1/plate-reader/',
               data=dict(regions=regions),  # Optional
     files=dict(upload=fp),
     headers={'Authorization': 'Token e81b0203dee3ab3156061cb9ca70abe4f78b884c'})

     a = response.json()
     a = a['results']

     print('1111111111111111111111111111111111111111111111111111111')
     print(a)

     if len(a) > 0:
          b = a[0]
          b = b['plate']
     else:
          b = '000'     

     return(b)    