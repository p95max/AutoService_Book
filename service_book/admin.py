from django.contrib import admin

from service_book.models import ServiceRecord, Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceRecord)
class ServiceAdmin(admin.ModelAdmin):
    pass

