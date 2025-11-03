from django.apps import AppConfig

class ServiceBookConfig(AppConfig):
    name = "service_book"

    def ready(self):
        from . import signals
