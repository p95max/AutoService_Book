from django import forms
from .models import Car

class AddNewAuto(forms.ModelForm):

    class Meta:
        model = Car
        fields = ['brand', 'model', 'prod_year', 'miliage', 'vin']
        widgets = {
            'brand': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter model:'}),
            'prod_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter year:'}),
            'miliage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter miliage(km):'}),
            'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter vin number:'}),
        }
        labels = {
            'brand': 'Brand',
            'model': 'Model',
            'prod_year': 'Prod Year',
            'miliage': 'Miliage',
            'vin': 'VIN',
        }