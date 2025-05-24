from django.http import HttpResponseRedirect
from django.shortcuts import render

from service_book.forms import AddNewAuto


def main(request):
    user = request.user


    context = {
        'user': user,
    }

    return render(request, 'main.html', context=context)

def add_auto(request):
    if request.method == 'POST':
        form = AddNewAuto(request.POST)

        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            form.save_m2m()
            return HttpResponseRedirect('/main')
    else:
        form = AddNewAuto()

    context = {
        'form': form,
    }

    return render(request, 'add_auto.html', context=context)

