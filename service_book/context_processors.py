from django.core.cache import cache
from django.db.models import Sum

from service_book.models import Car, ServiceRecord, Carpart


def global_settings(request):
    context = {}

# User total cars in garage
    if request.user.is_authenticated:
        user_cars_cache_key = f'user_{request.user.id}_cars_count'
        user_cars_count = cache.get(user_cars_cache_key)
        if user_cars_count is None:
            user_cars_count = Car.objects.filter(owner=request.user).count()
            cache.set(user_cars_cache_key, user_cars_count, 60 * 15)
        context['user_cars_count'] = user_cars_count

# User total service costs
    if request.user.is_authenticated:
        user_total_service_costs = f'user_{request.user.id}_total_service_costs'
        user_total_service_costs = cache.get(user_total_service_costs)
        if user_total_service_costs is None:
            user_total_service_costs = ServiceRecord.objects.filter(car__owner=request.user).aggregate(Sum('price'))['price__sum'] or 0
            cache.set(user_total_service_costs, user_total_service_costs, 60 * 15)
        context['user_total_service_costs'] = round(user_total_service_costs, 1)

# User total parts costs
    if request.user.is_authenticated:
        user_total_parts_costs = f'user_{request.user.id}_total_parts_costs'
        user_total_parts_costs = cache.get(user_total_parts_costs)
        if user_total_parts_costs is None:
            user_total_parts_costs = Carpart.objects.filter(car__owner=request.user).aggregate(Sum('price'))['price__sum'] or 0
            cache.set(user_total_parts_costs, user_total_parts_costs, 60 * 15)
        context['user_total_parts_costs'] = round(user_total_parts_costs, 1)

    else:
        context['user_cars_count'] = 0
        context['user_total_service_costs'] = 0
        context['user_total_parts_costs'] = 0

    return context

