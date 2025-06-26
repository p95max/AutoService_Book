import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from service_book.models import OtherExpense, ServiceRecord, FuelExpense, Carpart

@login_required
def export_csv_other(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_other_expense.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Name", "Car", "Price", "Expense type", "Paid status", "Description"])

    for item in OtherExpense.objects.filter(owner=request.user):
        writer.writerow([
            item.date.strftime('%d.%m.%Y %H:%M') if item.date else '',
            item.name,
            str(item.car) if item.car else '',
            f"{item.price:.2f}",
            item.get_expense_type_display(),
            'Paid' if item.paid_status else 'Not Paid',
            item.description,
        ])
    return response

@login_required
def export_csv_service(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_service_expense.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Car", "Mileage", "Place", "Service type", "Price", "Description"])

    for item in ServiceRecord.objects.filter(owner=request.user):
        writer.writerow([
            item.date.strftime('%d.%m.%Y %H:%M') if item.date else '',
            str(item.car) if item.car else '',
            str(item.miliage),
            item.place,
            item.get_service_type_display(),
            f"{item.price:.2f}",
            item.description,
        ])
    return response

@login_required
def export_csv_fuel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_fuel_expense.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Car", "Mileage", "Fuel type", "Fuel amount", "Price", "Gas station", "Description"])

    for item in FuelExpense.objects.filter(owner=request.user):
        writer.writerow([
            item.date.strftime('%d.%m.%Y %H:%M') if item.date else '',
            str(item.car) if item.car else '',
            str(item.miliage),
            item.get_fuel_type_display(),
            f"{item.fuel_amount:.2f}",
            f"{item.price:.2f}",
            item.gas_station,
            item.description,
        ])
    return response

@login_required
def export_csv_carpart(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_carpart_expense.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date purchase", "Item name", "Car", "Carpart type", "Price", "Place purchase",
                     "Date installation", "Place installation", "Description"])

    for item in Carpart.objects.filter(owner=request.user):
        writer.writerow([
            item.date_purchase.strftime('%d.%m.%Y %H:%M') if item.date_purchase else '',
            item.name,
            str(item.car) if item.car else '',
            item.get_carpart_type_display(),
            f"{item.price:.2f}",
            item.place_purchase,
            item.date_installation.strftime('%d.%m.%Y %H:%M') if item.date_installation else '',
            item.place_installation,
            item.description,
        ])
    return response