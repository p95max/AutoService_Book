from django.apps import AppConfig
from django.contrib.auth import get_user_model
from decouple import config

class ServiceBookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service_book'

    def ready(self):
        print('ServiceBookConfig.ready() called')
        import service_book.signals


