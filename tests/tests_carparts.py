import pytest
from django.urls import reverse
from django.utils import timezone
from service_book.models import User, Car, Brand, Carpart
from service_book.forms import AddNewCarPart

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
def carpart(user, car):
    return Carpart.objects.create(
        owner=user,
        car=car,
        date_purchase=timezone.now(),
        name='Test Part',
        carpart_type='engine',  # подставь актуальный тип из choices!
        price=500,
        place_purchase='Test Store',
        date_installation=timezone.now().date(),
        place_installation='Test Garage',
        description='Test description',
    )

def test_car_parts_view(client, user, car, carpart):
    client.login(username='test', password='testing')
    response = client.get(reverse('my_carparts'))
    assert response.status_code == 200
    assert 'carparts/my_carparts.html' in [t.name for t in response.templates]
    assert 'cars' in response.context
    assert 'page_obj' in response.context
    assert 'total_costs_per_car' in response.context

def test_add_carpart_get(client, user):
    client.login(username='test', password='testing')
    response = client.get(reverse('add_carpart'))
    assert response.status_code == 200
    assert 'carparts/add_carpart.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewCarPart)

def test_add_carpart_post_valid(client, user, car):
    client.login(username='test', password='testing')
    data = {
        'date_purchase': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'name': 'Test Part',
        'car': car.id,
        'carpart_type': 'engine',  # подставь актуальный тип из choices!
        'price': 500,
        'place_purchase': 'Test Store',
        'date_installation': timezone.now().strftime('%Y-%m-%d'),
        'place_installation': 'Test Garage',
        'description': 'Test description',
    }
    response = client.post(reverse('add_carpart'), data)
    assert response.status_code == 302
    assert response.url == reverse('my_carparts')
    assert Carpart.objects.filter(owner=user, car=car, name='Test Part').exists()

def test_add_carpart_post_invalid(client, user):
    client.login(username='test', password='testing')
    data = {}
    response = client.post(reverse('add_carpart'), data)
    assert response.status_code == 200
    assert 'carparts/add_carpart.html' in [t.name for t in response.templates]
    assert 'car' in response.context['form'].errors

def test_edit_carpart_get(client, user, carpart):
    client.login(username='test', password='testing')
    response = client.get(reverse('edit_carpart', kwargs={'pk': carpart.pk}))
    assert response.status_code == 200
    assert 'carparts/edit_carpart.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewCarPart)

def test_edit_carpart_post_valid(client, user, carpart, car):
    client.login(username='test', password='testing')
    data = {
        'date_purchase': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'name': 'Updated Part',
        'car': car.id,
        'carpart_type': 'engine',  # подставь актуальный тип из choices!
        'price': 600,
        'place_purchase': 'Updated Store',
        'date_installation': timezone.now().strftime('%Y-%m-%d'),
        'place_installation': 'Updated Garage',
        'description': 'Updated description',
    }
    response = client.post(reverse('edit_carpart', kwargs={'pk': carpart.pk}), data)
    assert response.status_code == 302
    assert response.url == reverse('my_carparts')
    carpart.refresh_from_db()
    assert carpart.name == 'Updated Part'
    assert carpart.price == 600

def test_edit_carpart_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_car = Car.objects.create(owner=other_user, model='Other car', brand=brand, prod_year=2015, miliage=50000)
    other_part = Carpart.objects.create(
        owner=other_user,
        car=other_car,
        date_purchase=timezone.now(),
        name='Other Part',
        carpart_type='engine',  # подставь актуальный тип из choices!
        price=100,
        place_purchase='Other Store',
        date_installation=timezone.now().date(),
        place_installation='Other Garage',
        description='Other description',
    )
    response = client.get(reverse('edit_carpart', kwargs={'pk': other_part.pk}))
    assert response.status_code == 404

def test_delete_car_part_post_owner(client, user, carpart):
    client.login(username='test', password='testing')
    response = client.post(reverse('delete_car_part', kwargs={'pk': carpart.pk}))
    assert response.status_code == 302
    assert response.url == reverse('my_carparts')
    assert not Carpart.objects.filter(pk=carpart.pk).exists()

def test_delete_car_part_get_redirect(client, user, carpart):
    client.login(username='test', password='testing')
    response = client.get(reverse('delete_car_part', kwargs={'pk': carpart.pk}))
    assert response.status_code == 302
    assert response.url == reverse('my_carparts')

def test_delete_car_part_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_car = Car.objects.create(owner=other_user, model='Other car', brand=brand, prod_year=2015, miliage=50000)
    other_part = Carpart.objects.create(
        owner=other_user,
        car=other_car,
        date_purchase=timezone.now(),
        name='Other Part',
        carpart_type='engine',  # подставь актуальный тип из choices!
        price=100,
        place_purchase='Other Store',
        date_installation=timezone.now().date(),
        place_installation='Other Garage',
        description='Other description',
    )
    response = client.get(reverse('delete_car_part', kwargs={'pk': other_part.pk}))
    assert response.status_code == 404