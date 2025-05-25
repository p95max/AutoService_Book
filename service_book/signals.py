from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FuelExpense, ServiceRecord, Car
from django.db.models import Max

def update_car_miliage(car):
    if car is None:
        return
    fuel_max = FuelExpense.objects.filter(car=car).aggregate(max_miliage=Max('miliage'))['max_miliage'] or 0
    service_max = ServiceRecord.objects.filter(car=car).aggregate(max_miliage=Max('miliage'))['max_miliage'] or 0
    max_miliage = max(fuel_max, service_max)
    if car.miliage != max_miliage:
        car.miliage = max_miliage
        car.save(update_fields=['miliage'])

@receiver(post_save, sender=FuelExpense)
@receiver(post_delete, sender=FuelExpense)
def update_miliage_by_fuel_expense(sender, instance, **kwargs):
    update_car_miliage(instance.car)

@receiver(post_save, sender=ServiceRecord)
@receiver(post_delete, sender=ServiceRecord)
def update_miliage_by_service_record(sender, instance, **kwargs):
    update_car_miliage(instance.car)
