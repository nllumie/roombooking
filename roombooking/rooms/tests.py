import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Room
from users.models import CustomUser

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    user = CustomUser.objects.create_user(
        username='adminuser',
        email='admin@example.com',
        password='admin123',
        department='IT',
        position='Admin',
        employee_id='ADMIN123',
        is_staff=True
    )
    return user

@pytest.fixture
def regular_user():
    user = CustomUser.objects.create_user(
        username='regularuser',
        email='regular@example.com',
        password='regular123',
        department='HR',
        position='Staff',
        employee_id='REG123'
    )
    return user

@pytest.fixture
def sample_room():
    room = Room.objects.create(
        name='Conference Room A',
        location='Floor 1',
        capacity=10,
        equipment='Projector, Whiteboard',
        description='Main conference room'
    )
    return room

@pytest.mark.django_db
def test_admin_can_create_room(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('room-list')
    data = {
        'name': 'New Room',
        'location': 'Floor 2',
        'capacity': 8,
        'equipment': 'TV Screen',
        'description': 'Small meeting room'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Room.objects.filter(name='New Room').exists()

@pytest.mark.django_db
def test_regular_user_cannot_create_room(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    url = reverse('room-list')
    data = {
        'name': 'New Room',
        'location': 'Floor 2',
        'capacity': 8,
        'equipment': 'TV Screen',
        'description': 'Small meeting room'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not Room.objects.filter(name='New Room').exists()

@pytest.mark.django_db
def test_list_rooms(api_client, regular_user, sample_room):
    api_client.force_authenticate(user=regular_user)
    url = reverse('room-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Conference Room A'

