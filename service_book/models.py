from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Car(models.Model):
    brand = models.ManyToManyField(Brand)
    model = models.CharField(max_length=100)
    prod_year = models.IntegerField()
    miliage = models.IntegerField()
    vin = models.CharField(max_length=20, unique=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Owner'
    )

    def __str__(self):
        return f"{self.model} - {self.owner}"


class ServiceRecord(models.Model):
    SERVICE_ACTIONS = [
        ('interval_service', 'Interval Service'),
        ('diagnostics', 'Diagnostic'),
        ('tire_service', 'Tire Service'),
        ('repair_service', 'Repair'),
        ('other_service', 'Other'),
    ]

    date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='User'
    )
    place = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_ACTIONS)
    description = models.TextField()

    def __str__(self):
        return f"{self.car} - {self.get_service_type_display()}"
