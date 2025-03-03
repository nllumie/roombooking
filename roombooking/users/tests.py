import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    user = CustomUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='password123',
        department='IT',
        position='Developer',
        employee_id='EMP123'
    )
    return user

@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse('register')
    data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpassword123',
        'department': 'HR',
        'position': 'Manager',
        'employee_id': 'EMP456'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert CustomUser.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_user_login(api_client, create_user):
    url = reverse('token_obtain_pair')
    data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

