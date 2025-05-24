from django.urls import path, include
from .views import (main, add_auto, add_service_record, user_autos, user_service_history,
                    edit_service_record, delete_service_record, edit_auto, delete_auto)

urlpatterns = [
    path('main/', main, name='main'),
    path('add_auto/', add_auto, name='add_auto'),
    path('add_service/', add_service_record, name='add_service'),
    path('services/<int:pk>/edit/', edit_service_record, name='edit_service'),
    path('services/<int:pk>/delete/', delete_service_record, name='delete_service'),
    path('autos/<int:pk>/edit/', edit_auto, name='edit_auto'),
    path('autos/<int:pk>/delete', delete_auto, name='delete_auto'),
    path('autos/', user_autos, name='autos'),
    path('service_history/', user_service_history, name='service_history'),
]