from celery import shared_task
from django.core.mail import EmailMessage
import requests
import pandas as pd
from . import models

@shared_task()
def send_recall_emails():
    for car in models.CarModel.objects.all():
        count = car.count
        make = car.make
        model = car.model
        year = car.year
        url = "https://api.nhtsa.gov/recalls/recallsByVehicle?make=" + make + "&model=" + model + "&modelYear=" + str(year)
        r = requests.get(url)
        recallList = pd.read_json(r.text)
        c_res = int(recallList.Count[0])
        if count != c_res:
            email = EmailMessage(
                'A Vehicle In your Garage has New Recalls',
                'Hello,\n\nThe NHTSA has released a recall for one of the vehicles saved in your garage on the Vehicle Safety Dashboard.\nNavigate to 35.227.169.250 to view it.\n\n-Vehicle Safety Dashboard\n\nIf you would like to be removed from this list, reply back to sender.',
                to=[car.user.email]
            )
            email.send()
            car.count = c_res
            car.save()
