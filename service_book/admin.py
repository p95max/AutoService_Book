from django.contrib import admin

from service_book.models import ServiceRecord, Car, ContactRequest, FuelExpense, Carpart, Brand

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'prod_year', 'miliage', 'owner']
    search_fields = ['model', 'vin']
    list_filter = ['prod_year', 'owner']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name']
    list_filter = ['name', 'country']

@admin.register(ServiceRecord)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['date', 'car',  'owner', 'service_type']
    search_fields = ['date', 'car',  'owner', 'service_type']
    list_filter = ['date', 'car',  'owner', 'service_type']

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at', 'is_resolved']
    search_fields = ['email', 'is_resolved']
    list_filter = ['email', 'created_at', 'is_resolved']

@admin.register(FuelExpense)
class FuelExpenseAdmin(admin.ModelAdmin):
    list_display = ['date', 'car', 'fuel_type', 'owner']
    search_fields = ['date', 'car', 'fuel_type', 'owner']
    list_filter = ['date', 'car', 'fuel_type', 'owner']

@admin.register(Carpart)
class CarPartAdmin(admin.ModelAdmin):
    list_display = ['date_purchase', 'carpart_type', 'owner']
    search_fields = ['date_purchase', 'carpart_type', 'owner']
    list_filter = ['date_purchase', 'carpart_type', 'owner']


