import pytest
from django.urls import reverse
from django.utils import timezone
from service_book.models import Car, Brand, Carpart
from django.contrib.auth.models import User
from service_book.forms import AddNewCarPart

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
        date_purchase=timezone.now(),  # Use aware datetime
        name='Test Part',
        carpart_type='tyre',
        price=100,
        place_purchase='Test Store',
        description='Test car part'
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
    assert isinstance(response.context['form'], AddNewCarPart)

@pytest.mark.django_db
def test_add_carpart_post_valid(client, user, car):
    client.login(username='test', password='testing')
    data = {
        'car': car.pk,
        'date_purchase': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'name': 'New Part',
        'carpart_type': 'tyre',
        'price': 200,
        'place_purchase': 'New Store',
        'description': 'New car part',
    }
    response = client.post(reverse('add_carpart'), data)
    assert response.status_code == 302
    assert Carpart.objects.filter(name='New Part').exists()

@pytest.mark.django_db
def test_edit_carpart_get(client, user, carpart):
    client.login(username='test', password='testing')
    response = client.get(reverse('edit_carpart', kwargs={'pk': carpart.pk}))
    assert response.status_code == 200
    assert 'carparts/edit_carpart.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewCarPart)

@pytest.mark.django_db
def test_edit_carpart_post_valid(client, user, carpart, car):
    client.login(username='test', password='testing')
    data = {
        'car': car.pk,
        'date_purchase': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'name': 'Edited Part',
        'carpart_type': 'tyre',
        'price': 200,
        'place_purchase': 'Edited Store',
        'description': 'Edited car part',
    }
    response = client.post(reverse('edit_carpart', kwargs={'pk': carpart.pk}), data)
    assert response.status_code == 302
    carpart.refresh_from_db()
    assert carpart.name == 'Edited Part'
    assert carpart.price == 200

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
    assert response.status_code == 302  # View redirects on GET

@pytest.mark.django_db
def test_delete_carpart_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_car = Car.objects.create(owner=other_user, model='Other car', brand=brand, prod_year=2015, miliage=50000)
    other_part = Carpart.objects.create(
        owner=other_user,
        car=other_car,
        date_purchase=timezone.now(),
        name='Other User Part',
        carpart_type='tyre',
        price=100,
        place_purchase='Other Store',
        description='Other user part'
    )
    response = client.get(reverse('delete_carpart', kwargs={'pk': other_part.pk}))
    assert response.status_code == 404  # Expect 404 due to owner filter