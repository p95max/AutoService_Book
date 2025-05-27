from django.contrib import admin

from service_book.models import ServiceRecord, Car, ContactRequest, FuelExpense, Carpart, Brand

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'prod_year', 'miliage', 'owner']
    search_fields = ['model', 'vin']
    list_filter = ['prod_year', 'owner']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
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

@admin.register(Carpart)
class CarPartAdmin(admin.ModelAdmin):
    pass


