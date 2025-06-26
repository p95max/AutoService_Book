import pytest
from django.urls import reverse
from django.utils import timezone
from service_book.models import User, Car, Brand, ServiceRecord
from service_book.forms import AddNewServiceRecord

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
def service_record(user, car):
    return ServiceRecord.objects.create(
        owner=user,
        car=car,
        price=100,
        date=timezone.now(),
        service_type='interval_service',
        place='Test Service Station',
        miliage=10000,
    )

def test_user_service_history_view_status(client, user, car, service_record):
    client.login(username='test', password='testing')
    response = client.get(reverse('service_history'))
    assert response.status_code == 200
    assert 'service_records/service_history.html' in [t.name for t in response.templates]
    assert 'cars' in response.context
    assert 'page_obj' in response.context
    assert 'user_total_service_costs' in response.context
    assert response.context['user_total_service_costs'] == 100

def test_add_service_get(client, user):
    client.login(username='test', password='testing')
    response = client.get(reverse('add_service'))
    assert response.status_code == 200
    assert 'service_records/add_service.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewServiceRecord)

def test_add_service_post_valid(client, user, car):
    client.login(username='test', password='testing')
    data = {
        'car': car.id,
        'price': 200,
        'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'service_type': 'interval_service',
        'place': 'Test Service Station',
        'miliage': 12345,
    }
    response = client.post(reverse('add_service'), data)
    assert response.status_code == 302
    assert response.url == reverse('service_history')
    assert ServiceRecord.objects.filter(owner=user, car=car, price=200).exists()

def test_add_service_post_invalid(client, user):
    client.login(username='test', password='testing')
    data = {}
    response = client.post(reverse('add_service'), data)
    assert response.status_code == 200
    assert 'service_records/add_service.html' in [t.name for t in response.templates]
    assert 'car' in response.context['form'].errors

def test_edit_service_get_by_owner(client, user, service_record):
    client.login(username='test', password='testing')
    response = client.get(reverse('edit_service', kwargs={'pk': service_record.pk}))
    assert response.status_code == 200
    assert 'service_records/edit_service.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewServiceRecord)

def test_edit_service_post_valid(client, user, service_record, car):
    client.login(username='test', password='testing')
    data = {
        'car': car.id,
        'price': 200,
        'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'service_type': 'interval_service',
        'place': 'Test Service Station',
        'miliage': 12345,
    }
    response = client.post(reverse('edit_service', kwargs={'pk': service_record.pk}), data)
    assert response.status_code == 302
    assert response.url == reverse('service_history')
    service_record.refresh_from_db()
    assert service_record.price == 200
    assert service_record.service_type == 'interval_service'

def test_edit_service_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_car = Car.objects.create(owner=other_user, model='Other car', brand=brand, prod_year=2015, miliage=50000)
    other_record = ServiceRecord.objects.create(
        owner=other_user,
        car=other_car,
        price=50,
        date=timezone.now(),
        service_type='interval_service',
        place='Other Service Station',
        miliage=50000,
    )
    response = client.get(reverse('edit_service', kwargs={'pk': other_record.pk}))
    assert response.status_code == 404

def test_delete_service_post_owner(client, user, service_record):
    client.login(username='test', password='testing')
    response = client.post(reverse('delete_service', kwargs={'pk': service_record.pk}))
    assert response.status_code == 302
    assert response.url == reverse('service_history')
    assert not ServiceRecord.objects.filter(pk=service_record.pk).exists()

def test_delete_service_get_redirect(client, user, service_record):
    client.login(username='test', password='testing')
    response = client.get(reverse('delete_service', kwargs={'pk': service_record.pk}))
    assert response.status_code == 302
    assert response.url == reverse('service_history')

def test_delete_service_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_car = Car.objects.create(owner=other_user, model='Other car', brand=brand, prod_year=2015, miliage=50000)
    other_record = ServiceRecord.objects.create(
        owner=other_user,
        car=other_car,
        price=50,
        date=timezone.now(),
        service_type='interval_service',
        place='Other Service Station',
        miliage=50000,
    )
    response = client.get(reverse('delete_service', kwargs={'pk': other_record.pk}))
    assert response.status_code == 404