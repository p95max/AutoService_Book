import os
from datetime import timezone

from allauth.account.internal.userkit import user_email
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from itertools import chain
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from service_book.forms import (AddNewAuto, AddNewServiceRecord, AddNewFuelExpense,
                                ContactRequestForm, AddNewCarPart, AddNewOtherExpense, UserUpdateForm)
from service_book.models import ServiceRecord, Car, FuelExpense, Carpart, OtherExpense, User

def main(request):
# Intro text
    intro_text = ""
    file_path = os.path.join(settings.BASE_DIR, 'static', 'text', 'home_intro.txt')
    try:
        with open(file_path) as file:
            intro_text = file.read()
    except FileNotFoundError:
        intro_text = "Error: File not found."

    context = {
        'intro_text': intro_text,
    }
    return render(request, 'main.html', context=context)

def contact_us(request):
    success = False

    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactRequestForm()
        else:
            success = False
    else:
        form = ContactRequestForm()

    context = {
        'form': form,
        'success': success,
    }
    return render(request, 'contact_us.html', context)

@login_required
def profile(request):
    user = get_object_or_404(User, username=request.user.username)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'username': user.username,
        'user_lastlogin': user.last_login,
        'date_joined': user.date_joined,
        'user_firstname': user.first_name,
        'user_lastname': user.last_name,
        'user_email': user.email,
        'form': form,
    }
    return render(request, 'profile.html', context)

# Autos list
@login_required
def user_autos(request):
    cars = Car.objects.filter(owner=request.user)

#All user expenses
    total_fuel = FuelExpense.objects.filter(owner=request.user).aggregate(Sum('price'))['price__sum'] or 0
    total_service = ServiceRecord.objects.filter(owner=request.user).aggregate(Sum('price'))['price__sum'] or 0
    total_carpart = Carpart.objects.filter(owner=request.user).aggregate(Sum('price'))['price__sum'] or 0
    total_other = OtherExpense.objects.filter(owner=request.user).aggregate(Sum('price'))['price__sum'] or 0
    total_sum = total_fuel + total_service + total_carpart + total_other
    total_sum = round(total_sum, 1)

    context = {
        'cars': cars,
        'total_sum': total_sum,
    }

    return render(request, 'autos/my_autos.html', context=context)

