import pytest
from django.urls import reverse
from django.utils import timezone
from service_book.models import User, Car, Brand, FuelExpense
from service_book.forms import AddNewFuelExpense

pytestmark = pytest.mark.django_db

@pytest.fixture
def user():
    return User.objects.create_user(username='test', password='testing')

@pytest.fixture
def brand():
    return Brand.objects.create(name='Test Brand')

@pytest.fixture
def car(user, brand):
    return Car.objects.create(owner=user, model='Test car', brand=brand, prod_year=2020, miliage=10000)

@pytest.fixture
def fuel_expense(user, car):
    return FuelExpense.objects.create(
        owner=user,
        car=car,
        price=100,
        date=timezone.now(),
        fuel_amount=40,
        fuel_type='diesel',
        distance=500,
        miliage=10500,
    )

def test_fuel_expense_view(client, user, car, fuel_expense):
    client.login(username='test', password='testing')
    response = client.get(reverse('fuel_expense'))
    assert response.status_code == 200
    assert 'fuel_expense/fuel_expense.html' in [t.name for t in response.templates]
    assert 'cars' in response.context
    assert 'page_obj' in response.context
    assert 'total_costs_all' in response.context

def test_add_fuel_expense_get(client, user):
    client.login(username='test', password='testing')
    response = client.get(reverse('add_fuel_expense'))
    assert response.status_code == 200
    assert 'fuel_expense/add_fuel_expense.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewFuelExpense)

def test_add_fuel_expense_post_valid(client, user, car):
    client.login(username='test', password='testing')
    data = {
        'car': car.id,
        'price': 150,
        'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'fuel_amount': 30,
        'fuel_type': 'diesel',
        'distance': 400,
        'miliage': 11000,
        'gas_station': 'Test Station',
    }
    response = client.post(reverse('add_fuel_expense'), data)
    # print(response.context['form'].errors)
    assert response.status_code == 302
    assert response.url == reverse('fuel_expense')
    assert FuelExpense.objects.filter(owner=user, car=car, price=150).exists()

def test_add_fuel_expense_post_invalid(client, user):
    client.login(username='test', password='testing')
    data = {}
    response = client.post(reverse('add_fuel_expense'), data)
    assert response.status_code == 200
    assert 'fuel_expense/add_fuel_expense.html' in [t.name for t in response.templates]
    assert 'car' in response.context['form'].errors

def test_edit_fuel_expense_get(client, user, fuel_expense):
    client.login(username='test', password='testing')
    response = client.get(reverse('edit_fuel_expense', kwargs={'pk': fuel_expense.pk}))
    assert response.status_code == 200
    assert 'fuel_expense/edit_fuel_expense.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewFuelExpense)

def test_edit_fuel_expense_post_valid(client, user, fuel_expense, car):
    client.login(username='test', password='testing')
    data = {
        'car': car.id,
        'price': 200,
        'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'fuel_amount': 35,
        'fuel_type': 'diesel',
        'distance': 450,
        'miliage': 11500,
        'gas_station': 'Test Station',
    }
    response = client.post(reverse('edit_fuel_expense', kwargs={'pk': fuel_expense.pk}), data)
    # print(response.context['form'].errors)
    assert response.status_code == 302
    assert response.url == reverse('fuel_expense')
    fuel_expense.refresh_from_db()
    assert fuel_expense.price == 200
    assert fuel_expense.fuel_amount == 35

def test_edit_fuel_expense_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_car = Car.objects.create(owner=other_user, model='Other car', brand=brand, prod_year=2015, miliage=50000)
    other_record = FuelExpense.objects.create(
        owner=other_user,
        car=other_car,
        price=50,
        date=timezone.now(),
        fuel_amount=20,
        fuel_type='diesel',
        distance=300,
        miliage=50500,
    )
    response = client.get(reverse('edit_fuel_expense', kwargs={'pk': other_record.pk}))
    assert response.status_code == 404

def test_delete_fuel_expense_post_owner(client, user, fuel_expense):
    client.login(username='test', password='testing')
    response = client.post(reverse('delete_fuel_expense', kwargs={'pk': fuel_expense.pk}))
    assert response.status_code == 302
    assert response.url == reverse('fuel_expense')
    assert not FuelExpense.objects.filter(pk=fuel_expense.pk).exists()

def test_delete_fuel_expense_get_redirect(client, user, fuel_expense):
    client.login(username='test', password='testing')
    response = client.get(reverse('delete_fuel_expense', kwargs={'pk': fuel_expense.pk}))
    assert response.status_code == 302
    assert response.url == reverse('fuel_expense')

def test_delete_fuel_expense_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_car = Car.objects.create(owner=other_user, model='Other car', brand=brand, prod_year=2015, miliage=50000)
    other_record = FuelExpense.objects.create(
        owner=other_user,
        car=other_car,
        price=50,
        date=timezone.now(),
        fuel_amount=20,
        fuel_type='diesel',
        distance=300,
        miliage=50500,
    )
    response = client.get(reverse('delete_fuel_expense', kwargs={'pk': other_record.pk}))
    assert response.status_code == 404