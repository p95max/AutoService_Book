import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from itertools import chain
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from service_book.forms import (AddNewAuto, AddNewServiceRecord, AddNewFuelExpense,
                                ContactRequestForm, AddNewCarPart)
from service_book.models import ServiceRecord, Car, FuelExpense, Carpart

def main(request):
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

# Autos list
@login_required
def user_autos(request):
    cars = Car.objects.filter(owner=request.user)
    return render(request, 'autos/my_autos.html', context={'cars': cars})

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
    service_history = ServiceRecord.objects.filter(owner=request.user)
    return render(request, 'service_records/service_history.html', context={'service_history': service_history})

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
                # Это заправка
                fuel_left += float(event.fuel_amount)
            if prev_miliage is not None and avg_cons and event.miliage is not None:

                distance = event.miliage - prev_miliage
                if distance > 0:
                    fuel_left -= (distance / 100) * avg_cons
                    if fuel_left < 0:
                        fuel_left = 0
            prev_miliage = event.miliage
        car.fuel_left = round(fuel_left, 2)

    context = {
        'fuel': fuel,
        'cars': cars,
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
    parts = Carpart.objects.filter(owner=request.user)
    owner = request.user

    return render(request, 'carparts/my_carparts.html', context={'parts': parts, 'owner': owner})

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