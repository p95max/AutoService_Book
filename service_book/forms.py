from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Car, ServiceRecord, FuelExpense, ContactRequest, Carpart, OtherExpense, User

class AddNewAuto(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'prod_year', 'miliage', 'vin']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter model:')}),
            'prod_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Enter year:')}),
            'miliage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Enter mileage (km):')}),
            'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter VIN number:')}),
        }
        labels = {
            'brand': _('Brand'),
            'model': _('Model'),
            'prod_year': _('Prod Year'),
            'miliage': _('Mileage'),
            'vin': _('VIN'),
        }

    def clean_prod_year(self):
        year = self.cleaned_data.get('prod_year')
        if year is None:
            return year
        current_year = timezone.now().year
        if year <= 1920:
            raise forms.ValidationError(_('Please enter a year after 1920'))
        if year > current_year:
            raise forms.ValidationError(_('You cannot be in the future'))
        return year

    def clean_miliage(self):
        miliage = self.cleaned_data.get('miliage')
        if miliage is None:
            return miliage
        if miliage < 0:
            raise forms.ValidationError(_('Please enter a positive number'))
        if miliage > 1000000:
            raise forms.ValidationError(_('Mileage is too large, check your input or contact us'))
        return miliage

    def clean_vin(self):
        vin = (self.cleaned_data.get('vin') or '').strip().upper()
        if vin:
            if len(vin) != 17:
                raise forms.ValidationError(_('VIN number must be exactly 17 characters long'))
            if not vin.isalnum():
                raise forms.ValidationError(_('VIN number must contain only letters and numbers'))
            qs = Car.objects.filter(vin=vin)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(_('This VIN already exists'))
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
            'date': _('Date'),
            'car': _('Car'),
            'place': _('Place'),
            'miliage': _('Mileage'),
            'service_type': _('Service Type'),
            'price': _('Price'),
            'description': _('Description'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['car'].queryset = Car.objects.filter(owner=user)
        else:
            self.fields['car'].queryset = Car.objects.none()

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        if price <= 0:
            raise forms.ValidationError(_('Price must be greater than 0'))
        return price

    def clean_miliage(self):
        miliage = self.cleaned_data.get('miliage')
        if miliage is None:
            return miliage
        if miliage < 0:
            raise forms.ValidationError(_('Please enter a positive number'))
        if miliage > 1000000:
            raise forms.ValidationError(_('Mileage is too large, check your input or contact us'))
        return miliage

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date is None:
            return date
        now = timezone.now()
        if date > now:
            raise forms.ValidationError(_('Date must not be in the future'))
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
            'date': _('Date'),
            'car': _('Car'),
            'miliage': _('Mileage'),
            'fuel_type': _('Fuel Type'),
            'fuel_amount': _('Fuel Amount'),
            'price': _('Price'),
            'gas_station': _('Gas Station'),
            'description': _('Description'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['car'].queryset = Car.objects.filter(owner=user)
        else:
            self.fields['car'].queryset = Car.objects.none()

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date is None:
            return date
        now = timezone.now()
        if date > now:
            raise forms.ValidationError(_('Date must not be in the future'))
        return date

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        if price <= 0:
            raise forms.ValidationError(_('Price must be greater than 0'))
        return price

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your Name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your Email')}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Your Message'), 'rows': 5}),
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
            'date_purchase': _('Date'),
            'name': _('Name'),
            'car': _('Car'),
            'carpart_type': _('Carpart Type'),
            'price': _('Price'),
            'place_purchase': _('Place'),
            'date_installation': _('Installation date'),
            'place_installation': _('Installation place'),
            'description': _('Description'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['car'].queryset = Car.objects.filter(owner=user)
        else:
            self.fields['car'].queryset = Car.objects.none()

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        if price <= 0:
            raise forms.ValidationError(_('Price must be greater than 0'))
        return price

    def clean(self):
        cleaned_data = super().clean()
        date_purchase = cleaned_data.get('date_purchase')
        date_installation = cleaned_data.get('date_installation')
        now = timezone.now()

        if date_purchase and date_purchase > now:
            self.add_error('date_purchase', _('Purchase date must not be in the future'))
        if date_installation and date_installation > now:
            self.add_error('date_installation', _('Installation date must not be in the future'))

        return cleaned_data

class AddNewOtherExpense(forms.ModelForm):
    PAID_CHOICES = (
        ('true', _('Paid')),
        ('false', _('Not Paid')),
    )
    paid_status = forms.ChoiceField(
        choices=PAID_CHOICES,
        widget=forms.RadioSelect,
        label=_('Payment status')
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
            'paid_status': forms.RadioSelect(choices=[(True, _('Paid')), (False, _('Not Paid'))]),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': _('Date'),
            'name': _('Name'),
            'car': _('Car'),
            'price': _('Price'),
            'expense_type': _('Expense Type'),
            'paid_status': _('Paid Status'),
            'description': _('Description'),
        }

    def clean_paid_status(self):
        value = self.cleaned_data.get('paid_status')
        return value == 'true'

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        if price <= 0:
            raise forms.ValidationError(_('Price must be greater than 0'))
        return price

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date is None:
            return date
        now = timezone.now()
        if date > now:
            raise forms.ValidationError(_('Date must not be in the future'))
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
            raise forms.ValidationError(_('Name and surname cannot contain numbers'))

        return cleaned_data