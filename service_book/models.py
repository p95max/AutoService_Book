from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class Car(models.Model):
    brand = models.ManyToManyField(Brand)
    model = models.CharField(max_length=100)
    prod_year = models.IntegerField()
    miliage = models.IntegerField()
    fuel_left = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    vin = models.CharField(max_length=20, unique=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Owner'
    )

    def __str__(self):
        brands = ", ".join([brand.name for brand in self.brand.all()])
        return f"{brands} - {self.model}"

class ServiceRecord(models.Model):
    SERVICE_ACTIONS = [
        ('interval_service', 'Interval Service'),
        ('diagnostics', 'Diagnostic'),
        ('tire_service', 'Tire Service'),
        ('repair_service', 'Repair'),
        ('other_service', 'Other'),
    ]

    date = models.DateTimeField(null=False, blank=False)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='User'
    )
    place = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_ACTIONS, default='other_service')
    miliage = models.IntegerField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.car} - {self.get_service_type_display()} - {self.date} - {self.price}$"

class FuelExpense(models.Model):
    FUEL_TYPES = [
        ('diesel', 'Regular diesel'),
        ('premium_diesel', 'Premium diesel'),
        ('petrol_e5', 'Petrol E5'),
        ('petrol_e10', 'Petrol E10'),
        ('lpg', 'LPG'),
        ('electric_charge', 'Electric charge'),
        ('other', 'Other'),
    ]
    date = models.DateTimeField(null=False, blank=False)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    miliage = models.IntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=50, choices=FUEL_TYPES, default='other')
    fuel_amount = models.DecimalField(max_digits=10, decimal_places=2)
    distance = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='User'
    )
    gas_station = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.car} - {self.get_fuel_type_display()} - {self.fuel_amount} - {self.date} - {self.price}$"

class ContactRequest(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"

class Carpart(models.Model):
    CARPART_TYPES = [
        ('body', 'Car body part'),
        ('engine', 'Car engine part'),
        ('transmission', 'Car transmission part'),
        ('tyre', 'Car tyre'),
        ('tuning', 'Car tuning part'),
        ('service', 'Car service part'),
        ('break', 'Car break part'),
        ('electric', 'Car electric part'),
        ('care', 'Car care'),
        ('other', 'Other'),
    ]

    date_purchase = models.DateTimeField(null=False, blank=False)
    name = models.CharField(max_length=200)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    carpart_type = models.CharField(max_length=50, choices=CARPART_TYPES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    place_purchase = models.CharField(max_length=100)
    date_installation = models.DateField(null=True, blank=True)
    place_installation = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.car} - {self.name} - {self.get_carpart_type_display()}"


