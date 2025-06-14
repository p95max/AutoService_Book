import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from service_book.models import OtherExpense, ServiceRecord, FuelExpense, Carpart, User

@login_required
def export_csv_other(request):
    username = get_object_or_404(User, username=request.user.username)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{username}_other_expense.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", 'Name', 'Car', 'Price', 'Expense type', 'Paid status', 'Description'])

    for item in OtherExpense.objects.filter(owner=request.user):
        writer.writerow([
            item.date.strftime('%d.%m.%Y %H:%M') if item.date else '',
            item.name,
            item.car,
            item.price,
            item.get_expense_type_display(),
            'Paid' if item.paid_status else 'Not Paid',
            item.description,
        ])
    return response

@login_required
def export_csv_service(request):
    username = get_object_or_404(User, username=request.user.username)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{username}_service_expense.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", 'Car', 'Mileage', 'Place', 'Service type', 'Price', 'Description'])

    for item in ServiceRecord.objects.filter(owner=request.user):
        writer.writerow([
            item.date.strftime('%d.%m.%Y %H:%M') if item.date else '',
            item.car,
            item.miliage,
            item.place,
            item.get_service_type_display(),
            item.price,
            item.description,

        ])
    return response

@login_required
def export_csv_fuel(request):
    username = get_object_or_404(User, username=request.user.username)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{username}_fuel_expense.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Car', 'Mileage', 'Fuel type', 'Fuel amount', 'Price', 'Gas station', 'Description'])

    for item in FuelExpense.objects.filter(owner=request.user):
        writer.writerow([
            item.date.strftime('%d.%m.%Y %H:%M') if item.date else '',
            item.car,
            item.miliage,
            item.get_fuel_type_display(),
            item.fuel_amount,
            item.price,
            item.gas_station,
            item.description,

        ])
    return response

@login_required
def export_csv_carpart(request):
    username = get_object_or_404(User, username=request.user.username)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{username}_carpart_expense.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date purchase', 'Item name', 'Car', 'Carpart type', 'Price', 'Place purchase',
                     'Date installation', 'Place installation', 'Description'])

    for item in Carpart.objects.filter(owner=request.user):
        writer.writerow([
            item.date_purchase if item.date_purchase else '',
            item.name,
            item.car,
            item.get_carpart_type_display(),
            item.price,
            item.place_purchase,
            item.date_installation if item.date_installation else '',
            item.place_installation,
            item.description,

        ])
    return response

