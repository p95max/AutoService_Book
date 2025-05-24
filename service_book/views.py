from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from service_book.forms import AddNewAuto, AddNewServiceRecord
from service_book.models import ServiceRecord, Car


def main(request):
    user = request.user


    context = {
        'user': user,
    }

    return render(request, 'main.html', context=context)

@login_required
def user_service_history(request):
    service_history = ServiceRecord.objects.filter(owner=request.user)

    return render(request, 'service_history.html', context={'service_history': service_history})

@login_required
def user_autos(request):
    cars = Car.objects.filter(owner=request.user)

    return render(request, 'my_autos.html', context={'cars': cars})

@login_required
def add_auto(request):
    if request.method == 'POST':
        form = AddNewAuto(request.POST)

        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            form.save_m2m()
            return HttpResponseRedirect('/autos/')
    else:
        form = AddNewAuto()


    context = {
        'form': form,
    }

    return render(request, 'add_auto.html', context=context)

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

    return render(request, 'edit_auto.html', {'form': form})

@login_required
def delete_auto(request, pk):
    auto = get_object_or_404(Car, pk=pk, owner=request.user)

    if request.method == 'POST':
        auto.delete()
        return redirect('autos')

    return redirect('autos')

@login_required
def add_service_record(request):
    if request.method == 'POST':
        form = AddNewServiceRecord(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            return HttpResponseRedirect('/service_history/')
    else:
        form = AddNewServiceRecord()


    context = {
        'form': form,
    }

    return render(request, 'add_service.html', context=context)

@login_required
def edit_service_record(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = AddNewServiceRecord(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('service_history')
    else:
        form = AddNewServiceRecord(instance=record)

    return render(request, 'edit_service.html', {'form': form})

@login_required
def delete_service_record(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk, owner=request.user)

    if request.method == 'POST':
        record.delete()
        return redirect('service_history')

    return redirect('service_history')
