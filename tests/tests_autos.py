import pytest
from unittest.mock import patch
from django.urls import reverse
from django.utils import timezone
from service_book import forms
from service_book.forms import AddNewAuto
from service_book.models import User, Car, Brand, Carpart, OtherExpense, FuelExpense, ServiceRecord

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
def setup_related(user, car):
    FuelExpense.objects.create(owner=user, car=car, price=10, date=timezone.now(), fuel_amount=10)
    ServiceRecord.objects.create(owner=user, car=car, price=15, date=timezone.now())
    Carpart.objects.create(owner=user, car=car, price=20, date_purchase=timezone.now())
    OtherExpense.objects.create(owner=user, car=car, price=5, date=timezone.now())

def test_user_autos_view_status(client, user, car, setup_related):
    client.login(username='test', password='testing')
    response = client.get(reverse('autos'))
    assert response.status_code == 200
    assert 'autos/my_autos.html' in [t.name for t in response.templates]
    assert 'cars' in response.context
    assert 'total_sum' in response.context
    assert response.context['total_sum'] == 50.0

def test_add_autos_get(client, user, brand):
    client.login(username='test', password='testing')
    response = client.get(reverse('add_auto'))
    assert response.status_code == 200
    assert 'autos/add_auto.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], forms.AddNewAuto)

def test_add_autos_post_valid(client, user, brand):
    client.login(username='test', password='testing')
    data = {
        'model': 'New Test model',
        'brand': brand.id,
        'prod_year': 2020,
        'miliage': 10000,
    }
    response = client.post(reverse('add_auto'), data)
    assert response.status_code == 302
    assert response.url == reverse('autos')
    assert Car.objects.filter(owner=user, model="New Test model").exists()

def test_add_autos_post_invalid(client, user):
    client.login(username='test', password='testing')
    data = {}
    response = client.post(reverse('add_auto'), data)
    assert response.status_code == 200
    assert 'autos/add_auto.html' in [t.name for t in response.templates]
    assert 'model' in response.context['form'].errors

def test_edit_autos_get_by_owner(client, user, car):
    client.login(username='test', password='testing')
    response = client.get(reverse('edit_auto', kwargs={'pk': car.pk}))
    assert response.status_code == 200
    assert 'autos/edit_auto.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewAuto)

def test_edit_autos_post_valid(client, user, car, brand):
    client.login(username='test', password='testing')
    data = {
        'model': 'Updated model',
        'brand': brand.id,
        'prod_year': 2020,
        'miliage': 10000,
    }
    response = client.post(reverse('edit_auto', kwargs={'pk': car.pk}), data)
    assert response.status_code == 302
    assert response.url == reverse('autos')
    car.refresh_from_db()
    assert car.model == 'Updated model'

def test_edit_autos_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_brand = Brand.objects.create(name='Other Brand')
    other_car = Car.objects.create(owner=other_user, model='Other model', prod_year=2000, miliage=100000, brand=other_brand)
    response = client.get(reverse('edit_auto', kwargs={'pk': other_car.pk}))
    assert response.status_code == 404

@patch('django.core.cache.cache.delete')
def test_delete_auto_post_owner(mock_cache_delete, client, user, car):
    client.login(username='test', password='testing')
    response = client.post(reverse('delete_auto', kwargs={'pk': car.pk}))
    assert response.status_code == 302
    assert response.url == reverse('autos')
    assert not Car.objects.filter(pk=car.pk).exists()
    mock_cache_delete.assert_called_once_with(f'user_{user.id}_cars_count')

def test_delete_auto_get_redirect(client, user, car):
    client.login(username='test', password='testing')
    response = client.get(reverse('delete_auto', kwargs={'pk': car.pk}))
    assert response.status_code == 302
    assert response.url == reverse('autos')

def test_delete_auto_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_brand = Brand.objects.create(name='Other Brand')
    other_car = Car.objects.create(owner=other_user, model='Other model', brand=other_brand, prod_year=2000, miliage=100000)
    response = client.get(reverse('delete_auto', kwargs={'pk': other_car.pk}))
    assert response.status_code == 404

def test_add_auto_without_vin():
    brand = Brand.objects.create(name='No VIN Brand')
    form = AddNewAuto(data={
        'brand': brand.id,
        'model': 'No VIN car',
        'prod_year': 2020,
        'miliage': 12000,
    })
    assert form.is_valid()

def test_user_autos_empty(client, user, car, setup_related):
    client.login(username='test', password='testing')
    car.delete()
    Car.objects.filter(owner=user).delete()
    response = client.get(reverse('autos'))
    assert response.status_code == 200
    assert list(response.context['cars']) == []
    assert response.context['total_sum'] == 50.0

# --- Model tests ---

@pytest.fixture
def model_user():
    return User.objects.create_user(username='testuser', password='13345')

@pytest.fixture
def model_brand():
    return Brand.objects.create(name='Brand')

@pytest.fixture
def model_car(model_user, model_brand):
    return Car.objects.create(owner=model_user, brand=model_brand, model='Model', prod_year=2010, miliage=11111)

def test_create_new_car_test(model_user, model_brand):
    car = Car.objects.create(owner=model_user, brand=model_brand, model='Model', prod_year=2010, miliage=11111)
    assert str(car) == f'{model_brand.name} - {car.model}'

def test_edit_car_test(client, model_user, model_brand):
    client.login(username='testuser', password='13345')
    car = Car.objects.create(owner=model_user, brand=model_brand, model='Model', prod_year=2010, miliage=11111)
    url = reverse('edit_auto', args=[car.id])
    response = client.post(url, {
        'owner': model_user.id,
        'brand': model_brand.id,
        'model': 'New Model',
        'prod_year': 2012,
        'miliage': 12345,
    })
    car.refresh_from_db()
    assert car.model == 'New Model'
    assert car.prod_year == 2012
    assert car.miliage == 12345
    assert response.status_code == 302

def test_delete_auto_post_test(client, model_user, model_brand, model_car):
    client.login(username='testuser', password='13345')
    response = client.post(reverse('delete_auto', args=[model_car.id]))
    assert not Car.objects.filter(id=model_car.id).exists()
    assert response.status_code == 302