@login_required
def add_auto(request):
    if request.method == 'POST':
        form = AddNewAuto(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            form.save_m2m()
            return redirect('autos')
    else:
        form = AddNewAuto()
    context = {'form': form}
    return render(request, 'autos/add_auto.html', context=context)

@login_required
def edit_auto(request, pk):
    auto = get_object_or_404(Car, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = AddNewAuto(request.POST, instance=auto)
        if form.is_valid():
            form.save()
            return redirect('autos')
    else:
        form = AddNewAuto(instance=auto)
    return render(request, 'autos/edit_auto.html', {'form': form})

@login_required
def delete_auto(request, pk):
    auto = get_object_or_404(Car, pk=pk, owner=request.user)
    if request.method == 'POST':
        auto.delete()
        return redirect('autos')
    return redirect('autos')

# Service records
@login_required
def user_service_history(request):
# Pagination and table sorting
    sort_by = request.GET.get('sort', 'date')
    sort_options = {
        'date': '-date',
        'price': '-price',
        'car': 'car__model',
        'service_type': 'service_type',
    }
    sort_field = sort_options.get(sort_by, '-date')
    service_history = ServiceRecord.objects.filter(owner=request.user).order_by(sort_field)
    paginator = Paginator(service_history, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
# Costs per car
    cars = Car.objects.filter(owner=request.user)
    total_costs_per_car = (
        ServiceRecord.objects
        .filter(owner=request.user)
        .values('car__id', 'car__brand__name', 'car__model')
        .annotate(total_cost=Sum('price'))
    )
    costs_dict = {item['car__id']: item['total_cost'] for item in total_costs_per_car}

    user_total_service_costs = ServiceRecord.objects.filter(owner=request.user).aggregate(Sum('price'))['price__sum'] or 0

    context = {
        'cars': cars,
        'page_obj': page_obj,
        'sort': sort_by,
        'costs_dict': costs_dict,
        'total_costs_per_car': total_costs_per_car,
        'user_total_service_costs': user_total_service_costs,
    }
    return render(request, 'service_records/service_history.html', context)

@login_required
def add_service_record(request):
    if request.method == 'POST':
        form = AddNewServiceRecord(request.POST, user=request.user)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            return redirect('service_history')
    else:
        form = AddNewServiceRecord(user=request.user)
    context = {'form': form}
    return render(request, 'service_records/add_service.html', context=context)

@login_required
def edit_service_record(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = AddNewServiceRecord(request.POST, user=request.user, instance=record)
        if form.is_valid():
            form.save()
            return redirect('service_history')
    else:
        form = AddNewServiceRecord(user=request.user, instance=record)
    return render(request, 'service_records/edit_service.html', {'form': form})

@login_required
def delete_service_record(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk, owner=request.user)
    if request.method == 'POST':
        record.delete()
        return redirect('service_history')
    return redirect('service_history')

# Fuel expense
@login_required
def fuel_expense(request):
    fuel = FuelExpense.objects.filter(owner=request.user)
    cars = Car.objects.filter(owner=request.user)
# total string
    total_refuels_all  = fuel.aggregate(Count('id'))['id__count'] or 0
    total_fuel_all = fuel.aggregate(Sum('fuel_amount'))['fuel_amount__sum'] or 0
    total_costs_all = fuel.aggregate(Sum('price'))['price__sum'] or 0
    total_costs_all = round(total_costs_all, 1)

# Pagination and table sorting
    sort_by = request.GET.get('sort', 'date')
    sort_options = {
        'date': '-date',
        'price': '-price',
        'car': 'car__model',
        'fuel_type': 'fuel_type',
    }
    sort_field = sort_options.get(sort_by, '-date')
    service_history = FuelExpense.objects.filter(owner=request.user).order_by(sort_field)
    paginator = Paginator(service_history, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

# Avag cons. and fuel left calculation
    for car in cars:
        fuel_records = FuelExpense.objects.filter(owner=request.user, car=car)
        service_records = ServiceRecord.objects.filter(car=car)
        all_events = sorted(
            chain(fuel_records, service_records),
            key=lambda x: x.date
        )
        total_fuel = sum(float(f.fuel_amount) for f in fuel_records if getattr(f, 'distance', None))
        total_distance = sum(getattr(f, 'distance', 0) for f in fuel_records if getattr(f, 'distance', None))
        if total_distance > 0:
            avg_cons = (total_fuel / total_distance) * 100
            car.avg_cons = avg_cons
        else:
            avg_cons = None
            car.avg_cons = None
        fuel_left = 0
        prev_miliage = None
        for event in all_events:
            if hasattr(event, 'fuel_amount'):
                fuel_left += float(event.fuel_amount)
            if prev_miliage is not None and avg_cons and event.miliage is not None:

                distance = event.miliage - prev_miliage
                if distance > 0:
                    fuel_left -= (distance / 100) * avg_cons
                    if fuel_left < 0:
                        fuel_left = 0
            prev_miliage = event.miliage
        car.fuel_left = round(fuel_left, 2)
# Fuel costs per car
    total_costs_per_car = (FuelExpense.objects.filter(owner=request.user)
                     .values('car__id', 'car__brand', 'car__model')
                     .annotate(total_cost=Sum('price'))
                     )
    costs_dict = {item['car__id']: item['total_cost']
                  for item in total_costs_per_car}

    context = {
        'page_obj': page_obj,
        'sort': sort_by,
        'fuel': fuel,
        'cars': cars,
        'total_refuels_all': total_refuels_all,
        'total_fuel_all': total_fuel_all,
        'total_costs_all': total_costs_all,
        'total_costs_per_car': total_costs_per_car,
        'costs_dict': costs_dict,
    }
    return render(request, 'fuel_expense/fuel_expense.html', context=context)

@login_required
def add_fuel_expense(request):
    if request.method == 'POST':
        form = AddNewFuelExpense(request.POST, user=request.user)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            return redirect('fuel_expense')
    else:
        form = AddNewFuelExpense(user=request.user)
    context = {'form': form}
    return render(request, 'fuel_expense/add_fuel_expense.html', context=context)

@login_required
def edit_fuel_expense(request, pk):
    record = get_object_or_404(FuelExpense, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = AddNewFuelExpense(request.POST, user=request.user, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            return redirect('fuel_expense')
    else:
        form = AddNewFuelExpense(user=request.user, instance=record)
    return render(request, 'fuel_expense/edit_fuel_expense.html', {'form': form})

@login_required
def delete_fuel_expense(request, pk):
    record = get_object_or_404(FuelExpense, pk=pk, owner=request.user)
    if request.method == 'POST':
        record.delete()
        return redirect('fuel_expense')
    return redirect('fuel_expense')

# Car parts
@login_required
def car_parts(request):
    cars = Car.objects.filter(owner=request.user)
    parts = Carpart.objects.filter(owner=request.user)
    owner = request.user
    total_costs_per_car = (
        Carpart.objects
        .filter(owner=request.user)
        .values('car__id', 'car__brand', 'car__model')
        .annotate(total_cost=Sum('price'))
    )
    costs_dict = {item['car__id']: item['total_cost'] for item in total_costs_per_car}

    # Pagination and table sorting
    sort_by = request.GET.get('sort', 'date_purchase')
    sort_options = {
        'date_purchase': '-date_purchase',
        'price': '-price',
        'car': 'car__model',
        'carpart_type': 'carpart_type',
    }
    sort_field = sort_options.get(sort_by, '-date_purchase')
    parts = Carpart.objects.filter(owner=request.user).order_by(sort_field)
    paginator = Paginator(parts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sort': sort_by,
        'cars': cars,
        'parts': parts,
        'owner': owner,
        'total_costs_per_car': total_costs_per_car,
        'costs_dict': costs_dict,
    }

    return render(request, 'carparts/my_carparts.html', context=context)

@login_required
def add_carpart(request):
    if request.method == 'POST':
        form = AddNewCarPart(request.POST, user=request.user)
        if form.is_valid():
            part = form.save(commit=False)
            part.owner = request.user
            part.save()
            return redirect('my_carparts')
    else:
        form = AddNewCarPart(user=request.user)
    context = {'form': form}

    return render(request, 'carparts/add_carpart.html', context=context)

@login_required
def edit_carpart(request, pk):
    part = get_object_or_404(Carpart, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = AddNewCarPart(request.POST, user=request.user, instance=part)
        if form.is_valid():
            part = form.save(commit=False)
            part.owner = request.user
            part.save()
            return redirect('my_carparts')
    else:
        form = AddNewCarPart(user=request.user, instance=part)

    return render(request, 'carparts/edit_carpart.html', {'form': form})

@login_required
def delete_car_part(request, pk):
    part = get_object_or_404(Carpart, pk=pk, owner=request.user)
    if request.method == 'POST':
        part.delete()
        return redirect('my_carparts')
    return redirect('my_carparts')

# Other expenses
@login_required
def other_expense(request):
    cars = Car.objects.filter(owner=request.user)
    other_expenses = OtherExpense.objects.filter(owner=request.user)
    owner = request.user
    total_costs_per_car = (
        OtherExpense.objects
        .filter(owner=request.user)
        .values('car__id', 'car__brand', 'car__model')
        .annotate(total_cost=Sum('price'))
    )
    costs_dict = {item['car__id']: item['total_cost'] for item in total_costs_per_car}

# Pagination and table sorting
    sort_by = request.GET.get('sort', 'date')
    sort_options = {
        'date': '-date',
        'price': '-price',
        'car': 'car__model',
        'paid_status': 'paid_status',
        'expense_type': 'expense_type',
    }
    sort_field = sort_options.get(sort_by, '-date')
    other_expenses = OtherExpense.objects.filter(owner=request.user).order_by(sort_field)
    paginator = Paginator(other_expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cars': cars,
        'other_expenses': other_expenses,
        'owner': owner,
        'total_costs_per_car': total_costs_per_car,
        'costs_dict': costs_dict,
        'sort_by': sort_by,
        'page_obj': page_obj,
    }

    return render(request, 'other_expenses/other_expenses.html', context=context)

@login_required
def add_other_expense(request):
    if request.method == 'POST':
        form = AddNewOtherExpense(request.POST, user=request.user)
        if form.is_valid():
            other_expense = form.save(commit=False)
            other_expense.owner = request.user
            other_expense.save()
            return redirect('other_expense')
    else:
        form = AddNewOtherExpense(user=request.user)
    context = {'form': form}

    return render(request, 'other_expenses/add_other_expense.html', context=context)

@login_required
def edit_other_expense(request, pk):
    other_expense = get_object_or_404(OtherExpense, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = AddNewOtherExpense(request.POST, user=request.user, instance=other_expense)
        if form.is_valid():
            other_expense = form.save(commit=False)
            other_expense.owner = request.user
            other_expense.save()
            return redirect('other_expense')
    else:
        form = AddNewOtherExpense(user=request.user, instance=other_expense)

    return render(request, 'other_expenses/edit_other_expense.html', {'form': form})

@login_required
def delete_other_expense(request, pk):
    other_expense = get_object_or_404(OtherExpense, pk=pk, owner=request.user)
    if request.method == 'POST':
        other_expense.delete()
        return redirect('other_expense')
    return redirect('other_expense')