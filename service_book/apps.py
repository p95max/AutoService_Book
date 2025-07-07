from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os


class ServiceBookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service_book'

    def ready(self):
        print('ServiceBookConfig.ready() called')
        import service_book.signals

        # create superuser for render deploy
        User = get_user_model()
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'password123')
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(admin_username, admin_email, admin_password)
            print(f"Superuser '{admin_username}' created")
        else:
            print(f"Superuser '{admin_username}' already exists")

