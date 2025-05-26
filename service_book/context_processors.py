from django.core.cache import cache

from service_book.models import Car


def global_settings(request):
    context = {}

    if request.user.is_authenticated:
        user_cars_cache_key = f'user_{request.user.id}_cars_count'
        user_cars_count = cache.get(user_cars_cache_key)
        if user_cars_count is None:
            user_cars_count = Car.objects.filter(owner=request.user).count()
            cache.set(user_cars_cache_key, user_cars_count, 60 * 15)
        context['user_cars_count'] = user_cars_count



    else:
        context['user_cars_count'] = 0

    return context