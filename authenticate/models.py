from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Vehicle(models.Model):

    user = models.OneToOneField(User, null= True, on_delete=models.CASCADE)
    vehicle_id = models.CharField(max_length=30)
    vehicle_model = models.CharField(max_length=31)
    is_charging = models.BooleanField(default=False)

    start_session = models.CharField(max_length=50)
    stop_session = models.CharField(max_length=50)
    total_time_last_session = models.CharField(max_length=50)
    average_count_kw_last_session = models.IntegerField()
    average_count_kwh_last_session = models.IntegerField()
    plot = models.TextField()

    def __str__(self):
        return str(self.user)



class Charge(models.Model):

    #user = models.OneToOneField(User, null= True, on_delete=models.CASCADE)
    current_kw = models.IntegerField()
    snapshot_time = models.CharField(max_length=50)

    #def __str__(self):
    #    return str(self.user)