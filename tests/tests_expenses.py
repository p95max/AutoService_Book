import pytest
from django.urls import reverse
from django.utils import timezone
from service_book.models import Car, Brand, OtherExpense
from django.contrib.auth.models import User
from service_book.forms import AddNewOtherExpense

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
def other_expense(user, car):
    return OtherExpense.objects.create(
        owner=user,
        car=car,
        date=timezone.now(),
        name='Test Expense',
        expense_type='insurance',
        price=150,
        paid_status=True,
        description='Test insurance'
    )

@pytest.mark.django_db
def test_other_expense_list_view(client, user, car, other_expense):
    client.login(username='test', password='testing')
    response = client.get(reverse('other_expense'))
    assert response.status_code == 200
    assert 'other_expenses/other_expenses.html' in [t.name for t in response.templates]
    assert other_expense.name in response.content.decode()

@pytest.mark.django_db
def test_add_other_expense_get(client, user):
    client.login(username='test', password='testing')
    response = client.get(reverse('add_other_expense'))
    assert response.status_code == 200
    assert 'other_expenses/add_other_expense.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewOtherExpense)

@pytest.mark.django_db
def test_add_other_expense_post_valid(client, user, car):
    client.login(username='test', password='testing')
    data = {
        'car': car.pk,
        'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'name': 'New Expense',
        'expense_type': 'insurance',
        'price': 200,
        'paid_status': 'true',
        'description': 'New insurance',
    }
    response = client.post(reverse('add_other_expense'), data)
    assert response.status_code == 302
    assert OtherExpense.objects.filter(name='New Expense').exists()

@pytest.mark.django_db
def test_add_other_expense_post_invalid(client, user):
    client.login(username='test', password='testing')
    data = {}  # Empty data
    response = client.post(reverse('add_other_expense'), data)
    assert response.status_code == 200
    assert 'other_expenses/add_other_expense.html' in [t.name for t in response.templates]
    errors = response.context['form'].errors
    for field in ['date', 'name', 'expense_type', 'price', 'paid_status']:
        assert field in errors

@pytest.mark.django_db
def test_edit_other_expense_get(client, user, other_expense):
    client.login(username='test', password='testing')
    response = client.get(reverse('edit_other_expense', kwargs={'pk': other_expense.pk}))
    assert response.status_code == 200
    assert 'other_expenses/edit_other_expense.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], AddNewOtherExpense)

@pytest.mark.django_db
def test_edit_other_expense_post_valid(client, user, other_expense, car):
    client.login(username='test', password='testing')
    data = {
        'car': car.pk,
        'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'name': 'Edited Expense',
        'expense_type': 'tax',
        'price': 300,
        'paid_status': 'false',
        'description': 'Edited insurance',
    }
    response = client.post(reverse('edit_other_expense', kwargs={'pk': other_expense.pk}), data)
    assert response.status_code == 302
    other_expense.refresh_from_db()
    assert other_expense.name == 'Edited Expense'
    assert other_expense.price == 300
    assert other_expense.paid_status is False

@pytest.mark.django_db
def test_delete_other_expense_post_owner(client, user, other_expense):
    client.login(username='test', password='testing')
    response = client.post(reverse('delete_other_expense', kwargs={'pk': other_expense.pk}))
    assert response.status_code == 302
    assert not OtherExpense.objects.filter(pk=other_expense.pk).exists()

@pytest.mark.django_db
def test_delete_other_expense_get_redirect(client, user, other_expense):
    client.login(username='test', password='testing')
    response = client.get(reverse('delete_other_expense', kwargs={'pk': other_expense.pk}))
    assert response.status_code == 302  # View redirects on GET

@pytest.mark.django_db
def test_delete_other_expense_not_owner(client, user, brand):
    client.login(username='test', password='testing')
    other_user = User.objects.create_user(username='other_user', password='other_password')
    other_car = Car.objects.create(owner=other_user, model='Other car', brand=brand, prod_year=2015, miliage=50000)
    other_exp = OtherExpense.objects.create(
        owner=other_user,
        car=other_car,
        date=timezone.now(),
        name='Other User Expense',
        expense_type='fines',
        price=100,
        paid_status=True,
        description='Other user expense'
    )
    response = client.get(reverse('delete_other_expense', kwargs={'pk': other_exp.pk}))
    assert response.status_code == 404  # Expect 404 due to owner filter in get_object_or_404