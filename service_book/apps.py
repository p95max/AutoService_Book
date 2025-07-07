from django.apps import AppConfig
from django.contrib.auth import get_user_model
from decouple import config

class ServiceBookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service_book'

    def ready(self):
        print('ServiceBookConfig.ready() called')
        import service_book.signals

        User = get_user_model()
        admin_username = config('ADMIN_USERNAME')
        admin_email = config('ADMIN_EMAIL')
        admin_password = config('ADMIN_PASSWORD')

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(admin_username, admin_email, admin_password)
            print(f"Superuser '{admin_username}' created.")
        else:
            print(f"Superuser '{admin_username}' already exists.")
