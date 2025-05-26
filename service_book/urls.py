from django.urls import path, include
from .views import (main, add_auto, add_service_record, user_autos, user_service_history,
                    edit_service_record, delete_service_record, edit_auto, delete_auto,
                    fuel_expense, add_fuel_expense, edit_fuel_expense, delete_fuel_expense,
                    contact_us, add_carpart, car_parts, delete_car_part, edit_carpart)

urlpatterns = [
    path('main/', main, name='main'),
    path('contact_us/', contact_us, name='contact_us'),
# Autos list
    path('autos/', user_autos, name='autos'),
    path('add_auto/', add_auto, name='add_auto'),
    path('autos/<int:pk>/edit/', edit_auto, name='edit_auto'),
    path('autos/<int:pk>/delete', delete_auto, name='delete_auto'),
# Service records
    path('service_history/', user_service_history, name='service_history'),
    path('add_service/', add_service_record, name='add_service'),
    path('services/<int:pk>/edit/', edit_service_record, name='edit_service'),
    path('services/<int:pk>/delete/', delete_service_record, name='delete_service'),
# Fuel expense
    path('fuel_expense/', fuel_expense, name='fuel_expense'),
    path('add_fuel_expense/', add_fuel_expense, name='add_fuel_expense'),
    path('fuel_expense/<int:pk>/edit/', edit_fuel_expense, name='edit_fuel_expense'),
    path('fuel_expense/<int:pk>/delete', delete_fuel_expense, name='delete_fuel_expense'),
# Car parts
    path('my_carparts', car_parts, name='my_carparts'),
    path('add_carpart/', add_carpart, name='add_carpart'),
    path('carparts/<int:pk>/edit/', edit_carpart, name='edit_carpart'),
    path('carparts/<int:pk>/delete/', delete_car_part, name='delete_carpart'),
]