import pytest


@pytest.fixture
def staff_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='StaffUser',
        password='strong-test-pass',
        is_staff=True
    )


@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user_client(staff_user, client):

    client.force_authenticate(user=staff_user)
    yield client
    client.force_authenticate(user=None)
