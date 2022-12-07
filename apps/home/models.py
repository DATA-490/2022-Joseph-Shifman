from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CarModel(models.Model):
    year = models.IntegerField()
    make = models.CharField(
        max_length=100
    )
    model = models.CharField(
        max_length=100
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    count = models.IntegerField(
        "Number of recalls"
    )

    def __str__(self):
        return str(self.year) + " " + self.make + " " + self.model

    class Meta:
        unique_together = ("user","year","make","model")