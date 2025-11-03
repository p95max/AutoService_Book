import os
from django.contrib import admin
from django.urls import path, include

ADMIN_URL = os.getenv('ADMIN_URL', 'admin')

urlpatterns = [
    path(f'{ADMIN_URL}/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('service_book.urls')),

]




