from django import forms
from django.contrib.auth.models import User
import datetime
from . import models

class CarForm(forms.Form):
    year = forms.IntegerField(
        label="Year",
        max_value=datetime.date.today().year+1,
        min_value=1949,
        required=True
    )
    make = forms.CharField(
        label="Make",
        max_length=100,
        required=True
    )
    model = forms.CharField(
        label="Model",
        max_length=100,
        required=True
    )
    count = forms.IntegerField(
        label="Count",
        required=True
    )

    def save(self, request):
        car_instance = models.CarModel()
        car_instance.year = self.cleaned_data["year"]
        car_instance.make = self.cleaned_data["make"]
        car_instance.model = self.cleaned_data["model"]
        car_instance.count = self.cleaned_data["count"]
        car_instance.user = request.user
        car_instance.save()
        return car_instance
