from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import FuelExpense, ServiceRecord, Car
from django.db.models import Max

def update_car_miliage(car):
    if car is None:
        return
    cache_key = f'car_{car.id}_max_miliage'
    max_miliage = cache.get(cache_key)
    if max_miliage is None:
        fuel_max = FuelExpense.objects.filter(car=car).aggregate(max_miliage=Max('miliage'))['max_miliage'] or 0
        service_max = ServiceRecord.objects.filter(car=car).aggregate(max_miliage=Max('miliage'))['max_miliage'] or 0
        max_miliage = max(fuel_max, service_max)
        cache.set(cache_key, max_miliage, 60 * 15)
    if car.miliage != max_miliage:
        car.miliage = max_miliage
        car.save(update_fields=['miliage'])

def get_cached_value(cache_key, query, ttl=60*15):
    value = cache.get(cache_key)
    if value is None:
        value = query() or 0
        cache.set(cache_key, value, ttl)
    return round(value, 1)

@receiver(post_save, sender=FuelExpense)
@receiver(post_delete, sender=FuelExpense)
def update_miliage_by_fuel_expense(sender, instance, **kwargs):
    update_car_miliage(instance.car)

@receiver(post_save, sender=ServiceRecord)
@receiver(post_delete, sender=ServiceRecord)
def update_miliage_by_service_record(sender, instance, **kwargs):
    update_car_miliage(instance.car)

@receiver(post_save, sender=FuelExpense)
def update_fuel_left_add(sender, instance, created, **kwargs):
    if created and instance.car:
        instance.car.fuel_left += instance.fuel_amount
        instance.car.save(update_fields=['fuel_left'])

@receiver(post_delete, sender=FuelExpense)
def update_fuel_left_delete(sender, instance, **kwargs):
    if instance.car:
        instance.car.fuel_left -= instance.fuel_amount
        instance.car.save(update_fields=['fuel_left'])

@receiver(pre_save, sender=FuelExpense)
def set_distance_on_save(sender, instance, **kwargs):
    if (instance.distance is None or instance.distance == 0) and instance.miliage and instance.car and instance.owner:
        prev = FuelExpense.objects.filter(
            car=instance.car,
            owner=instance.owner,
            date__lt=instance.date
        ).order_by('-date').first()
        if prev and prev.miliage:
            instance.distance = instance.miliage - prev.miliage
        else:
            instance.distance = None


@receiver([post_save, post_delete], sender=Car)
def clear_user_cars_count_cache(sender, instance, **kwargs):
    if instance.owner:
        cache_key = f'user_{instance.owner.id}_cars_count'
        cache.delete(cache_key)

@receiver([post_save, post_delete], sender=ServiceRecord)
def clear_service_costs_cache(sender, instance, **kwargs):
    if instance.owner:
        cache.delete(f'user_{instance.owner.id}_total_service_costs')

