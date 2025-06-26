import pytest
from django.urls import reverse
from django.utils import timezone
from service_book.models import Carpart, Car, Brand
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(username='test', password='testing')

@pytest.fixture
def brand(db):
    return Brand.objects.create(name='Test Brand')

@pytest.fixture
def car(user, brand):
    return Car.objects.create(owner=user, model='Test car', brand=brand, prod_year=2020, miliage=10000)

@pytest.fixture
def carpart(user, car):
    return Carpart.objects.create(
        owner=user,
        car=car,
        date_purchase=timezone.now().date(),
        name='Test Part',
        carpart_type='engine',  # подставь актуальный тип из choices!
        price=123.45,
        place_purchase='Test Store',
        date_installation=timezone.now().date(),
        place_installation='Test Garage',
        description='Car engine part'
    )

@pytest.mark.django_db
def test_car_parts_view(client, user, car, carpart):
    client.login(username='test', password='testing')
    response = client.get(reverse('my_carparts'))
    assert response.status_code == 200
    assert 'carparts/my_carparts.html' in [t.name for t in response.templates]
    assert carpart.name in response.content.decode()

@pytest.mark.django_db
def test_add_carpart_get(client, user):
    client.login(username='test', password='testing')
    response = client.get(reverse('add_carpart'))
    assert response.status_code == 200
    assert 'carparts/add_carpart.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_add_carpart_post_valid(client, user, car):
    client.login(username='test', password='testing')
    data = {
        'date_purchase': timezone.now().date(),
        'name': 'New Part',
        'car': car.pk,
        'carpart_type': 'engine',  # подставь актуальный тип из choices!
        'price': 100,
        'place_purchase': 'Store',
        'date_installation': timezone.now().date(),
        'place_installation': 'Garage',
        'description': 'desc',
    }
    response = client.post(reverse('add_carpart'), data)
    assert response.status_code == 302  # redirect after success
    assert Carpart.objects.filter(name='New Part').exists()

@pytest.mark.django_db
def test_add_carpart_post_invalid(client, user):
    client.login(username='test', password='testing')
    data = {}  # пустые данные
    response = client.post(reverse('add_carpart'), data)
    assert response.status_code == 200
    assert 'carparts/add_carpart.html' in [t.name for t in response.templates]
    # Проверяем, что форма невалидна и есть ошибки по обязательным полям
    errors = response.context['form'].errors
    for field in ['date_purchase', 'name', 'carpart_type', 'price', 'place_purchase']:
        assert field in errors

@pytest.mark.django_db
def test_edit_carpart_get(client, user, carpart):
    client.login(username='test', password='testing')
    response = client.get(reverse('edit_carpart', kwargs={'pk': carpart.pk}))
    assert response.status_code == 200
    assert 'carparts/edit_carpart.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_edit_carpart_post_valid(client, user, carpart, car):
    client.login(username='test', password='testing')
    data = {
        'date_purchase': timezone.now().date(),
        'name': 'Edited Part',
        'car': car.pk,
        'carpart_type': 'engine',
        'price': 200,
        'place_purchase': 'New Store',
        'date_installation': timezone.now().date(),
        'place_installation': 'New Garage',
        'description': 'edited desc',
    }
    response = client.post(reverse('edit_carpart', kwargs={'pk': carpart.pk}), data)
    assert response.status_code == 302
    carpart.refresh_from_db()
    assert carpart.name == 'Edited Part'

@pytest.mark.django_db
def test_delete_carpart_post_owner(client, user, carpart):
    client.login(username='test', password='testing')
    response = client.post(reverse('delete_carpart', kwargs={'pk': carpart.pk}))
    assert response.status_code == 302
    assert not Carpart.objects.filter(pk=carpart.pk).exists()

@pytest.mark.django_db
def test_delete_carpart_get_redirect(client, user, carpart):
    client.login(username='test', password='testing')
    response = client.get(reverse('delete_carpart', kwargs={'pk': carpart.pk}))
    # Обычно delete через GET редиректит или запрещён
    assert response.status_code in (302, 405)

@pytest.mark.django_db
def test_delete_carpart_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_car = Car.objects.create(owner=other_user, model='Other car', brand=brand, prod_year=2015, miliage=50000)
    other_part = Carpart.objects.create(
        owner=other_user,
        car=other_car,
        date_purchase=timezone.now().date(),
        name='Other Part',
        carpart_type='engine',
        price=100,
        place_purchase='Other Store',
        date_installation=timezone.now().date(),
        place_installation='Other Garage',
        description='Other description',
    )
    response = client.get(reverse('delete_carpart', kwargs={'pk': other_part.pk}))
    assert response.status_code in (302, 403, 404)