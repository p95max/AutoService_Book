from django.urls import path, include
from .views import main, add_auto

urlpatterns = [
    path('main/', main, name='main'),
    path('add_auto/', add_auto, name='add_auto'),
]