from django import forms
from .models import Car, ServiceRecord, FuelExpense

class AddNewAuto(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'prod_year', 'miliage', 'vin']
        widgets = {
            'brand': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter model:'}),
            'prod_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter year:'}),
            'miliage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter miliage(km):'}),
            'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter vin number:'}),
        }
        labels = {
            'brand': 'Brand',
            'model': 'Model',
            'prod_year': 'Prod Year',
            'miliage': 'Miliage',
            'vin': 'VIN',
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(owner=user)

class AddNewServiceRecord(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ['date', 'car', 'place', 'service_type', 'price', 'description',]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Date',
            'car': 'Car',
            'place': 'Place',
            'service_type': 'Service Type',
            'price': 'Price',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(owner=user)

class AddNewFuelExpense(forms.ModelForm):
    class Meta:
        model = FuelExpense
        fields = ['date', 'car', 'fuel_type', 'fuel_amount', 'price', 'gas_station', 'description',]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'fuel_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'gas_station': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Date',
            'car': 'Car',
            'fuel_type': 'Fuel Type',
            'fuel_amount': 'Fuel Amount',
            'price': 'Price',
            'gas_station': 'Gas Station',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(owner=user)