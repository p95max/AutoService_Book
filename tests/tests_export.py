
import pytest
import csv
from io import StringIO
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from service_book.models import Brand, Car, OtherExpense, ServiceRecord, FuelExpense, Carpart

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testing')

@pytest.fixture
def brand(db):
    return Brand.objects.create(name='Test Brand')

@pytest.fixture
def car(user, brand):
    return Car.objects.create(
        owner=user,
        model='Test Car',
        brand=brand,
        prod_year=2020,
        miliage=10000
    )

@pytest.fixture
def other_expense(user, car):
    return OtherExpense.objects.create(
        owner=user,
        car=car,
        date=timezone.now(),
        name='Test Expense',
        expense_type='insurance',
        price=150.00,
        paid_status=True,
        description='Test insurance expense'
    )

@pytest.fixture
def service_record(user, car):
    return ServiceRecord.objects.create(
        owner=user,
        car=car,
        date=timezone.now(),
        miliage=10000,
        place='Test Garage',
        service_type='interval_service',
        price=200.00,
        description='Test service'
    )

@pytest.fixture
def fuel_expense(user, car):
    return FuelExpense.objects.create(
        owner=user,
        car=car,
        date=timezone.now(),
        miliage=10000,
        fuel_type='petrol_e5',
        fuel_amount=50.00,
        price=75.00,
        gas_station='Test Station',
        description='Test fuel expense'
    )

@pytest.fixture
def carpart(user, car):
    return Carpart.objects.create(
        owner=user,
        car=car,
        date_purchase=timezone.now(),
        name='Test Part',
        carpart_type='tyre',
        price=100.00,
        place_purchase='Test Store',
        date_installation=timezone.now(),
        place_installation='Test Garage',
        description='Test car part'
    )

@pytest.mark.django_db
def test_export_csv_other_authenticated(client, user, other_expense):
    client.login(username='testuser', password='testing')
    response = client.get(reverse('export_other_csv'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert response['Content-Disposition'] == f'attachment; filename="{user.username}_other_expense.csv"'

    # Парсим содержимое CSV
    content = response.content.decode('utf-8')
    csv_reader = csv.reader(StringIO(content))
    headers = next(csv_reader)
    assert headers == ["Date", "Name", "Car", "Price", "Expense type", "Paid status", "Description"]

    # Проверяем строку данных
    data_row = next(csv_reader)
    assert data_row[1] == other_expense.name
    assert data_row[2] == str(other_expense.car)
    assert data_row[3] == f"{other_expense.price:.2f}"  # Ожидаем 150.00
    assert data_row[4] == other_expense.get_expense_type_display()
    assert data_row[5] == 'Paid'
    assert data_row[6] == other_expense.description

@pytest.mark.django_db
def test_export_csv_other_unauthenticated(client):
    response = client.get(reverse('export_other_csv'))
    assert response.status_code == 302
    assert '/accounts/login/' in response.url

@pytest.mark.django_db
def test_export_csv_service_authenticated(client, user, service_record):
    client.login(username='testuser', password='testing')
    response = client.get(reverse('export_service_csv'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert response['Content-Disposition'] == f'attachment; filename="{user.username}_service_expense.csv"'

    # Парсим содержимое CSV
    content = response.content.decode('utf-8')
    csv_reader = csv.reader(StringIO(content))
    headers = next(csv_reader)
    assert headers == ["Date", "Car", "Mileage", "Place", "Service type", "Price", "Description"]

    # Проверяем строку данных
    data_row = next(csv_reader)
    assert data_row[1] == str(service_record.car)
    assert data_row[2] == str(service_record.miliage)
    assert data_row[3] == service_record.place
    assert data_row[4] == service_record.get_service_type_display()
    assert data_row[5] == f"{service_record.price:.2f}"  # Ожидаем 200.00
    assert data_row[6] == service_record.description

@pytest.mark.django_db
def test_export_csv_service_unauthenticated(client):
    response = client.get(reverse('export_service_csv'))
    assert response.status_code == 302
    assert '/accounts/login/' in response.url

@pytest.mark.django_db
def test_export_csv_fuel_authenticated(client, user, fuel_expense):
    client.login(username='testuser', password='testing')
    response = client.get(reverse('export_fuel_csv'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert response['Content-Disposition'] == f'attachment; filename="{user.username}_fuel_expense.csv"'

    # Парсим содержимое CSV
    content = response.content.decode('utf-8')
    csv_reader = csv.reader(StringIO(content))
    headers = next(csv_reader)
    assert headers == ["Date", "Car", "Mileage", "Fuel type", "Fuel amount", "Price", "Gas station", "Description"]

    # Проверяем строку данных
    data_row = next(csv_reader)
    assert data_row[1] == str(fuel_expense.car)
    assert data_row[2] == str(fuel_expense.miliage)
    assert data_row[3] == fuel_expense.get_fuel_type_display()
    assert data_row[4] == f"{fuel_expense.fuel_amount:.2f}"  # Ожидаем 50.00
    assert data_row[5] == f"{fuel_expense.price:.2f}"  # Ожидаем 75.00
    assert data_row[6] == fuel_expense.gas_station
    assert data_row[7] == fuel_expense.description

@pytest.mark.django_db
def test_export_csv_fuel_unauthenticated(client):
    response = client.get(reverse('export_fuel_csv'))
    assert response.status_code == 302
    assert '/accounts/login/' in response.url

@pytest.mark.django_db
def test_export_csv_carpart_authenticated(client, user, carpart):
    client.login(username='testuser', password='testing')
    response = client.get(reverse('export_carpart_csv'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert response['Content-Disposition'] == f'attachment; filename="{user.username}_carpart_expense.csv"'

    # Парсим содержимое CSV
    content = response.content.decode('utf-8')
    csv_reader = csv.reader(StringIO(content))
    headers = next(csv_reader)
    assert headers == ["Date purchase", "Item name", "Car", "Carpart type", "Price", "Place purchase",
                       "Date installation", "Place installation", "Description"]

    # Проверяем строку данных
    data_row = next(csv_reader)
    assert data_row[1] == carpart.name
    assert data_row[2] == str(carpart.car)
    assert data_row[3] == carpart.get_carpart_type_display()
    assert data_row[4] == f"{carpart.price:.2f}"  # Ожидаем 100.00
    assert data_row[5] == carpart.place_purchase
    assert data_row[7] == carpart.place_installation
    assert data_row[8] == carpart.description

@pytest.mark.django_db
def test_export_csv_carpart_unauthenticated(client):
    response = client.get(reverse('export_carpart_csv'))
    assert response.status_code == 302
    assert '/accounts/login/' in response.url

@pytest.mark.django_db
def test_export_csv_other_empty(client, user):
    client.login(username='testuser', password='testing')
    response = client.get(reverse('export_other_csv'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert response['Content-Disposition'] == f'attachment; filename="{user.username}_other_expense.csv"'
    content = response.content.decode('utf-8')
    csv_reader = csv.reader(StringIO(content))
    headers = next(csv_reader)
    assert headers == ["Date", "Name", "Car", "Price", "Expense type", "Paid status", "Description"]
    assert len(list(csv_reader)) == 0  # Нет строк с данными