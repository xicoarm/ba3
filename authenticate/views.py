from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import EditVehicleForm, SignUpForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth.models import User
from authenticate.models import Vehicle
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import RPi.GPIO as GPIO
import time
import pymodbus
from pymodbus.pdu import ModbusRequest

from pymodbus.client import ModbusSerialClient as ModbusClient 
#initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer
from datetime import datetime

def home(request):
    return render(request, 'authenticate/home.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully')
            return redirect('home')
        else:
            messages.warning(request, "Username or Password is incorrect !!")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            form = SignUpForm(request.POST)
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'authenticate/register.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'authenticate/edit_profile.html', context)

def edit_vehicle(request):
    if request.method == 'POST':
        form = EditVehicleForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle Updated Successfully")
            return redirect('home')
    else:
        form = EditVehicleForm
    context = {
        'form': form,
    }
    return render(request, 'authenticate/edit_vehicle.html', context)

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Changed Successfully")
            return redirect('home')
    else:
        form = ChangePasswordForm(user=request.user)
        print(form)
    context = {
        'form': form,
    }
    return render(request, 'authenticate/change_password.html', context)


def start_charging(request):

    if not request.user.vehicle.is_charging:

        request.user.vehicle.start_session = datetime.now()

        #start script to turn on the Switch
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(21, GPIO.OUT)
        
        try:
            #while True:
                GPIO.output(21, GPIO.HIGH)
                print("pin is on")

                #time.sleep(2)
                
                #GPIO.output(21, GPIO.LOW)
                #print('pin is off')
                #time.sleep(2)

        except:      
            messages.MessageFailure(request, "Error while starting the charging session")
            return redirect('home')   

        else:
            messages.success(request, "Charging session activated")
            status = request.user.vehicle
            status.is_charging  = True
            status.save()
            return render(request, 'authenticate/home.html')

        finally: 
            GPIO.cleanup()
	



    #script_response = switch.py --chdir /users/scripts

    #start the script to periodically check the meter values

    #if charging started


    #if charging could not be started
    # return render(request, "users/not_charging.html")



def stop_charging(request):

    if request.user.vehicle.is_charging:

        now = request.user.vehicle.stop_session = datetime.now()
        then = datetime.strptime(request.user.vehicle.start_session, '%Y-%m-%d %H:%M:%S.%f')

        tdelta =  now - then
        seconds = tdelta.total_seconds()

        request.user.vehicle.total_time_last_session = seconds


        # kw count...
        #kw_count



        #start script to turn on the Switch
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(21, GPIO.OUT)
        
        try:
            #while True:
                #GPIO.output(21, GPIO.HIGH)
                #print("pin is on")

                #time.sleep(2)
                
                GPIO.output(21, GPIO.LOW)
                
                print('pin is off')
                #time.sleep(2)

        except:      
            messages.MessageFailure(request, "Error while starting the charging session")
            return redirect('home')   

        else:
            messages.success(request, "Charging session deactivated")
            status = request.user.vehicle
            status.is_charging  = False
            status.save()
            return render(request, 'authenticate/home.html')

        finally: 
            GPIO.cleanup()




def stats(request):

    #if still charging 

    #count= the number of registers to read
    #unit= the slave unit this request is targeting
    #address= the starting address to read from

    client = ModbusClient(method = 'rtu', port='/dev/ttyUSB1', stopbits = 1, bytesize = 8, parity = 'E' , baudrate= 9600)

    #Connect to the serial modbus server
    connection = client.connect()
    print(connection)

    #Starting add, num of reg to read, slave unit.
    coil = client.read_holding_registers(0x0140,2,unit=1)# address, count, slave address

    for t in range(2):
        print(coil.getRegister(t))
        if t == 1:
            request.consumption = coil.getRegister(t)

    #Closes the underlying socket connection
    client.close()
    
    

    #else charging finished
    return render(request, 'authenticate/stats.html') 



def kw_count():

    #if still charging 

    #count= the number of registers to read
    #unit= the slave unit this request is targeting
    #address= the starting address to read from

    client = ModbusClient(method = 'rtu', port='/dev/ttyUSB1', stopbits = 1, bytesize = 8, parity = 'E' , baudrate= 9600)

    #Connect to the serial modbus server
    connection = client.connect()
    print(connection)

    #Starting add, num of reg to read, slave unit.
    coil = client.read_holding_registers(0x0140,2,unit=1)# address, count, slave address

    for t in range(2):
        print(coil.getRegister(t))
        if t == 1:
            consumption = coil.getRegister(t)

    #Closes the underlying socket connection
    client.close()
    
    

    #else charging finished
    return consumption