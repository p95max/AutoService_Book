from datetime import datetime
from django import forms
from .models import Car, ServiceRecord, FuelExpense, ContactRequest, Carpart, OtherExpense, User


class AddNewAuto(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'prod_year', 'miliage', 'vin']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
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

    def clean_prod_year(self):
        year = self.cleaned_data['prod_year']
        current_year = datetime.now().year
        if year <= 1920:
            raise forms.ValidationError('Please enter a year after 1920')
        if year > current_year:
            raise forms.ValidationError('You cannot be in the future')
        return year

    def clean_miliage(self):
        miliage = self.cleaned_data['miliage']
        if miliage < 0:
            raise forms.ValidationError('Please enter a positive number')
        if miliage > 1000000:
            raise forms.ValidationError('Miliage is too large, check your input or contact us')
        return miliage

    def clean_vin(self):
        vin = self.cleaned_data.get('vin', '').strip().upper()
        if vin:
            if len(vin) != 17:
                raise forms.ValidationError('VIN number must be 17 characters long')
            if not vin.isalnum():
                raise forms.ValidationError('VIN number must contains only letters and numbers')
            if Car.objects.filter(vin=vin).exists():
                raise forms.ValidationError('This VIN already exists')
        return vin

class AddNewServiceRecord(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ['date', 'car', 'miliage', 'place', 'service_type', 'price', 'description',]
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'miliage': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Date',
            'car': 'Car',
            'place': 'Place',
            'miliage': 'Miliage',
            'service_type': 'Service Type',
            'price': 'Price',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['car'].queryset = Car.objects.filter(owner=user)
        else:
            self.fields['car'].queryset = Car.objects.none()

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Price must be greater than 0')
        return price

    def clean_miliage(self):
        miliage = self.cleaned_data['miliage']
        if miliage < 0:
            raise forms.ValidationError('Please enter a positive number')
        if miliage > 1000000:
            raise forms.ValidationError('Miliage is too large, check your input or contact us')
        return miliage

    def clean_date(self):
        date = self.cleaned_data['date']
        now = datetime.now()
        if date > now:
            raise forms.ValidationError('Date must not be in the future')
        return date

class AddNewFuelExpense(forms.ModelForm):
    class Meta:
        model = FuelExpense
        fields = ['date', 'car', 'miliage', 'fuel_type', 'fuel_amount', 'price', 'gas_station', 'description',]
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'miliage': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'fuel_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gas_station': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Date',
            'car': 'Car',
            'miliage': 'Miliage',
            'fuel_type': 'Fuel Type',
            'fuel_amount': 'Fuel Amount',
            'price': 'Price',
            'gas_station': 'Gas Station',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['car'].queryset = Car.objects.filter(owner=user)
        else:
            self.fields['car'].queryset = Car.objects.none()

    def clean_date(self):
        date = self.cleaned_data['date']
        now = datetime.now()
        if date > now:
            raise forms.ValidationError('Date must not be in the future')
        return date

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Price must be greater than 0')
        return price

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }

class AddNewCarPart(forms.ModelForm):
    class Meta:
        model = Carpart
        fields = ['date_purchase', 'name', 'car', 'carpart_type', 'price', 'place_purchase',
                  'date_installation', 'place_installation', 'description',]
        widgets = {
            'date_purchase': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'carpart_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'place_purchase': forms.TextInput(attrs={'class': 'form-control'}),
            'date_installation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'place_installation': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'date_purchase': 'Date',
            'name': 'Name',
            'car': 'Car',
            'carpart_type': 'Carpart Type',
            'price': 'Price',
            'place_purchase': 'Place',
            'date_installation': 'Installation date',
            'place_installation': 'Installation place',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['car'].queryset = Car.objects.filter(owner=user)
        else:
            self.fields['car'].queryset = Car.objects.none()

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Price must be greater than 0')
        return price

    def clean(self):
        cleaned_data = super().clean()
        date_purchase = cleaned_data.get('date_purchase')
        date_installation = cleaned_data.get('date_installation')
        now = datetime.now()

        if date_purchase and date_purchase > now:
            self.add_error('date_purchase', 'Purchase date must not be in the future')
        if date_installation and date_installation > now:
            self.add_error('date_installation', 'Installation date must not be in the future')

        return cleaned_data

class AddNewOtherExpense(forms.ModelForm):
    PAID_CHOICES = (
    ('true', 'Paid'),
        ('false', 'Not Paid'),
    )
    paid_status = forms.ChoiceField(
        choices=PAID_CHOICES,
        widget=forms.RadioSelect,
        label='Payment status'
    )

    class Meta:
        model = OtherExpense
        fields = ['date', 'name', 'car', 'price', 'expense_type', 'paid_status', 'description']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expense_type': forms.Select(attrs={'class': 'form-control'}),
            'paid_status': forms.RadioSelect(choices=[(True, 'Paid'), (False, 'Not Paid')]),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Date',
            'name': 'Name',
            'car': 'Car',
            'price': 'Price',
            'expense_type': 'Expense Type',
            'paid_status': 'Paid Status',
            'description': 'Description',
        }

    def clean_paid_status(self):
        value = self.cleaned_data['paid_status']
        return value == 'true'

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Price must be greater than 0')
        return price

    def clean_date(self):
        date = self.cleaned_data['date']
        now = datetime.now()
        if date > now:
            raise forms.ValidationError('Date must not be in the future')
        return date

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['car'].queryset = Car.objects.filter(owner=user)
        else:
            self.fields['car'].queryset = Car.objects.none()

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name', '')
        last_name = cleaned_data.get('last_name', '')

        if any(char.isdigit() for char in first_name) or any(char.isdigit() for char in last_name):
            raise forms.ValidationError('Name and surname cannot contain numbers')

        return cleaned_data