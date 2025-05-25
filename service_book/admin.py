from django.contrib import admin

from service_book.models import ServiceRecord, Car, ContactRequest, FuelExpense

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceRecord)
class ServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(FuelExpense)
class FuelExpenseAdmin(admin.ModelAdmin):
    pass

