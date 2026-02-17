from django.db import models
from django.contrib.auth.models import User

from Resource.models import Resource
# Create your models here.


class Status(models.Model):
    name = models.CharField(max_length=50)
    verbose_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.verbose_name}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True, verbose_name="Об'єкт")
    start_time = models.DateTimeField(verbose_name="Заброньовано від")
    end_time = models.DateTimeField(verbose_name="Заброньовано до")
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, verbose_name="Статус", default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    description = models.CharField(max_length=255, verbose_name="Додаткова інформація", null=True, blank=True, default=None)
    reason = models.CharField(max_length=255, verbose_name="інформація від адміністрації", null=True, blank=True, default=True)

    def __str__(self):
        return f"{self.resource.name}|{self.resource.type}: {self.start_time}-{self.end_time}: {self.status.verbose_name}"
    

class Action(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"Назва дії: {self.name}"


class BookingLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.ForeignKey(Action, on_delete=models.SET_NULL, null=True, verbose_name="Дія")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата й час події")

    def __str__(self):
        return f"{self.timestamp}: {self.booking.resource.name}-{self.user.username}-{self.action.name}"
